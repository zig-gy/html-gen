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
            if i % 2 == 0:
                new_nodes.append(TextNode(text=text, text_type=TextType.TEXT))
            else:
                new_nodes.append(TextNode(text=text, text_type=text_type))
    return new_nodes

def extract_markdown_images(text):
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    images = re.findall(regex, text)
    return images

def extract_markdown_links(text):
    regex = r"(?<!\!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    images = re.findall(regex, text)
    return images

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        image_strings = extract_markdown_images(node.text)
        if node.text_type != TextType.TEXT or len(image_strings) == 0:
            new_nodes.append(node)
            continue
        node_text = node.text
        for image_string in image_strings:
            new_texts = node_text.split(f"![{image_string[0]}]({image_string[1]})", 1)
            # print(new_texts)
            if new_texts[0] != "":
                new_nodes.append(TextNode(new_texts[0], TextType.TEXT))
            new_nodes.append(TextNode(image_string[0], TextType.IMAGE, image_string[1]))
            if len(new_texts) > 1:    
                node_text = new_texts[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        link_strings = extract_markdown_links(node.text)
        if node.text_type != TextType.TEXT or len(link_strings) == 0:
            new_nodes.append(node)
            continue
        node_text = node.text
        for link_string in link_strings:
            new_texts = node_text.split(f"[{link_string[0]}]({link_string[1]})", 1)
            # print(new_texts)
            if new_texts[0] != "":
                new_nodes.append(TextNode(new_texts[0], TextType.TEXT))
            new_nodes.append(TextNode(link_string[0], TextType.LINK, link_string[1]))
            if len(new_texts) > 1:
                node_text = new_texts[1]
        if node_text != "":
            new_nodes.append(TextNode(node_text, TextType.TEXT))
    return new_nodes