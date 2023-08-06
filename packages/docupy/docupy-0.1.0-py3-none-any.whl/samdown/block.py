"""Functions for turning markdown blocks into HTML elements."""

import re

def process_block(block):
    """Takes a block of Markdown and returns the correct HTML for that
    block, based on its contents."""

    block = re.sub(r"_(.*?)_", r"<u>\1</u>", block)
    block = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", block)
    block = re.sub(r"\*(.*?)\*", r"<em>\1</em>", block)

    return "<p>%s</p>" % block
