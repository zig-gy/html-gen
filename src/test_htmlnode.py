import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "hola", props={"href":"www.hola.com", "style":"text-align: center;"})
        check = ' href="www.hola.com" style="text-align: center;"'
        self.assertEqual(node.props_to_html(), check)

    def test_not_eq(self):
        node = HTMLNode("p", "hola", props={"href":"www.hola.com", "style":"text-align: center;"})
        check = ' href="www.feo.com" style="text-align: center;"'
        self.assertNotEqual(node.props_to_html(), check)

    def test_repr(self):
        node = HTMLNode("p", "hola", props={"href":"www.hola.com", "style":"text-align: center;"})
        node2 = HTMLNode("p", "hola", props={"href":"www.hola.com", "style":"text-align: center;"})
        self.assertEqual(str(node), str(node2))
        

if __name__ == "__main__":
    unittest.main()


