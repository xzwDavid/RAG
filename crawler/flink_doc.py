import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin


def clean_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip()


def save_to_markdown(url, title, label_dir):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到所有class为markdown的元素
        markdown_elements = soup.find_all(class_='markdown')

        if not markdown_elements:
            return False, f"{title} (Error: No markdown content found)"

        # 准备markdown内容
        markdown_content = [f"# {title}\n"]

        # 处理每个markdown元素
        for element in markdown_elements:
            # 获取所有文本内容，保持原有格式
            for child in element.descendants:
                if child.name:
                    if child.name.startswith('h'):
                        level = child.name[1]
                        markdown_content.append(f"\n{'#' * int(level)} {child.get_text(strip=True)}\n")
                    elif child.name == 'p':
                        markdown_content.append(f"\n{child.get_text()}\n")
                    elif child.name == 'ul':
                        for li in child.find_all('li', recursive=False):
                            markdown_content.append(f"* {li.get_text()}")
                    elif child.name == 'ol':
                        for i, li in enumerate(child.find_all('li', recursive=False), 1):
                            markdown_content.append(f"{i}. {li.get_text()}")
                    elif child.name == 'pre':
                        markdown_content.append(f"\n```\n{child.get_text()}\n```\n")
                    elif child.name == 'blockquote':
                        markdown_content.append(f"\n> {child.get_text()}\n")
                    elif child.name == 'code':
                        markdown_content.append(f"`{child.get_text()}`")

        # 处理文件名和保存
        safe_title = clean_filename(title)
        filepath = os.path.join(label_dir, f"{safe_title}.md")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_content))

        return True, filepath

    except Exception as e:
        return False, f"{title} (Error: {str(e)})"


def scrape_flink_docs():
    base_url = "https://nightlies.apache.org/flink/flink-docs-master/"
    base_dir = "flink_docs"
    successful_files = []
    failed_files = []

    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        labels = soup.find_all('label', class_='flex justify-between')

        for label in labels:
            label_text = label.get_text(strip=True)
            label_dir = os.path.join(base_dir, clean_filename(label_text))
            os.makedirs(label_dir, exist_ok=True)

            print(f"\n=== Processing {label_text} ===")

            next_ul = label.find_next_sibling('ul')
            if next_ul:
                links = next_ul.find_all('a')
                for link in links:
                    title = link.get_text(strip=True)
                    url = link.get('href')
                    full_url = urljoin('https:', url)

                    print(f"Processing: {title}")
                    print(f"URL: {full_url}")
                    success, filepath = save_to_markdown(full_url, title, label_dir)

                    if success:
                        successful_files.append(filepath)
                        print(f"✓ Saved to: {filepath}")
                    else:
                        failed_files.append(filepath)
                        print(f"✗ Failed: {filepath}")

                    time.sleep(1)

        print("\n=== Processing Complete ===")
        print(f"\nTotal successful files: {len(successful_files)}")
        print(f"Total failed files: {len(failed_files)}")

        if failed_files:
            print("\nFailed files:")
            for file in failed_files:
                print(f"✗ {file}")

    except Exception as e:
        print(f"An error occurred during scraping: {e}")

    return successful_files, failed_files


if __name__ == "__main__":
    successful, failed = scrape_flink_docs()