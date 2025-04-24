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
        
    def test_italic(self):
        node = TextNode("_Buenas_ personas", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '_', TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("Buenas", TextType.ITALIC),
            TextNode(" personas", TextType.TEXT)
        ])
        
    def test_code(self):
        node = TextNode("Codigo `cosaFea()` Fin codigo", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("Codigo ", TextType.TEXT),
            TextNode("cosaFea()", TextType.CODE),
            TextNode(" Fin codigo", TextType.TEXT)
        ])