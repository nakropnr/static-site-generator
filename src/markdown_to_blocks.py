import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    block_split =markdown.split("\n\n")
    strip_blocks = []
    for i in range(len(block_split)):
        strip_block = block_split[i].strip()
        if strip_block != "":
            strip_blocks.append(strip_block)
    return strip_blocks

def block_to_block_type(block):
    # print(f"DEBUG: Block being checked: {repr(block)}")
    hash_count = 0
    for char in block:
        if char == "#":
            hash_count += 1
        else:
            # if char == " ":
            #     print(f"DEBUG: Found space, hash_count={hash_count}, condition={(hash_count >= 1 and hash_count <= 6)}")

            if (hash_count >= 1 and hash_count <= 6) and char == " ":
                print("DEBUG: Returning HEADING")
                return BlockType.HEADING
            break
    if block.startswith("```") and block.rstrip().endswith("```"):
        # print("DEBUG: Code block condition matched!")
        # print("DEBUG: Returning CODE")
        return BlockType.CODE
    if all(line.startswith(">") for line in block.splitlines()):
        return BlockType.QUOTE
    lines = block.splitlines()
    if all(line.startswith("- ") or line.startswith("* ") for line in lines):
        return BlockType.UNORDERED_LIST
    if block.startswith("1."):
        lines = block.splitlines()
        for i, line in enumerate(lines, 1):
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    