import unittest
from block_nodes import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)
from inline_nodes import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def assertTextNodeListsEqual(self, list1, list2):
        self.assertEqual(len(list1), len(list2))
        for node1, node2 in zip(list1, list2):
            self.assertEqual(node1.text, node2.text)
            self.assertEqual(node1.text_type, node2.text_type)
            self.assertEqual(node1.url, node2.url)

    def test_plain_text(self):
        text = "Just plain text"
        result = text_to_textnodes(text)
        expected = [TextNode("Just plain text", TextType.TEXT)]
        self.assertTextNodeListsEqual(result, expected)

    def test_bold_text(self):
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertTextNodeListsEqual(result, expected)

    def test_italic_text(self):
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertTextNodeListsEqual(result, expected)

    def test_code_text(self):
        text = "This is `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertTextNodeListsEqual(result, expected)

    def test_image(self):
        text = "This has an ![image](img.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This has an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.png"),
        ]
        self.assertTextNodeListsEqual(result, expected)

    def test_link(self):
        text = "This has a [link](url.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This has a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        self.assertTextNodeListsEqual(result, expected)

    def test_combined_markdown(self):
        text = (
            "This is **bold**, _italic_, `code`, ![image](img.png), and [link](url.com)"
        )
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "img.png"),
            TextNode(", and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url.com"),
        ]
        self.assertTextNodeListsEqual(result, expected)

    # def test_nested_markdown(self):
    #     text = "This is **bold with _italic_** and `code`"
    #     result = text_to_textnodes(text)
    #     expected = [
    #         TextNode("This is ", TextType.TEXT),
    #         TextNode("bold with ", TextType.BOLD),
    #         TextNode("italic", TextType.ITALIC),
    #         TextNode(" and ", TextType.TEXT),
    #         TextNode("code", TextType.CODE),
    #     ]
    #     self.assertTextNodeListsEqual(result, expected)

    def test_empty_text(self):
        text = ""
        result = text_to_textnodes(text)
        expected = []
        self.assertTextNodeListsEqual(result, expected)

    def test_multiple_spaces(self):
        text = "This  has   extra   spaces"
        result = text_to_textnodes(text)
        expected = [TextNode("This  has   extra   spaces", TextType.TEXT)]
        self.assertTextNodeListsEqual(result, expected)

    def test_unclosed_delimiter(self):
        text = "This has **unclosed bold"
        with self.assertRaises(Exception):
            text_to_textnodes(text)

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

    def test_markdown_to_blocks_single_paragraph(self):
        md = "This is a simple paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a simple paragraph."])

    def test_markdown_to_blocks_multiple_paragraphs(self):
        md = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, ["First paragraph.", "Second paragraph.", "Third paragraph."]
        )

    def test_markdown_to_blocks_paragraph_with_multiple_lines(self):
        md = "This is the first line.\nThis is the second line.\n\nNew block starts here."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is the first line.\nThis is the second line.",
                "New block starts here.",
            ],
        )

    def test_markdown_to_blocks_list_block(self):
        md = "- Item 1\n- Item 2\n- Item 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["- Item 1\n- Item 2\n- Item 3"])

    def test_markdown_to_blocks_leading_and_trailing_spaces(self):
        md = "   Paragraph with spaces.   \n\n    Another one.   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Paragraph with spaces.", "Another one."])

    def test_markdown_to_blocks_extra_blank_lines(self):
        md = "\n\nFirst block.\n\n\n\nSecond block after extra newlines.\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block.", "Second block after extra newlines."])

    def test_markdown_to_blocks_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_whitespace(self):
        md = "   \n  \n\n\n  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_code_block(self):
        block = "```\nprint('Hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_list_block(self):
        block = "- This is a list item."
        self.assertEqual(block_to_block_type(block), BlockType.LIST)

    def test_ordered_list_block(self):
        block = "1. First item in ordered list."
        self.assertEqual(block_to_block_type(block), BlockType.ORDER)

    def test_heading_block(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_plain_text_block(self):
        block = "This is just a paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.TEXT)

    def test_incomplete_code_block(self):
        block = "```print('missing end delimiter')"
        self.assertEqual(block_to_block_type(block), BlockType.TEXT)

    def test_multiple_hashes_heading(self):
        block = "### Sub-heading level 3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_non_matching_list(self):
        block = "* Not a markdown list according to our BlockType"
        self.assertEqual(block_to_block_type(block), BlockType.TEXT)

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

    if __name__ == "__main__":
        unittest.main()
