import unittest

from htmlnode import LeafNode, ParentNode


class ParentTest(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_nested_parent_nodes(self):
        inner_parent_node = ParentNode("section", [LeafNode("p", "inner content")])
        outer_parent_node = ParentNode("article", [inner_parent_node])
        self.assertEqual(
            outer_parent_node.to_html(),
            "<article><section><p>inner content</p></section></article>",
        )

    def test_to_html_with_deeply_nested_nodes(self):
        level_3_node = LeafNode("em", "deep content")
        level_2_node = ParentNode("span", [level_3_node])
        level_1_node = ParentNode("div", [level_2_node])
        root_node = ParentNode("section", [level_1_node])
        self.assertEqual(
            root_node.to_html(),
            "<section><div><span><em>deep content</em></span></div></section>",
        )

    def test_to_html_with_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode("", [LeafNode("span", "content")])

    def test_to_html_with_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [])


if __name__ == "__main__":
    unittest.main()
