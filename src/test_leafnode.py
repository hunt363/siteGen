import unittest
from htmlnode import LeafNode
from textnode import TextNode, TextType


class LeafTest(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode(tag="p", value="Hello, world!")
        # print(node.to_html())
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = LeafNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_text(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = LeafNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic_text(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = LeafNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code_text(self):
        node = TextNode("Code snippet", TextType.CODE)
        html_node = LeafNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet")

    def test_link_text(self):
        node = TextNode("Click here", TextType.LINK, url="https://example.com")
        html_node = LeafNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image_text(self):
        node = TextNode(
            "Image description", TextType.IMAGE, url="https://example.com/image.png"
        )
        html_node = LeafNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/image.png", "alt": "Image description"},
        )

    def test_invalid_text_type(self):
        with self.assertRaises(ValueError):
            node = TextNode("Invalid type", None)
            LeafNode.text_node_to_html_node(node)

    def test_leaf_to_html_b(self):
        node = LeafNode(value="Hello, world!")
        # print(node.to_html())
        self.assertEqual(node.to_html(), "Hello, world!")


if __name__ == "__main__":
    unittest.main()
