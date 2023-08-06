"""This module contains for functions for parsing markdown."""

import re

def markdown_to_html(markdown, paths=None):
    """Takes a string in markdown, and converts it to HTML. There must be two
    line breaks between separate blocks.

    :param str markdown: The maekdown to convert.
    :param dict paths: If given, any paths will be replaced using this lookup.
    :rtype: ``str``"""

    blocks = text_to_blocks(markdown)
    html_blocks = [block_to_html(block, paths=paths) for block in blocks]
    return "\n".join(html_blocks)


def text_to_blocks(text):
    """Breaks a string into a list of blocks, using double line breaks.
    Windows line breaks (``\\r\\n``) are supported.

    :param str text: The string to break up.
    :rtype: ``list``"""

    blocks = text.replace("\r\n", "\n").split("\n\n")
    blocks = [block.strip().replace("\n", " ") for block in blocks]
    blocks = list(filter(bool, blocks))
    return blocks


def block_to_html(block, paths=None):
    """Converts a markdown block to its HTML equivalent.

    :param str block: The block to convert.
    :param dict paths: If given, any paths will be replaced using this lookup.
    :rtype: ``str``"""

    substituted_characters = []
    html = ""
    while "\\" in block:
        location = block.find("\\")
        if location != len(block) - 1:
            substituted_characters.append(block[location + 1])
            block = block[:location] + "\x1A" + block[location + 2:]
        else:
            block = block[:-1]
    if block[0] == "!" or block[0] == "#":
        html = create_special_html(block, paths=paths)
    else:
        html = create_paragraph_html(block)
    for char in substituted_characters:
        html = html.replace("\x1A", char, 1)
    return html


def create_special_html(block, paths=None):
    """Converts a special markdown block to its HTML equivalent. That is,
    images, videos, and YouTube blocks.

    :param str block: The block to convert.
    :param dict paths: If given, any paths will be replaced using this lookup.
    :rtype: ``str``"""

    if block[0] == "#":
        start = re.search(r"[^#]", block).start()
        level = block[:start].count("#")
        return "<h{}>{}</h{}>".format(level, block[start:].strip(), level)
    else:
        if re.compile(r"\[(.*?)\]\((.*?)\)").match(block[1:]):
            path = re.compile(r"\[(.*?)\]\((.*?)\)").findall(block[1:])[0][1]
            if paths: path = paths.get(path, "")
            return re.sub(
             r"\[(.*?)\]\((.*?)\)",
             r'<figure><img src="{}" title="\1"></figure>'.format(path),
             block[1:]
            )
        elif re.compile(r"\((.*?)\)").match(block[1:]):
            path = re.compile(r"\((.*?)\)").findall(block[1:])[0]
            if paths: path = paths.get(path, "")
            return '<video src="{}" controls></video>'.format(path)
        elif re.compile(r"\{(.*?)\}").match(block[1:]):
            return re.sub(
             r"\{(.*?)\}",
             r'<div class="youtube"><iframe src="//www.youtube.com/embed'
             r'/\1/" frameborder="0" allowfullscreen></iframe></div>',
             block[1:]
            )
    return ""


def create_paragraph_html(block):
    """Converts a paragraph markdown block to its HTML equivalent.

    :param str block: The block to convert.
    :param dict paths: If given, any paths will be replaced using this lookup.
    :rtype: ``str``"""

    block = re.sub(
     r"\{(.*?)\}\((.*?)\)", r'<a href="\2" target="_blank">\1</a>', block
    )
    block = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', block)
    block = re.sub(r"\~\~(.*?)\~\~", r"<del>\1</del>", block)
    block = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", block)
    block = re.sub(r"\*(.*?)\*", r"<em>\1</em>", block)
    return "<p>{}</p>".format(block)
