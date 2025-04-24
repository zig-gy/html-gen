from htmlnode import HTMLNode
from textnode import TextNode, TextType

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag=tag, value=value, props=props)
        
    def to_html(self):
        if self.value == None:
            raise ValueError("wrong value")
        tag = ""
        closing_tag = ""
        props = ""
        if self.props != None:
            props = self.props_to_html()
        if self.tag != None:
            tag = f"<{self.tag}{props}>"
            closing_tag = f"</{self.tag}>"
        return tag + self.value + closing_tag

def text_node_to_html_node(text_node):
    text = text_node.text
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(text)
        case TextType.BOLD:
            return LeafNode(text, "b")
        case TextType.ITALIC:
            return LeafNode(text, "i")
        case TextType.CODE:
            return LeafNode(text, "code")
        case TextType.LINK:
            return LeafNode(text, "a", {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("", "img", {"src":text_node.ur, "alt":text})
