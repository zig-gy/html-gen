from enum import Enum

from parentnode import ParentNode
from leafnode import LeafNode, text_node_to_html_node
from inline import text_to_nodes
from textnode import TextNode, TextType
from inline import text_to_nodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered list"
    OL = "ordered list"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        type_of_block = block_to_block_type(block)
        if type_of_block == BlockType.PARAGRAPH:
            text = text_to_children(block)
            node = ParentNode("p", children=text)
            html_nodes.append(node)
        elif type_of_block == BlockType.HEADING:
            counted_pound = block[:7].count("#")
            clean_text = block.lstrip("# ")
            text = text_to_children(clean_text)
            node = ParentNode(f"h{counted_pound}", children=text)
            html_nodes.append(node)
        elif type_of_block == BlockType.CODE:
            code = block.strip("`").lstrip("\n")
            inner_node = text_node_to_html_node(TextNode(code,TextType.CODE))
            node = ParentNode("pre", children=[inner_node])
            html_nodes.append(node)
        elif type_of_block == BlockType.UL:
            list_items = create_html_list_items(block)
            node = ParentNode("ul", children=list_items)
            html_nodes.append(node)
        elif type_of_block == BlockType.OL:
            list_items = create_html_list_items(block)
            node = ParentNode("ol", children=list_items)
            html_nodes.append(node)
        elif type_of_block == BlockType.QUOTE:
            new_block = clean_quote(block)
            text = text_to_children(new_block)
            node = ParentNode("blockquote", children=text)
            html_nodes.append(node)
    return ParentNode("div",children=html_nodes)
            
            
def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type_of_block = block_to_block_type(block)
        if type_of_block == BlockType.HEADING:
            clean_text = block.lstrip("# ")
            return clean_text.strip()

def text_to_children(text):
    new_text = text.split("\n")
    new_text = " ".join(new_text)
    nodes = text_to_nodes(new_text)
    children = list(map(text_node_to_html_node, nodes))
    return children

def clean_quote(text):
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        new_lines.append(line.lstrip("> "))
    return "\n".join(new_lines)

def create_html_list_items(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        clean_line = line.lstrip("- .123456789")
        text = text_to_children(clean_line)
        node = ParentNode("li", text)
        children.append(node)
    return children
        
    
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
    if block.startswith(("#","##","###","####","#####","######")) and "\n" not in block:
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
