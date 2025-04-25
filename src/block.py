from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered list"
    OL = "ordered list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        new_blocks.append(block)
    return new_blocks

def block_to_block_type(block):
    block = block.strip()
    if block == "":
        return BlockType.PARAGRAPH
    if block[0] == "#" and "\n" not in block:
        return BlockType.HEADING
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    if block[0] == ">":
        lines = block.split("\n")
        is_quote = True
        for line in lines:
            if line[0] != ">":
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE
    if block[:2] == "- ":
        lines = block.split("\n")
        is_ul = True
        for line in lines:
            if line[:2] != "- ":
                is_ul = False
                break
        if is_ul:
            return BlockType.UL
    if block[:3] == "1. ":
        lines = block.split("\n")
        is_ol = True
        for i, line in enumerate(lines):
            if line[:3] != f"{i+1}. ":
                is_ol = False
                break
        if is_ol:
            return BlockType.OL
    return BlockType.PARAGRAPH
