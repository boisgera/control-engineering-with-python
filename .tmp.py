from numpy import *
from numpy.linalg import *
from scipy.linalg import *
from matplotlib.pyplot import *
from mpl_toolkits.mplot3d import *
from scipy.integrate import solve_ivp
# Python 3.x Standard Library
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
# --------------------------------------------------------------------------

# TODO: also reconsider line width and markersize stuff "for the web
#       settings".
fontsize = 10

width = 345 / 72.27
height = width / (16/9)

rc = {
    "text.usetex": True,
    "pgf.preamble": r"\usepackage{amsmath,amsfonts,amssymb}",
    #"font.family": "serif",
    "font.serif": [],
    #"font.sans-serif": [],
    "legend.fontsize": fontsize,
    "axes.titlesize":  fontsize,
    "axes.labelsize":  fontsize,
    "xtick.labelsize": fontsize,
    "ytick.labelsize": fontsize,
    "figure.max_open_warning": 100,
    #"savefig.dpi": 300,
    #"figure.dpi": 300,
    "figure.figsize": [width, height],
    "lines.linewidth": 1.0,
}
mpl.rcParams.update(rc)

# Web target: 160 / 9 inches (that's ~45 cm, this is huge) at 90 dpi
# (the "standard" dpi for Web computations) gives 1600 px.
width_in = 160 / 9

def save(name, **options):
    cwd = os.getcwd()
    root = os.path.dirname(os.path.realpath(__file__))
    os.chdir(root)
    pp.savefig(name + ".svg", **options)
    os.chdir(cwd)

def set_ratio(ratio=1.0, bottom=0.1, top=0.1, left=0.1, right=0.1):
    height_in = (1.0 - left - right)/(1.0 - bottom - top) * width_in / ratio
    pp.gcf().set_size_inches((width_in, height_in))
    pp.gcf().subplots_adjust(bottom=bottom, top=1.0-top, left=left, right=1.0-right)
def Q(f, xs, ys):
    X, Y = meshgrid(xs, ys)
    v = vectorize
    fx = v(lambda x, y: f([x, y])[0])
    fy = v(lambda x, y: f([x, y])[1])
    return X, Y, fx(X, Y), fy(X, Y)
a = 2.0; x0 = 1.0
figure()
t = linspace(0.0, 3.0, 1000)
plot(t, exp(a*t)*x0, "k")
xlabel("$t$"); ylabel("$x(t)$"); title(f"$a={a}$")
grid(); axis([0.0, 2.0, 0.0, 10.0])
tight_layout()
save("images/scalar-LTI-2")
figure()
plot(real(a), imag(a), "x", color="k")
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$"); grid(True)
tight_layout() 
save("images/scalar-LTI-2-poles")
a = 1.0; x0 = 1.0
figure()
t = linspace(0.0, 3.0, 1000)
plot(t, exp(a*t)*x0, "k")
xlabel("$t$"); ylabel("$x(t)$"); title(f"$a={a}$")
grid(); axis([0.0, 2.0, 0.0, 10.0])
tight_layout()
save("images/scalar-LTI-1")
figure()
plot(real(a), imag(a), "x", color="k")
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$"); grid(True)
tight_layout()
save("images/scalar-LTI-1-poles")
a = 0.0; x0 = 1.0
figure()
t = linspace(0.0, 3.0, 1000)
plot(t, exp(a*t)*x0, "k")
xlabel("$t$"); ylabel("$x(t)$"); title(f"$a={a}$")
grid(); axis([0.0, 2.0, 0.0, 10.0])
tight_layout()
save("images/scalar-LTI-0")
figure()
plot(real(a), imag(a), "x", color="k")
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$"); grid(True)
tight_layout()
save("images/scalar-LTI-0-poles")
a = -1.0; x0 = 1.0
figure()
t = linspace(0.0, 3.0, 1000)
plot(t, exp(a*t)*x0, "k")
xlabel("$t$"); ylabel("$x(t)$"); title(f"$a={a}$")
grid(); axis([0.0, 2.0, 0.0, 10.0])
tight_layout()
save("images/scalar-LTI-m1")
figure()
plot(real(a), imag(a), "x", color="k")
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$"); grid(True)
tight_layout()
save("images/scalar-LTI-m1-poles")
a = -2.0; x0 = 1.0
figure()
t = linspace(0.0, 3.0, 1000)
plot(t, exp(a*t)*x0, "k")
xlabel("$t$"); ylabel("$x(t)$"); title(f"$a={a}$")
grid(); axis([0.0, 2.0, 0.0, 10.0])
tight_layout()
save("images/scalar-LTI-m2")
figure()
plot(real(a), imag(a), "x", color="k")
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$"); grid(True)
tight_layout()
save("images/scalar-LTI-m2-poles")
a1 = -1.0; a2 = 2.0; x10 = x20 = 1.0
figure()
t = linspace(0.0, 3.0, 1000)
x1 = exp(a1*t)*x10; x2 = exp(a2*t)*x20
xn = sqrt(x1**2 + x2**2)
plot(t, xn , "k")
plot(t, x1, "k--")
plot(t, x2 , "k--")
xlabel("$t$"); ylabel("$\|x(t)\|$"); title(f"$a_1={a1}, \; a_2={a2}$")
grid(); axis([0.0, 2.0, 0.0, 10.0])
tight_layout()
save("images/scalar-LTI-m1p2")
figure()
plot(real(a1), imag(a1), "x", color="k")
plot(real(a2), imag(a2), "x", color="k")
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a_1={a1}, \; a_2={a2}$")
grid(True)
tight_layout()
save("images/scalar-LTI-m1p2-poles")
a1 = -1.0; a2 = -2.0; x10 = x20 = 1.0
figure()
t = linspace(0.0, 3.0, 1000)
x1 = exp(a1*t)*x10; x2 = exp(a2*t)*x20
xn = sqrt(x1**2 + x2**2)
plot(t, xn , "k")
plot(t, x1, "k--")
plot(t, x2 , "k--")
xlabel("$t$"); ylabel("$\|x(t)\|$"); title(f"$a_1={a1}, \; a_2={a2}$")
grid(); axis([0.0, 2.0, 0.0, 10.0])
tight_layout()
save("images/scalar-LTI-m1m2")
figure()
plot(real(a1), imag(a1), "x", color="k")
plot(real(a2), imag(a2), "x", color="k")
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a_1={a1}, \; a_2={a2}$")
grid(True)
tight_layout()
save("images/scalar-LTI-m1m2-poles")
a = 1.0j; x0=1.0
figure()
t = linspace(0.0, 20.0, 1000)
plot(t, real(exp(a*t)*x0), label="$\Re(x(t))$")
plot(t, imag(exp(a*t)*x0), label="$\mathrm{Im}(x(t))$")
xlabel("$t$")
legend(); grid()
tight_layout()
save("images/scalar-LTI-alt-1")
fig = figure()
ax = fig.add_subplot(111, projection="3d")
zticks = ax.set_zticks
ax.plot(t, real(exp(a*t)*x0), imag(exp(a*t)*x0))
xticks([0.0, 20.0]); yticks([]); zticks([])
ax.set_xlabel("$t$")
ax.set_ylabel("$\Re(x(t))$")
ax.set_zlabel("$\mathrm{Im}(x(t))$")
tight_layout()
save("images/scalar-LTI-3d")
figure()
plot(real(a), imag(a), "x", color="k")
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$"); grid(True)
tight_layout()
save("images/scalar-LTI-1j-poles")
a = -0.5 + 1.0j; x0=1.0
figure()
t = linspace(0.0, 20.0, 1000)
plot(t, real(exp(a*t)*x0), label="$\Re(x(t))$")
plot(t, imag(exp(a*t)*x0), label="$\mathrm{Im}(x(t))$")
xlabel("$t$")
legend(); grid()
tight_layout()
save("images/scalar-LTI-alt-2")
fig = figure()
ax = fig.add_subplot(111, projection="3d")
zticks = ax.set_zticks
ax.plot(t, real(exp(a*t)*x0), imag(exp(a*t)*x0))
xticks([0.0, 20.0]); yticks([]); zticks([])
ax.set_xlabel("$t$")
ax.set_ylabel("$\Re(x(t))$")
ax.set_zlabel("$\mathrm{Im}(x(t))$")
tight_layout()
save("images/scalar-LTI-3d-2")
figure()
plot(real(a), imag(a), "x", color="k")
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$")
grid(True)
tight_layout()
save("images/scalar-LTI-m11j-poles")
