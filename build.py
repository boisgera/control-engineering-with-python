#!/usr/bin/env python

# Python 3 Standard Library
import copy
import json
import os.path
import sys

# Pandoc
import pandoc
from pandoc.types import *


# ------------------------------------------------------------------------------
# TODO: reconsider all flags wrt use cases and simplification of the document.
# Consider:
#   - slides and slides + hidden? (aka setup code need for proper display
#     of the slides ?)

# TODO: the div removal filters off the 'notes' and thus borks speaker notes.

__doc__ = """

flags:

  - target: hidden, slides, notebook or no flag (both targets)

    'hidden' is "exec-only", the nitty-gritty stuff that won't appear anywhere,
    but is necessary for some side effects such as generating images used by
    the slides. This is a "slides setup" option ... require slides to be
    added to this list of classes at the same time? (more explicit)

    'slides' won't appear in the notebook, but in the slides, and it's
    also executed

    'notebook' is not executed and appears only in the notebook.

"""

# Source Document
# ------------------------------------------------------------------------------
doc_file = sys.argv[-1]  # some markdown document
doc_name = os.path.splitext(doc_file)[0]
doc = pandoc.read(file=doc_file)

# Code Execution
# ------------------------------------------------------------------------------
# TODO: make a single function that gathers the code that need to be executed
# (filter off non-executable divs and code blocks at the same time).
# That would be handy to flag some small portions of the documents as
# slides-only, such as images, without a big div wrap.


def exec_code(doc):
    """
    Execute all code blocks not flagged as "notebook" (and not in "notebook" div).
    """
    doc = copy.deepcopy(doc)

    root = doc[1]  # top-level blocks (Pandoc(Meta, [Block]))

    # Locate the divs and extract the relevant data
    divs = []
    for index, elt in enumerate(root):  # top-level divs only
        if isinstance(elt, Div):
            div = elt
            attr, blocks = div[:]  # Div(Attr, [Block])
            classes = attr[1]  # Attr = (Text, [Text], [(Text, Text)])

            if "notebook" in classes:
                divs.append((index, blocks))

    # Reverse document order is needed not to invalidate
    # the remaining matches indices.
    for index, blocks in reversed(divs):
        del root[index]  # remove the div

    src = ""
    for elt in pandoc.iter(doc):
        if isinstance(elt, CodeBlock):
            code = elt
            attr, text = code[:]  # CodeBlock(Attr, Text)
            _, classes, _ = attr[:]  # Attr = (Text, [Text], [(Text, Text)])
            if "notebook" not in classes:
                src += text + "\n"
    with open(".tmp.py", "w") as output:
        output.write(src)
    exec(src, {"__file__": __file__})


if "--fast" not in sys.argv:
    exec_code(doc)

# Document Filter
# ------------------------------------------------------------------------------
# TODO: great stuff, why not used yet ?!? Ah I see because the concrete
# operations not only remove but unpack stuff or delete. So we need a
# replace rather than a remove.
def remove(doc, needs_removal):
    "Selected Content Removal - Two-pass Algorithm"

    doc = copy.deepcopy(doc)  # the removal is actually in-place,
    # but the user of this function should not worry about that.

    # Locate the divs and extract the relevant data
    matches = []
    for elt, path in pandoc.iter(doc, path=True):
        if needs_removal(elt):
            parent, index = path[-1]
            matches.append((parent, index))

    # Reverse document order is needed not to invalidate
    # the remaining matches indices.
    for parent, index in reversed(matches):
        del parent[index]

    return doc


# Slides Generation
# ------------------------------------------------------------------------------
def make_slides_doc(doc):
    doc = copy.deepcopy(doc)  # the transformation is actually in-place,
    # but the user of this function should not worry about that.

    root = doc[1]  # top-level blocks

    # Locate the divs and extract the relevant data
    divs = []
    for index, elt in enumerate(root):  # top-level divs only
        if isinstance(elt, Div):
            div = elt
            attr, blocks = div[:]  # Div(Attr, [Block])
            classes = attr[1]  # Attr = (Text, [Text], [(Text, Text)])

            if "hidden" in classes or "notebook" in classes:
                divs.append(("remove", index, blocks))
            elif "notes" not in classes:  # don't remove the speaker notes wrapper.
                divs.append(("unpack", index, blocks))

    # Reverse document order is needed not to invalidate
    # the remaining matches indices.
    for action, index, blocks in reversed(divs):
        del root[index]
        if action == "unpack":
            root[index:index] = blocks

    return doc


slides_doc = make_slides_doc(doc)

options = ["--standalone", "-V", "theme:white", "--mathjax", "-V", "slideNumber:true"]

pandoc.write(slides_doc, file=doc_name + ".html", format="revealjs", options=options)

# Notebook Generation
# ------------------------------------------------------------------------------

# Two issues here: for one some Header stuff flagged 'slides'
# should be removed from the notebook output but isn't. Mmmmmm shit.
# Second, deeper issue: Headers are NOT the holders of the elements
# that follow, so the algorithm needs to be smarter and identify the
# corresponding content.
# For now, short term: squash two issues by using only divs in the
# document to deal with conditional content.
# Ouch: the reveal target doesn't like divs very much (overlap
# and / or no newpage). Can we solve this by unpacking slides divs ?


def make_notebook_doc(doc):
    doc = copy.deepcopy(doc)  # the transformation is actually in-place,
    # but the user of this function should not worry about that.

    root = doc[1]  # top-level blocks

    # Locate the divs and extract the relevant data
    divs = []
    for index, elt in enumerate(root):
        if isinstance(elt, Div):
            div = elt
            classes = div[0][1]
            blocks = div[1]

            if "hidden" in classes or "slides" in classes or "notes" in classes:
                divs.append(("remove", index, blocks))
            else:
                divs.append(("unpack", index, blocks))

    # Reverse document order is needed not to invalidate
    # the remaining matches indices.
    for action, index, blocks in reversed(divs):
        del root[index]
        if action == "unpack":
            root[index:index] = blocks

    return doc


notebook_doc = make_notebook_doc(doc)

# TODO: also need to remove unsupported construct from Jupyter Markdown Cells.
#       E.g.: attributes (that's about it ?)
for elt in pandoc.iter(notebook_doc):
    if isinstance(elt, Header):
        header = elt
        attr = header[1] = ("", [], [])


def Notebook():
    return copy.deepcopy(
        {
            "cells": [],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3 (ipykernel)",
                    "language": "python",
                    "name": "python3",
                },
                "language_info": {
                    "codemirror_mode": {"name": "ipython", "version": 3},
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.9.7",
                },
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
    )


def CodeCell():
    return copy.deepcopy(
        {
            "cell_type": "code",
            #"execution_count": 1,
            "metadata": {},
            "outputs": [],
            "source": [],
        }
    )


def MarkdownCell():
    return copy.deepcopy({"cell_type": "markdown", "metadata": {}, "source": []})


def notebookify(doc):
    from pandoc.types import Pandoc, Meta, CodeBlock, Header, Para, Str, Space

    notebook = Notebook()
    cells = notebook["cells"]
    blocks = doc[1]
    #execution_count = 1

    metamap = doc[0][0]
    hero_title = [
        Str("Control"), Space(), Str("Engineering"), Space(), 
        Str("with"), Space(), 
        Str("Python")
    ]
    title = metamap["title"][0]
    author = metamap["author"][0][0][0]

    header = Pandoc(
        Meta({}), 
        [
            Header(1, ("", [], []), hero_title),
            Header(1, ("", [], []), title),
            Para(author),
        ]
    )

    header_cell = MarkdownCell()
    header_cell["source"] = pandoc.write(header)
    cells.append(header_cell)

    for block in blocks:
        if isinstance(block, CodeBlock):
            source = block[1]
            code_cell = CodeCell()
            code_cell["source"] = source
            code_cell["execution_count"] = None # execution_count
            #execution_count += 1
            cells.append(code_cell)
        else:
            wrapper = Pandoc(Meta({}), [block])
            options = ["-t", "markdown-smart-raw_attribute"]
            # -smart needed for en-dashes for example: we don't expect Jupyter
            # cells to be smart, so we *disable* the smart output so that
            # '–' won't get represented as '--'.
            # -raw_attribute so that raw html is output as HTML, not as
            # the non-standard markdown syntax `<p>Hello</p>`{=html} that
            # the Jupyter notebooks do not understand.
            source = pandoc.write(wrapper, options=options)

            merge_markdown = False
            if (
                merge_markdown
                and len(cells) >= 1
                and cells[-1]["cell_type"] == "markdown"
            ):
                cells[-1]["source"] += "\n" + source
            else:
                markdown_cell = MarkdownCell()
                markdown_cell["source"] = source
                cells.append(markdown_cell)
    return notebook


notebook = notebookify(notebook_doc)
output = open(doc_name + ".ipynb", "w")
output.write(json.dumps(notebook, indent=2))
output.close()
