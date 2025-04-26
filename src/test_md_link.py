import unittest
from extract_links import extract_markdown_images, extract_markdown_links
from inline_nodes import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class LinkTests(unittest.TestCase):

    def test_extract_images_basic(self):
        self.assertEqual(
            extract_markdown_images("![alt text](image.png)"),
            [("alt text", "image.png")],
        )

    def test_extract_images_multiple(self):
        self.assertEqual(
            extract_markdown_images("![a](1.png) ![b](2.png)"),
            [("a", "1.png"), ("b", "2.png")],
        )

    def test_extract_images_with_urls(self):
        self.assertEqual(
            extract_markdown_images("![logo](https://example.com/logo.png)"),
            [("logo", "https://example.com/logo.png")],
        )

    def test_extract_images_special_chars(self):
        self.assertEqual(
            extract_markdown_images("![image #1](file_1.png)"),
            [("image #1", "file_1.png")],
        )

    def test_extract_images_empty(self):
        self.assertEqual(extract_markdown_images(""), [])
        self.assertEqual(extract_markdown_images("No images here"), [])

    def test_extract_images_malformed(self):
        self.assertEqual(extract_markdown_images("![missing url]"), [])
        self.assertEqual(extract_markdown_images("![]()"), [("", "")])

    # Tests for extract_markdown_links()
    def test_extract_links_basic(self):
        self.assertEqual(
            extract_markdown_links("[link text](https://example.com)"),
            [("link text", "https://example.com")],
        )

    def test_extract_links_multiple(self):
        self.assertEqual(
            extract_markdown_links("[a](1.html) [b](2.html)"),
            [("a", "1.html"), ("b", "2.html")],
        )

    def test_extract_links_special_chars(self):
        self.assertEqual(
            extract_markdown_links("[page #1](section_1.html)"),
            [("page #1", "section_1.html")],
        )

    def test_extract_links_empty(self):
        self.assertEqual(extract_markdown_links(""), [])
        self.assertEqual(extract_markdown_links("No links here"), [])

    def test_extract_links_malformed(self):
        self.assertEqual(extract_markdown_links("[missing url]"), [])
        self.assertEqual(extract_markdown_links("[]()"), [("", "")])

    def test_differentiate_images_from_links(self):
        text = "![image](img.png) [link](page.html)"
        self.assertEqual(extract_markdown_images(text), [("image", "img.png")])
        self.assertEqual(extract_markdown_links(text), [("link", "page.html")])

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

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

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    if __name__ == "__main__":
        unittest.main()
