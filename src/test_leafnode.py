import unittest

from leafnode import LeafNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode(tag="a", value="Link", props={"href":"www.hola.com"})
        self.assertEqual(node.to_html(), '<a href="www.hola.com">Link</a>')

    def test_leaf_to_b(self):
        node = LeafNode(tag="b", value="Bold text")
        self.assertEqual(node.to_html(), "<b>Bold text</b>")

    def test_leaf_to_no_tag(self):
        node = LeafNode(value="Hola")
        self.assertEqual(node.to_html(), "Hola")
        
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "www.hola.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
