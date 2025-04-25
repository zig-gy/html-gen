import unittest

from block import markdown_to_blocks, BlockType, block_to_block_type

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