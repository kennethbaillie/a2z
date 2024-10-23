import re

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_markdown_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def sort_by_headers(content):
    # Split the content by top-level headers (#)
    sections = re.split(r'(^# .+$)', content, flags=re.MULTILINE)
    
    # Every section will be a header followed by its content, so group them in pairs
    section_pairs = [(sections[i], sections[i+1]) for i in range(1, len(sections), 2)]
    
    # Sort sections by their headers (case-insensitive)
    section_pairs_sorted = sorted(section_pairs, key=lambda pair: pair[0].lower())
    
    # Reassemble the sorted sections back into a single string
    sorted_content = sections[0]  # The initial part before the first header, if any
    for header, body in section_pairs_sorted:
        sorted_content += header + body
    
    return sorted_content

def main(file_path):
    content = read_markdown_file(file_path)
    sorted_content = sort_by_headers(content)
    write_markdown_file(file_path, sorted_content)
    print(f"File '{file_path}' sorted successfully by top-level headers.")

if __name__ == "__main__":
    file_path = "a2z.md"  # Replace with your file path
    main(file_path)
