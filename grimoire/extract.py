def chunk_markdown(markdown: str) -> dict[str, str]:
    if "#" not in markdown:
        return {}

    headers = []
    content = ""
    for line in markdown.split("\n"):
        line = line.strip()
        if line.startswith("#"):
            headers.append(line.strip("# "))
        else:
            content += line.strip()

    return {"|".join(headers): content}
