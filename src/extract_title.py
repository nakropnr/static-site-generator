import os
from markdown_to_html import markdown_to_html_node


def extract_title(markdown):
    if markdown.startswith("#"):
        extracted = markdown.strip("# ")
    else:
        raise Exception("Not header!")
    return extracted

