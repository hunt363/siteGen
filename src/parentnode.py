from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if tag is None:
            raise ValueError("ParentNode must have a tag")
        if children is None:
            raise ValueError("ParentNode must have children (can be empty list)")
        if not isinstance(children, list):
            raise TypeError("Children must be a list")
        for child in children:
            if not hasattr(child, "to_html") or not callable(child.to_html):
                raise TypeError("Each child must implement to_html()")

        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None:
            raise ValueError("ParentNode must have children")
        return (
            f"<{self.tag}>"
            + "".join(child.to_html() for child in self.children)
            + f"</{self.tag}>"
        )

    def __eq__(self, other):
        if not isinstance(other, ParentNode):
            return False
        return (
            self.tag == other.tag
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
