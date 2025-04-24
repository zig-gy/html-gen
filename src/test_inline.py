import unittest

from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_two_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ], matches)
    
    def test_empty_markdown_images(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)
        
    def test_no_image_markdown_images(self):
        matches = extract_markdown_images("hola buenas tardes")
        self.assertListEqual([], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
            )
    
    def test_empty_markdown_links(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)
        
    def test_no_image_markdown_links(self):
        matches = extract_markdown_links("hola buenas tardes")
        self.assertListEqual([], matches)