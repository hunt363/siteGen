from htmlnode import HTMLNode
from textnode import TextNode, TextType


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value")

        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
        )

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def text_node_to_html_node(text_node: TextNode):
        match (text_node.text_type):
            case TextType.TEXT:
                return LeafNode(tag=None, value=text_node.text)
            case TextType.BOLD:
                return LeafNode(tag="b", value=text_node.text)
            case TextType.ITALIC:
                return LeafNode(tag="i", value=text_node.text)
            case TextType.CODE:
                return LeafNode(tag="code", value=text_node.text)
            case TextType.LINK:
                return LeafNode(
                    tag="a",
                    value=text_node.text,
                    props={"href": text_node.url},
                )
            case TextType.IMAGE:
                return LeafNode(
                    tag="img",
                    value="",
                    props={"src": text_node.url, "alt": text_node.text},
                )
            case _:
                raise ValueError("Invalid text type")
