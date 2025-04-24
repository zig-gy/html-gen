import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("delimiter not closed")
        if node.text_type != TextType.TEXT or len(node.text) == 0:
            new_nodes.append(node)
            continue
        new_texts = node.text.split(delimiter)
        for i, text in enumerate(new_texts):
            if text == "":
                continue
            check_uneven = 1
            if i % 2 == check_uneven:
                new_nodes.append(TextNode(text=text, text_type=text_type))
            else:
                new_nodes.append(TextNode(text=text, text_type=TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    regex = r"!\[.+?\]\(.+?\)"
    images = re.findall(regex, text)
    tups = []
    for image in images:
        url = re.search(r"(?<=\()(.+?)(?=\))", image)
        alt_text = re.search(r"(?<=\[)(.+?)(?=\])", image)
        tups.append((alt_text[0], url[0]))
    return tups

def extract_markdown_links(text):
    regex = r"\[.+?\]\(.+?\)"
    images = re.findall(regex, text)
    tups = []
    for image in images:
        url = re.search(r"(?<=\()(.+?)(?=\))", image)
        alt_text = re.search(r"(?<=\[)(.+?)(?=\])", image)
        tups.append((alt_text[0], url[0]))
    return tups
