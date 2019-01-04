#!/usr/bin/env python

# Python 2.7 Standard Library
from __future__ import division
import gc
import os

# Third-Party Packages
import numpy as np; np.seterr(all="ignore")
import numpy.linalg as la
import scipy.misc
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as pp
import matplotlib.axes as ax
import matplotlib.patches as pa


#
# Matplotlib Configuration & Helper Functions
# ------------------------------------------------------------------------------
#
rc = {
    "text.usetex": True,
    "pgf.preamble": [r"\usepackage{amsmath,amsfonts,amssymb}"], 
    #"font.family": "serif",
    "font.serif": [],
    #"font.sans-serif": [],
    "legend.fontsize": 10, 
    "axes.titlesize":  10,
    "axes.labelsize":  10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "savefig.dpi": 300
}
mpl.rcParams.update(rc)

# Use PGF to render PDF with LaTeX fonts of the proper size.
from matplotlib.backends.backend_pgf import FigureCanvasPgf
mpl.backend_bases.register_backend("pdf", FigureCanvasPgf)

# The width of the standard LaTeX document is 345.0 pt.
width_in = 345.0 / 72.0 # nota: text height = 598 pt for A4, 550 pt for US Letter.

def save(name, dpi=None):
    options = {} #{"bbox_inches": "tight"}
    if dpi:
        options["dpi"] = dpi
    cwd = os.getcwd()
    root = os.path.dirname(os.path.realpath(__file__))
    os.chdir(root)
    pp.savefig(name + ".pdf", **options)
    pp.savefig(name + ".png", **options)
    pp.savefig(name + ".pgf", **options)
    pp.savefig(name + ".svg", **options)
    os.chdir(cwd)

def set_ratio(ratio=1.0, bottom=0.1, top=0.1, left=0.1, right=0.1):
    height_in = (1.0 - left - right)/(1.0 - bottom - top) * width_in / ratio
    pp.gcf().set_size_inches((width_in, height_in))
    pp.gcf().subplots_adjust(bottom=bottom, top=1.0-top, left=left, right=1.0-right)

def dummy():
    x = np.r_[0.0:4.0:0.01]
    y = np.r_[0.0:4.0:0.1]
    uv_shape = (len(y), len(x))
    u = np.ones(uv_shape)
    v = np.zeros(uv_shape) + 0.1*u
    pp.streamplot(x, y, u, v)
    save("streamplot")  

def lotka_volterra():
    pp.figure()

    Y, X = np.mgrid[0.0:2.0:200j, 0.0:4.0:200j]

    alpha = 2 / 3
    beta = 4 / 3
    delta = gamma = 1.0
    U = alpha * X - beta * X * Y
    V = delta * X * Y - gamma * Y

    pp.axes().set_aspect(1.0)
    pp.axes().axis([0.0, 4.0, 0.0, 2.0])    

    pp.streamplot(X, Y, U, V, color="k")

    height_in = width_in
    pp.gcf().set_size_inches((width_in, height_in)) # height_in ignored ?
    # weight_in does not match ? dpi issue ? Prob. cause changing width_in 
    # does have an influence.

    # This is the bbox_in: tight options that is messing with us ...
    # (width and height). Investigate what that stuff is doing.
 
    save("prey-predator", dpi=180)     # TODO: use "savefig.dpi" param instead in rc.


def test():

    fig, axes = pp.subplots(nrows=1, ncols=1)

    axes.plot([0,1,2], [0,1,1])
    axes.axis([-0.1, 2.1, -0.1, 1.1])
    #axes.set_aspect(8.0)

    fig.subplots_adjust(left=0.25, right=0.75)
    fig.set_size_inches((width_in, width_in))


    pp.savefig("test.pdf")
    pp.savefig("test.png")

if  __name__ == "__main__":
    #dummy()
    #lotka_volterra()
    test()


