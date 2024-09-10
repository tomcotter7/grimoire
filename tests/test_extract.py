from pathlib import Path
from unittest.mock import mock_open, patch

from grimoire import chunk_markdown, chunk_multiple_markdown_files


def test_chunk_markdown_no_headers():
    markdown = "header1"
    assert chunk_markdown(markdown) == {}


def test_chunk_markdown_one_header():
    markdown = "# header1"
    assert chunk_markdown(markdown) == {}


def test_chunk_markdown_one_header_with_content():
    markdown = "# header1\n some content"
    assert chunk_markdown(markdown) == {"header1": "some content"}


def test_chunk_markdown_sub_header_no_content_inbetween():
    markdown = "# header1\n## header2\n some content"
    assert chunk_markdown(markdown) == {"header1|header2": "some content"}


def test_chunk_markdown_sub_sub_header_no_content_inbetween():
    markdown = "# header1\n## header2\n### header3\n some content"
    output = chunk_markdown(markdown)
    print(output)
    assert output == {"header1|header2|header3": "some content"}


def test_chunk_markdown_two_headers():
    markdown = "# header1\nsome content\n# header2\n some content"
    assert chunk_markdown(markdown) == {
        "header1": "some content",
        "header2": "some content",
    }


def test_chunk_markdown_sub_header_content_inbetween():
    markdown = (
        "# header1\n some content\n## header2\n some content\n# header3\n some content"
    )
    assert chunk_markdown(markdown) == {
        "header1": "some content",
        "header1|header2": "some content",
        "header3": "some content",
    }


def test_chunk_markdown_sub_sub_header_content_inbetween():
    markdown = "# header1\n some content1\n## header2\n some content2\n### header3\n some content3\n# header4\n some content4\n## header5\n some content5"
    assert chunk_markdown(markdown) == {
        "header1": "some content1",
        "header1|header2": "some content2",
        "header1|header2|header3": "some content3",
        "header4": "some content4",
        "header4|header5": "some content5",
    }


@patch("builtins.open", new_callable=mock_open, read_data="# header1\n some content1")
def test_chunk_multiple_markdown_files(open_mock):
    files = [Path(f"file{i}.md") for i in range(1, 4)]
    output = chunk_multiple_markdown_files(files)
    expected_output = {
        "file1.md": {"header1": "some content1"},
        "file2.md": {"header1": "some content1"},
        "file3.md": {"header1": "some content1"},
    }

    assert output == expected_output
