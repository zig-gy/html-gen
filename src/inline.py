from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("delimiter not closed")
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            new_texts = node.text.split(delimiter)
            if node.text[-1] == delimiter[0]:
                new_texts = new_texts[:-1]
            if node.text[0] == delimiter[0]:
                new_texts = new_texts[1:]
            for i, text in enumerate(new_texts):
                check_even = 0
                if node.text[0] != delimiter[0]:
                    check_even = 1
                    
                if i % 2 == check_even:
                    new_nodes.append(TextNode(text=text, text_type=text_type))
                else:
                    new_nodes.append(TextNode(text=text, text_type=TextType.TEXT))
    return new_nodes