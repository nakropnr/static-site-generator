import re
from htmlnode import HTMLNode
from markdown_to_blocks import BlockType, block_to_block_type, markdown_to_blocks
from split_node import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    child_nodes = []
    for block in block_list:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            node = code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            node = quote_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = ul_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = ol_to_html_node(block)
        else:
            node = paragraph_to_html_node(block)
        child_nodes.append(node)
    return HTMLNode("div", None, child_nodes)

def paragraph_to_html_node(block):
    # Clean up the text by replacing newlines with spaces and removing extra whitespace
    cleaned_text = " ".join(block.split())
    children = text_to_children(cleaned_text)
    node = HTMLNode("p", None, children)
    return node

def heading_to_html_node(block):
    hash_count = 0
    for char in block:
        if char == "#":
            hash_count += 1
    plain_text = re.sub(r'^#+\s*', '', block)
    children = text_to_children(plain_text)
    node = HTMLNode(f"h{hash_count}", None, children)
    return node

def code_to_html_node(block):
    content = re.sub(r'^```\n?|```$', '', block)
    lines = content.split('\n')
    cleaned_lines = [line.lstrip() for line in lines]
    cleaned_content = '\n'.join(cleaned_lines)
    text_node = TextNode(cleaned_content, TextType.TEXT)
    html_node = text_node_to_html_node(text_node)
    pre_node = HTMLNode("code", None, [html_node])
    node = HTMLNode("pre", None, [pre_node])
    return node

def quote_to_html_node(block):
    cleaned = block.lstrip("> ")
    children = text_to_children(cleaned)
    node = HTMLNode("blockquote", None, children)
    return node

def ul_to_html_node(block):
    split_lines = block.split("\n")
    li_list = []
    for line in split_lines:
        cleaned = line.lstrip("- ")
        children = text_to_children(cleaned)
        li_node = HTMLNode("li", None, children)
        li_list.append(li_node)
    node = HTMLNode("ul", None, li_list)

    return node
def ol_to_html_node(block):
    split_lines = block.split("\n")
    li_list = []
    for line in split_lines:
        cleaned = re.sub(r'^\d+\.\s*', '', line)
        children = text_to_children(cleaned)
        li_node = HTMLNode("li", None, children)
        li_list.append(li_node)
    node = HTMLNode("ol", None, li_list)

    return node

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    return html_nodes