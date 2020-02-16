#!/usr/bin/env python

import copy
import json
import os.path
import sys

import pandoc
from pandoc.types import *


# ------------------------------------------------------------------------------
__doc__ = """

flags:

  - target: hidden, slides, notebook or no flag (both targets)

    'hidden' is "exec-only", the nitty-gritty stuff that won't appear anywhere,
    but is necessary for some side effects such as generating images used by
    the slides.

    'slides' won't appear in the notebook, but in the slides, and it's
    also executed

    'notebook' is not executed and appears only in the notebook.

  - exec status: no-exec or no flag (exec by default in slides mode only)

    NOTA: no-exec never used so far in the slides.

"""


# Source Document
# ------------------------------------------------------------------------------
doc_file = sys.argv[1]
doc_name = os.path.splitext(doc_file)[0]
doc = pandoc.read(file=doc_file)
# TODO: add python writer support in pandoc, add proper pdf quirk mangt
# pandoc.write(doc, file="doc.py", format="python") # debug


# Code Execution
# ------------------------------------------------------------------------------


def make_code_doc(doc):
    doc = copy.deepcopy(doc)  # the transformation is actually in-place,
    # but the user of this function should not worry about that.

    root = doc[1]  # top-level blocks

    # print(root)

    # Locate the divs and extract the relevant data
    divs = []
    for index, elt in enumerate(root):
        if isinstance(elt, Div):
            div = elt
            classes = div[0][1]
            contents = div[1]

            if "no-exec" in classes or "notebook" in classes:
                divs.append(("remove", index, contents))
            else:
                divs.append(("unpack", index, contents))

    # Reverse document order is needed not to invalidate
    # the remaining matches indices.
    for action, index, contents in reversed(divs):
        del root[index]
        if action == "unpack":
            root[index:index] = contents

    return doc


code_doc = make_code_doc(doc)

src = ""
for elt in pandoc.iter(code_doc):
    if isinstance(elt, CodeBlock):
        code = elt
        attr, text = code[:]
        _, classes, _ = attr[:]
        if "no-exec" not in classes and "notebook" not in classes:
            src += text + "\n"
with open(".tmp.py", "w") as output:
    output.write(src)
exec(src, {"__file__": __file__})

# Document Filter
# ------------------------------------------------------------------------------
# TODO: pandoc naming: is "path" well named? Cause I am tempted to also
#       name path the last component ... the "path" representation is
#       quite redundant ... DUNNO. Also use "location"? Path being a
#       nested seq of locations?
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

    # print(root)

    # Locate the divs and extract the relevant data
    divs = []
    for index, elt in enumerate(root):
        if isinstance(elt, Div):
            div = elt
            classes = div[0][1]
            contents = div[1]

            if "hidden" in classes or "notebook" in classes:
                divs.append(("remove", index, contents))
            else:
                divs.append(("unpack", index, contents))

    # Reverse document order is needed not to invalidate
    # the remaining matches indices.
    for action, index, contents in reversed(divs):
        del root[index]
        if action == "unpack":
            root[index:index] = contents

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

    # print(root)

    # Locate the divs and extract the relevant data
    divs = []
    for index, elt in enumerate(root):
        if isinstance(elt, Div):
            div = elt
            classes = div[0][1]
            contents = div[1]

            if "hidden" in classes or "slides" in classes:
                divs.append(("remove", index, contents))
            else:
                divs.append(("unpack", index, contents))

    # Reverse document order is needed not to invalidate
    # the remaining matches indices.
    for action, index, contents in reversed(divs):
        del root[index]
        if action == "unpack":
            root[index:index] = contents

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
                    "display_name": "Python 3",
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
                    "version": "3.6.4",
                },
            },
            "nbformat": 4,
            "nbformat_minor": 2,
        }
    )


def CodeCell():
    return copy.deepcopy(
        {
            "cell_type": "code",
            "execution_count": 1,
            "metadata": {},
            "outputs": [],
            "source": [],
        }
    )


def MarkdownCell():
    return copy.deepcopy({"cell_type": "markdown", "metadata": {}, "source": []})


def notebookify(doc):
    from pandoc.types import Pandoc, Meta, CodeBlock

    notebook = Notebook()
    cells = notebook["cells"]
    blocks = doc[1]
    # print(blocks)
    execution_count = 1

    for block in blocks:
        if isinstance(block, CodeBlock):
            source = block[1]
            code_cell = CodeCell()
            code_cell["source"] = source
            code_cell["execution_count"] = execution_count
            execution_count += 1
            cells.append(code_cell)
        else:
            wrapper = Pandoc(Meta({}), [block])
            options = ["-t", "markdown-smart"]  # needed for en-dashes for
            # example: we don't expect Jupyter cells to be smart, so we
            # *disable* the smart output so that '–' won't get represented
            # as '--'.
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
