import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin


def clean_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip()


def convert_element_to_markdown(element):
    """将单个HTML元素转换为markdown文本"""
    if isinstance(element, str):
        return element.strip()

    # 处理各种HTML标签
    if element.name == 'a':
        return f"[{element.get_text()}]({element.get('href', '')})"
    elif element.name == 'acronym':
        return element.get_text()
    elif element.name == 'code':
        return f"`{element.get_text()}`"
    elif element.name == 'strong' or element.name == 'b':
        return f"**{element.get_text()}**"
    elif element.name == 'em' or element.name == 'i':
        return f"*{element.get_text()}*"
    elif element.name == 'span':
        return element.get_text()
    else:
        return element.get_text()


def save_to_markdown(url, title, section_dir):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找文档内容区域
        doc_content = soup.find('div', id='docContent')
        if not doc_content:
            return False, f"{title} (Error: No content found)"

        markdown_content = [f"# {title}\n"]

        for section in doc_content.find_all(['div'], class_=['sect1', 'sect2', 'sect3']):
            # 处理所有段落和内容
            for element in section.children:
                if element.name:
                    # 处理标题
                    if element.name in ['h1', 'h2', 'h3', 'h4']:
                        level = int(element.name[1])
                        markdown_content.append(f"\n{'#' * level} {element.get_text(strip=True)}\n")

                    # 处理段落
                    elif element.name == 'p':
                        para_content = []
                        for child in element.children:
                            para_content.append(convert_element_to_markdown(child))
                        markdown_content.append(f"\n{''.join(para_content)}\n")

                    # 处理列表
                    elif element.name == 'ul':
                        for li in element.find_all('li', recursive=False):
                            markdown_content.append(f"* {li.get_text()}")
                        markdown_content.append("")

                    # 处理有序列表
                    elif element.name == 'ol':
                        for i, li in enumerate(element.find_all('li', recursive=False), 1):
                            markdown_content.append(f"{i}. {li.get_text()}")
                        markdown_content.append("")

                    # 处理代码块
                    elif element.name == 'pre':
                        markdown_content.append(f"\n```\n{element.get_text()}\n```\n")

                    # 处理表格
                    elif element.name == 'table':
                        for row in element.find_all('tr'):
                            cells = row.find_all(['th', 'td'])
                            markdown_content.append(
                                '| ' + ' | '.join(cell.get_text(strip=True) for cell in cells) + ' |')
                            if row.find('th'):  # 如果是表头行，添加分隔符
                                markdown_content.append('|' + '|'.join(['---' for _ in cells]) + '|')

        # 保存文件
        safe_title = clean_filename(title)
        filepath = os.path.join(section_dir, f"{safe_title}.md")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_content))

        return True, filepath

    except Exception as e:
        return False, f"{title} (Error: {str(e)})"


def scrape_postgres_docs():
    base_url = "https://www.postgresql.org/docs/current/"
    base_dir = "postgres_docs"
    successful_files = []
    failed_files = []

    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到目录结构 - 通常在toc类下
        toc = soup.find('dl', class_='toc')
        if not toc:
            print("Could not find table of contents")
            return

        # 遍历每个章节
        for dt in toc.find_all('dt'):
            section_title = dt.get_text(strip=True)
            section_dir = os.path.join(base_dir, clean_filename(section_title))
            os.makedirs(section_dir, exist_ok=True)

            print(f"\n=== Processing {section_title} ===")

            # 找到对应的dd元素，它包含子链接
            dd = dt.find_next_sibling('dd')
            if dd:
                links = dd.find_all('a')
                for link in links:
                    title = link.get_text(strip=True)
                    url = link.get('href')
                    full_url = urljoin(base_url, url)

                    print(f"Processing: {title}")
                    print(f"URL: {full_url}")
                    success, filepath = save_to_markdown(full_url, title, section_dir)

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
    successful, failed = scrape_postgres_docs()