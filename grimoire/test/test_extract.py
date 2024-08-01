from grimoire import chunk_markdown


def test_chunk_markdown_no_headers():
    markdown = "header1"
    assert chunk_markdown(markdown) == {}


def test_chunk_markdown_one_header():
    markdown = "# header1"
    assert chunk_markdown(markdown) == {"header1": ""}


def test_chunk_markdown_one_header_with_content():
    markdown = "# header1\n some content"
    assert chunk_markdown(markdown) == {"header1": "some content"}


def test_chunk_markdown_sub_header_no_content_inbetween():
    markdown = "# header1\n ## header2\n some content"
    assert chunk_markdown(markdown) == {"header1|header2": "some content"}


def test_chunk_markdown_sub_sub_header_no_content_inbetween():
    markdown = "#header1\n ##header2\n ###header3\n some content"
    assert chunk_markdown(markdown) == {"header1|header2|header3": "some content"}


def test_chunk_markdown_two_headers():
    markdown = "#header1\n some content\n #header 2\n some content"
    assert chunk_markdown(markdown) == {
        "header1": "some content",
        "header2": "some content",
    }
