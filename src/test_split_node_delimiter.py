import unittest
from inline_nodes import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):

    # Test with backticks as code delimiters
    def test_split_simple(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_multiple_code_blocks(self):
        node = TextNode("Start `code1` middle `code2` end", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("code1", TextType.CODE),
                TextNode(" middle ", TextType.TEXT),
                TextNode("code2", TextType.CODE),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_split_no_delimiters(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("Just plain text", TextType.TEXT),
            ],
        )

    def test_split_empty_string(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [])

    # Adjusted to handle empty delimiters as TextType.CODE
    def test_split_only_delimiters(self):
        node = TextNode("``", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [],
        )

    def test_split_starts_ends_with_delimiter(self):
        node = TextNode("`start` middle `end`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("start", TextType.CODE),
                TextNode(" middle ", TextType.TEXT),
                TextNode("end", TextType.CODE),
            ],
        )

    def test_ignores_non_text_nodes(self):
        node1 = TextNode("Some text", TextType.TEXT)
        node2 = TextNode("Ignore this", TextType.CODE)
        result = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("Some text", TextType.TEXT),
                TextNode("Ignore this", TextType.CODE),
            ],
        )

    # New tests using **bold** delimiter and TextType.BOLD

    def test_split_bold_text(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_multiple_bold_blocks(self):
        node = TextNode("Start **bold1** middle **bold2** end", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("bold1", TextType.BOLD),
                TextNode(" middle ", TextType.TEXT),
                TextNode("bold2", TextType.BOLD),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_split_single_unmatched_bold_delimiter_start(self):
        node = TextNode("Here is a ** lonely bold delimiter.", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_single_unmatched_bold_delimiter_end(self):
        node = TextNode("Here is a lonely bold delimiter**.", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    # New tests using _italic_ delimiter and TextType.ITALIC

    def test_split_italic_text(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_multiple_italic_blocks(self):
        node = TextNode("Start _italic1_ middle _italic2_ end", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            result,
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("italic1", TextType.ITALIC),
                TextNode(" middle ", TextType.TEXT),
                TextNode("italic2", TextType.ITALIC),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_split_single_unmatched_italic_delimiter_start(self):
        node = TextNode("Here is a _ lonely italic delimiter.", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_split_single_unmatched_italic_delimiter_end(self):
        node = TextNode("Here is a lonely italic delimiter_.", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "_", TextType.ITALIC)


if __name__ == "__main__":
    unittest.main()
