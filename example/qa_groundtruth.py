import os
import json
import random
import requests
import time
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv


class TreeNode:
    def __init__(self, value, path):
        self.value = value  # Node name (file or folder name)
        self.path = path  # Node path (relative to root directory)
        self.children = []  # List of child nodes


def build_tree_from_directory(root_dir, current_path=''):
    full_path = os.path.join(root_dir, current_path)
    node = TreeNode(os.path.basename(full_path) if current_path else os.path.basename(root_dir), current_path)

    if os.path.isdir(full_path):
        # Get all files and subfolders in the directory
        entries = os.listdir(full_path)
        for entry in entries:
            if entry == '.git':  # Ignore .git folder
                continue
            entry_path = os.path.join(current_path, entry)
            child_node = build_tree_from_directory(root_dir, entry_path)
            node.children.append(child_node)
    else:
        # If it's a file, return the node directly
        pass  # No additional processing needed for file nodes
    return node


def collect_parent_child_md_files(node):
    parent_child_pairs = []

    if os.path.isdir(os.path.join(root_docs_path, node.path)):
        md_files = []
        subfolders = []

        # Iterate through child nodes, distinguish between .md files and subfolders
        for child in node.children:
            child_full_path = os.path.join(root_docs_path, child.path)
            if os.path.isdir(child_full_path):
                subfolders.append(child)
            elif child.value.endswith('.md') and child.value != '_index.md':
                md_files.append(child)

        # If current node has .md files and subfolders, collect parent-child relationships
        if md_files and subfolders:
            for md_file in md_files:
                for subfolder in subfolders:
                    child_md_files = collect_all_md_files(subfolder)
                    for child_md in child_md_files:
                        parent_child_pairs.append(((md_file.path, md_file.path), (child_md.path, child_md.path)))

    # Recursively traverse subfolders
    for child in node.children:
        child_full_path = os.path.join(root_docs_path, child.path)
        if os.path.isdir(child_full_path):
            parent_child_pairs.extend(collect_parent_child_md_files(child))

    return parent_child_pairs


def collect_all_md_files(node):
    md_files = []
    node_full_path = os.path.join(root_docs_path, node.path)
    if os.path.isdir(node_full_path):
        for child in node.children:
            md_files.extend(collect_all_md_files(child))
    else:
        if node.value.endswith('.md') and node.value != '_index.md':
            md_files.append(node)
    return md_files


def read_md_files_from_paths(root_path, md_file_paths):
    contents = []
    md_files = []
    for md_file_path in md_file_paths:
        file_full_path = os.path.join(root_path, md_file_path)
        if os.path.isfile(file_full_path):
            try:
                with open(file_full_path, 'r', encoding='utf-8') as f:
                    contents.append(f.read())
                md_files.append(md_file_path)
            except Exception as e:
                print(f"Error reading file {file_full_path}: {str(e)}")
        else:
            print(f"File {file_full_path} not found")
    return contents, md_files


def create_prompt_from_contents(contents):
    # Combine multiple document contents and create appropriate prompt
    combined_content = '\n'.join(contents)
    prompt = (
        "Based on the following documents, please generate a question that requires combining multiple documents to answer, "
        "and provide a detailed answer. Both the question and answer should be in Chinese. "
        "Make sure the answer requires referencing content from multiple documents.\n\n"
        "Document contents:\n"
        f"{combined_content}"
    )
    return prompt


def generate_question_and_answer(prompt, api_url, api_key, max_retries=3, delay_seconds=3) -> Optional[str]:
    """
    Generate question and answer with retry mechanism and delay between requests

    Args:
        prompt: The input prompt
        api_url: Azure OpenAI API URL
        api_key: API key
        max_retries: Maximum number of retry attempts
        delay_seconds: Delay between requests in seconds

    Returns:
        Generated answer or None if failed
    """
    headers = {
        'Content-Type': 'application/json',
        'api-key': api_key
    }
    payload = {
        "messages": [
            {"role": "system", "content": "You are a knowledgeable assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000,
        "top_p": 0.95,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    for attempt in range(max_retries):
        try:
            # Add delay before each request (except first attempt)
            if attempt > 0:
                time.sleep(delay_seconds)

            print(f"Making API request (attempt {attempt + 1}/{max_retries})...")
            response = requests.post(api_url, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            elif response.status_code == 429:  # Rate limit exceeded
                retry_after = int(response.headers.get('Retry-After', delay_seconds))
                print(f"Rate limit exceeded. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                continue
            else:
                print(f"Request failed with status code: {response.status_code}")
                print(f"Response content: {response.text}")

        except requests.RequestException as e:
            print(f"Request error occurred: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay_seconds} seconds...")
                time.sleep(delay_seconds)
            continue

    print("All retry attempts failed")
    return None


def save_results(question_answer, md_files_list, output_path):
    data = {
        'question_answer': question_answer,
        'documents': md_files_list,
        'timestamp': datetime.now().isoformat()
    }
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Results saved to {output_path}")


def main():
    # Load environment variables
    load_dotenv()

    # Load configuration
    api_url = os.getenv('AZURE_OPENAI_API_URL')
    api_key = os.getenv('AZURE_OPENAI_API_KEY')

    if not api_url or not api_key:
        raise ValueError("Please set AZURE_OPENAI_API_URL and AZURE_OPENAI_API_KEY environment variables")

    # Specify your document root directory
    global root_docs_path
    root_docs_path = '.'  # Replace with actual path

    # Create output directory
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    # Build tree and collect pairs
    try:
        root = build_tree_from_directory(root_docs_path)
        parent_child_pairs = collect_parent_child_md_files(root)

        if not parent_child_pairs:
            print("No valid document pairs found.")
            return

        num_pairs_to_select = 5
        selected_pairs = random.sample(parent_child_pairs, min(num_pairs_to_select, len(parent_child_pairs)))

        for idx, pair in enumerate(selected_pairs, 1):
            parent_md_path, _ = pair[0]
            child_md_path, _ = pair[1]
            print(f"\nProcessing pair {idx}/{len(selected_pairs)}:")
            print(f"Parent: {parent_md_path}")
            print(f"Child: {child_md_path}")

            contents, md_files = read_md_files_from_paths(root_docs_path, [parent_md_path, child_md_path])

            if not contents:
                print("Files not found, skipping...")
                continue

            prompt = create_prompt_from_contents(contents)
            question_answer = generate_question_and_answer(prompt, api_url, api_key)

            if question_answer:
                output_file = os.path.join(output_dir, f'result_{idx}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
                save_results(question_answer, md_files, output_file)

            # Add delay between processing pairs
            if idx < len(selected_pairs):
                delay = 5  # 5 seconds between processing pairs
                print(f"Waiting {delay} seconds before processing next pair...")
                time.sleep(delay)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    main()