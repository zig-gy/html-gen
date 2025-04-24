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
        
    def test_two_bold(self):
        node = TextNode("**Bold 1** y tambien **Bold 2**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("Bold 1", TextType.BOLD),
            TextNode(" y tambien ", TextType.TEXT),
            TextNode("Bold 2", TextType.BOLD)
        ])
        
    def test_list_of_text(self):
        node = TextNode("Hola buenas _tardes_ muchachos, ¿como estan?", TextType.TEXT)
        node2 = TextNode("Buenas _tardes_ señorita.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], '_', TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("Hola buenas ", TextType.TEXT),
            TextNode("tardes", TextType.ITALIC),
            TextNode(" muchachos, ¿como estan?", TextType.TEXT),
            TextNode("Buenas ", TextType.TEXT),
            TextNode("tardes", TextType.ITALIC),
            TextNode(" señorita.", TextType.TEXT)
        ])
        
    def test_non_closing_delimiter(self):
        node = TextNode("Esto **no", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(str(context.exception), "delimiter not closed")
            
    def test_mixed_delimiters(self):
        node = TextNode("Hola **mundo** _lindo_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("Hola ", TextType.TEXT),
            TextNode("mundo", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("lindo", TextType.ITALIC),
        ])
        
    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes, [node])
        
    def test_no_delimiters(self):
        node = TextNode("Texto sin delimitadores", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(new_nodes, [node])
        
    def test_multiple_nodes_with_mixed_delimiters(self):
        node1 = TextNode("Hola **mundo**", TextType.TEXT)
        node2 = TextNode("_lindo_ dia", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], '**', TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("Hola ", TextType.TEXT),
            TextNode("mundo", TextType.BOLD),
            TextNode("lindo", TextType.ITALIC),
            TextNode(" dia", TextType.TEXT),
        ])