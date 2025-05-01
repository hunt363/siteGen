from enum import Enum

from htmlnode import LeafNode, ParentNode, text_node_to_html_node
from inline_nodes import text_to_textnodes
from htmlnode import HTMLNode, TextNode
from textnode import TextType


class BlockType(Enum):
    CODE = "```"
    QUOTE = "> "
    LIST = "- "
    ORDER = "1. "
    HEADING = ("# ", "## ", "### ", "#### ", "##### ", "######")
    TEXT = ""


def block_to_block_type(block: str):
    if block.startswith(BlockType.CODE.value) and block.endswith(BlockType.CODE.value):
        return BlockType.CODE
    elif block.startswith(BlockType.QUOTE.value):
        return BlockType.QUOTE
    elif block.startswith(BlockType.LIST.value):
        return BlockType.LIST
    elif block.startswith(BlockType.ORDER.value):
        return BlockType.ORDER
    elif block.startswith(BlockType.HEADING.value):
        return BlockType.HEADING
    else:
        return BlockType.TEXT


def markdown_to_blocks(markdown: str):
    lines = [line.strip() for line in markdown.splitlines()]

    blocks = []
    current_block = []

    for line in lines:
        if line == "":
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
        else:
            current_block.append(line)

    if current_block:
        blocks.append("\n".join(current_block))

    return blocks


def markdown_to_html_node(markdown: str, basepath: str = "/") -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.CODE:
            code_content = block.strip("`").strip()
            if "\n" in code_content and not code_content.endswith("\n"):
                code_content += "\n"
            code_leaf = LeafNode(tag="code", value=code_content)
            pre_node = ParentNode(tag="pre", children=[code_leaf])
            block_nodes.append(pre_node)

        elif block_type == BlockType.QUOTE:
            quote_text = "\n".join(line.lstrip("> ") for line in block.splitlines())
            quote_nodes = [
                text_node_to_html_node(node) for node in text_to_textnodes(quote_text)
            ]
            block_nodes.append(ParentNode(tag="blockquote", children=quote_nodes))

        elif block_type == BlockType.LIST:
            list_items = []
            for line in block.splitlines():
                item_text = line.lstrip("- ").strip()
                item_nodes = [
                    text_node_to_html_node(node)
                    for node in text_to_textnodes(item_text)
                ]
                list_items.append(ParentNode(tag="li", children=item_nodes))
            block_nodes.append(ParentNode(tag="ul", children=list_items))

        elif block_type == BlockType.ORDER:
            list_items = []
            for line in block.splitlines():
                # Remove "1. " etc
                item_text = line[line.find(".") + 1 :].strip()
                item_nodes = [
                    text_node_to_html_node(node)
                    for node in text_to_textnodes(item_text)
                ]
                list_items.append(ParentNode(tag="li", children=item_nodes))
            block_nodes.append(ParentNode(tag="ol", children=list_items))

        elif block_type == BlockType.HEADING:
            # Count number of '#' characters
            heading_level = 0
            for char in block:
                if char == "#":
                    heading_level += 1
                else:
                    break
            heading_text = block.lstrip("#").strip()
            heading_nodes = [
                text_node_to_html_node(node) for node in text_to_textnodes(heading_text)
            ]
            block_nodes.append(
                ParentNode(tag=f"h{heading_level}", children=heading_nodes)
            )

        else:  # BlockType.TEXT
            block_text = block.replace("\n", " ")
            text_nodes = [
                text_node_to_html_node(node) for node in text_to_textnodes(block_text)
            ]
            block_nodes.append(ParentNode(tag="p", children=text_nodes))

    return ParentNode(tag="div", children=block_nodes)


# def markdown_to_html(markdown: str):
#     blocks = markdown_to_blocks(markdown)
#     for block in blocks:
#         block_type = block_to_block_type(block)


# def text_to_children(text: str):
#     nodes = text_to_textnodes(text)
#     for node in nodes:
#         node = text_node_to_html_node(node)
