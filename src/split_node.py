import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimeter, text_type):
    text_node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            text_node_list.append(old_node)
            continue

        chunks = old_node.text.split(delimeter)
        if len(chunks) % 2 == 0 or chunks == []:
            raise Exception("No closing delimiter!")
        else:
            new_node_list = []
            for i, chunk in enumerate(chunks):
                if i % 2 == 0:
                    if chunk != "":
                        new_node_list.append(TextNode(chunk, old_node.text_type))
                else:
                    if chunk != "":
                        new_node_list.append(TextNode(chunk, text_type))
                    
            text_node_list.extend(new_node_list)
    return text_node_list

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    text_node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            text_node_list.append(old_node)
            continue
        original_text = old_node.text
        img_tuples = extract_markdown_images(original_text)
        if len(img_tuples) == 0:
            text_node_list.append(old_node)
            continue
        for image in img_tuples:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                text_node_list.append(TextNode(sections[0], TextType.TEXT))
            text_node_list.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
                text_node_list.append(TextNode(original_text, TextType.TEXT))
    return text_node_list

def split_nodes_link(old_nodes):
    text_node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            text_node_list.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            text_node_list.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                text_node_list.append(TextNode(sections[0], TextType.TEXT))
            text_node_list.append(
                TextNode(
                    link[0],
                    TextType.LINK,
                    link[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
                text_node_list.append(TextNode(original_text, TextType.TEXT))
    return text_node_list

def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    bold_split = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)
    code_split = split_nodes_delimiter(italic_split, "`", TextType.CODE)
    image_split = split_nodes_image(code_split)
    link_split = split_nodes_link(image_split)
    return link_split