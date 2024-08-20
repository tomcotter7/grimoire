import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def chunk_lines(lines: list[str], depth: int) -> list[dict]:
    pattern = r"^(#{1," + re.escape(str(depth)) + "}) ?(.+)$"
    headers = {}
    current_section = ""
    chunks = []

    for line in lines:
        header_match = re.match(pattern, line)
        if header_match is not None:
            if current_section:  # if there is a current section, add it to the chunks
                header = "|".join([val for val in headers.values() if val])
                chunks.append({header: current_section.strip()})
                current_section = ""

            level = len(header_match.group(1))
            headers[level] = header_match.group(2)

            max_level = max(headers.keys())
            if level < max_level:
                for i in range(level + 1, max_level + 1):
                    headers[i] = ""

        elif line and headers:
            current_section += line + "\n"

    if current_section:
        header = "|".join([val for val in headers.values() if val])
        chunks.append({header: current_section.strip()})

    return chunks


def chunk_markdown(markdown: str) -> dict[str, str]:
    lines = markdown.split("\n")
    data = chunk_lines(lines, 5)
    return {k: v for d in data for k, v in d.items()}


def chunk_markdown_file(file: Path) -> dict[str, str]:
    text = open(file, "r").read()
    return chunk_markdown(text)


def chunk_multiple_markdown_files(files: list[Path]) -> dict:
    with ThreadPoolExecutor() as executor:
        results = executor.map(chunk_markdown_file, files)

    return {str(file): data for file, data in zip(files, results)}
