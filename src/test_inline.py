import unittest

from inline import split_nodes_delimiter
from textnode import TextNode, TextType

class TestInline(unittest.TestCase):
    
    def test_bold(self):
        node = TextNode("Hola **cabros**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("Hola ", TextType.TEXT),
            TextNode("cabros", TextType.BOLD)
        ])