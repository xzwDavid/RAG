import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

def clean_filename(filename):
    """Clean the filename to remove invalid characters."""
    return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip()

def save_to_markdown(url, title, label_dir):
    """Fetch and save the content of a URL as a Markdown file."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find relevant content (specific to NumPy docs)
        # content_div = soup.find(class_="section")
        content_div = soup.find("article", class_="bd-article")
        if not content_div:
            return False, f"{title} (Error: No meaningful content found)"

        markdown_content = [f"# {title}\n"]

        # Process each element inside the content section
        for element in content_div.descendants:
            if element.name:
                if element.name.startswith('h'):
                    level = element.name[1]
                    markdown_content.append(f"\n{'#' * int(level)} {element.get_text(strip=True)}\n")
                elif element.name == 'p':
                    text = element.get_text(strip=True)
                    if text:  # Skip blank paragraphs
                        markdown_content.append(f"\n{text}\n")
                elif element.name == 'ul':
                    for li in element.find_all('li', recursive=False):
                        markdown_content.append(f"* {li.get_text(strip=True)}")
                elif element.name == 'ol':
                    for i, li in enumerate(element.find_all('li', recursive=False), 1):
                        markdown_content.append(f"{i}. {li.get_text(strip=True)}")
                elif element.name == 'pre':
                    markdown_content.append(f"\n```\n{element.get_text(strip=True)}\n```\n")
                elif element.name == 'blockquote':
                    markdown_content.append(f"\n> {element.get_text(strip=True)}\n")
                elif element.name == 'code':
                    markdown_content.append(f"`{element.get_text(strip=True)}`")

        # Clean up blank lines
        cleaned_content = "\n".join(line for line in markdown_content if line.strip())

        # Prepare the directory and save the file
        safe_title = clean_filename(title)
        filepath = os.path.join(label_dir, f"{safe_title}.md")
        os.makedirs(label_dir, exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)

        return True, filepath

    except Exception as e:
        return False, f"{title} (Error: {str(e)})"

def crawl_numpy_docs(base_url, base_dir="doc/numpy_docs", depth=3):
    """Crawl the NumPy API reference and save content as Markdown."""
    visited = set()
    successful_files = []
    failed_files = []

    def crawl(url, directory, current_depth):
        if current_depth == 0 or url in visited:
            return

        visited.add(url)

        try:
            # print("hhh")
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Process links at the current level
            links = soup.find_all("li", class_=f"toctree-l{4 - current_depth}")
            for link in links:
                a_tag = link.find('a', href=True)
                if a_tag:
                    title = a_tag.get_text(strip=True)
                    full_url = urljoin(url, a_tag['href'])

                    print(f"Processing: {title} (Depth: {current_depth})")
                    success, result = save_to_markdown(full_url, title, directory)

                    if success:
                        successful_files.append(result)
                        print(f"✓ Saved to: {result}")
                    else:
                        failed_files.append(result)
                        print(f"✗ Failed: {result}")

                    # Recursively crawl sub-levels
                    subdirectory = os.path.join(directory, clean_filename(title))
                    crawl(full_url, subdirectory, current_depth - 1)

        except Exception as e:
            print(f"Error while crawling {url}: {e}")

    # Start crawling from the base URL
    crawl(base_url, base_dir, depth)

    print("\n=== Crawling Complete ===")
    print(f"Total successful files: {len(successful_files)}")
    print(f"Total failed files: {len(failed_files)}")

    if failed_files:
        print("\nFailed files:")
        for file in failed_files:
            print(f"✗ {file}")

    return successful_files, failed_files

if __name__ == "__main__":
    base_url = "https://numpy.org/doc/stable/reference/index.html"
    crawl_numpy_docs(base_url)

