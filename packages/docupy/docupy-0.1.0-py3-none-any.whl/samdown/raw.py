from .block import process_block

"""Functions for processing raw markdown."""

def split(raw_text):
    """Takes a chunk of raw markdown and splits it into blocks.

    :param str raw_text: The raw markdown.
    :rtype: ``list``"""

    return raw_text.replace("\r\n", "\n").split("\n\n")


def html_from_markdown(markdown):
    """Converts markdown text into HTML.

    :param str markdown: The markdown text to convert to HTML.
    :rtype: ``str``"""
    
    return "\n".join([process_block(block) for block in split(markdown)])
