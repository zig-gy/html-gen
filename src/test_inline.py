import unittest

from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_nodes
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
        
    def test_image_passed_to_link(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)
        
    def test_image_and_link_passed_to_link(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), and this is a link [link](www.hola.com)"
        )
        self.assertListEqual([("link", "www.hola.com")], matches)
        
    def test_image_and_link_passed_to_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), and this is a link [link](www.hola.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_no_split_image(self):
        node = TextNode("Hola", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
        
    def test_text_after_image(self):
        node = TextNode(
            "This is an ![image](www.hola.com) and another ![imagey](www.chao.com) xd",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        # print(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "www.hola.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("imagey", TextType.IMAGE, "www.chao.com"),
                TextNode(" xd", TextType.TEXT)
            ],
            new_nodes
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is a [link](www.hola.com) and another [linky](www.chao.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.hola.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("linky", TextType.LINK, "www.chao.com")
            ],
            new_nodes
        )
        
    def test_no_split_links(self):
        node = TextNode("Hola", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)
        
    def test_text_after_link(self):
        node = TextNode(
            "This is a [link](www.hola.com) and another [linky](www.chao.com) xd",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        # print(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.hola.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("linky", TextType.LINK, "www.chao.com"),
                TextNode(" xd", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_links_with_no_closing_parenthesis(self):
        node = TextNode(
            "This is a [link](www.hola.com and another [linky](www.chao.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a [link](www.hola.com and another ", TextType.TEXT),
                TextNode("linky", TextType.LINK, "www.chao.com")
            ],
            new_nodes
        )

    def test_split_images_with_no_closing_parenthesis(self):
        node = TextNode(
            "This is an ![image](www.hola.com and another ![imagey](www.chao.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is an ![image](www.hola.com and another ", TextType.TEXT),
                TextNode("imagey", TextType.IMAGE, "www.chao.com")
            ],
            new_nodes
        )

    def test_split_links_and_images_combined(self):
        node = TextNode(
            "This is a [link](www.hola.com) and an ![image](www.image.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.hola.com"),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "www.image.com")
            ],
            new_nodes
        )

    def test_split_images_with_multiple_identical_images(self):
        node = TextNode(
            "This is an ![image](www.hola.com) and another ![image](www.hola.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "www.hola.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "www.hola.com")
            ],
            new_nodes
        )

    def test_split_links_with_multiple_identical_links(self):
        node = TextNode(
            "This is a [link](www.hola.com) and another [link](www.hola.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.hola.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.hola.com")
            ],
            new_nodes
        )
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_nodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

    def test_only_text_text_to_textnodes(self):
        text = "Hola mundo!"
        nodes = text_to_nodes(text)
        self.assertEqual(nodes, [
            TextNode("Hola mundo!", TextType.TEXT)
        ])