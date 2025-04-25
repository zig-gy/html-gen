import unittest

from block import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node

class TestBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_block_to_block_type_heading(self):
        block = "# Hola"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_block_to_block_type_code(self):
        block = """
```
string = "Hola Mundo!"
print(string)
```
"""
        # print("code",block[0:4], block[-3:])v
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = """
> Hola
> Mundo
> bonito
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)
        
    def test_block_to_block_type_ul(self):
        block = """
- buenas
- tardes
- cabros
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UL)
        
    def test_block_to_block_type_ol(self):
        block = """
1. Primero
2. Segundo
3. Tercero
"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.OL)
        
    def test_block_to_block_type_paragraph(self):
        block = "Holas"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_wrong_ol(self):
        block = """
1. Primero
4. Segundo
3. Tercero
"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.OL)
        
    def test_block_to_block_type_missing_quote(self):
        block = """
> Hola
 Mundo
> bonito
"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.QUOTE)
    
    def test_block_to_block_type_wrong_ul(self):
        block = """
- buenas
 tardes
- cabros
"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.UL)
        
    def test_block_to_block_type_mixed_list(self):
        block = """
1. Item one
- Item two
3. Item three
"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.OL)
        self.assertNotEqual(block_type, BlockType.UL)

    def test_block_to_block_type_empty_block(self):
        block = ""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_whitespace_block(self):
        block = "   "
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_multiline_heading(self):
        block = """
# Heading
Another line
"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_code_with_extra_characters(self):
        block = """
```
hola
```
djakld
"""
        block_type = block_to_block_type(block)
        self.assertNotEqual(block_type, BlockType.CODE)
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )

    def test_blockquote(self):
        md = """
> This is a blockquote
> with multiple lines
> and **formatting**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote with multiple lines and <b>formatting</b></blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2 with **bold**
- Item 3 with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2 with <b>bold</b></li><li>Item 3 with <code>code</code></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second item with _italic_
3. Third item
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <i>italic</i></li><li>Third item</li></ol></div>",
        )

    def test_mixed_content(self):
        md = """
# Main Heading

This is a paragraph with **bold** text.

## Subheading

- List item 1
- List item 2

> A blockquote with some _italic_ text
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main Heading</h1><p>This is a paragraph with <b>bold</b> text.</p><h2>Subheading</h2><ul><li>List item 1</li><li>List item 2</li></ul><blockquote>A blockquote with some <i>italic</i> text</blockquote></div>",
        )

    def test_empty_input(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")