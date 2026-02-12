from numpy import *
from numpy.linalg import *
from scipy.integrate import solve_ivp
from matplotlib.pyplot import *
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

width
def Q(f, xs, ys):
    X, Y = meshgrid(xs, ys)
    fx = vectorize(lambda x, y: f([x, y])[0])
    fy = vectorize(lambda x, y: f([x, y])[1])
    return X, Y, fx(X, Y), fy(X, Y)
def fun(t, y):
    return y * y
t0, tf, y0 = 0.0, 3.0, array([1.0])
result = solve_ivp(fun, t_span=[t0, tf], y0=y0)
figure()
plot(result["t"], result["y"][0], "k")
xlim(t0, tf); xlabel("$t$"); ylabel("$x(t)$")
tight_layout()
save("images/finite-time-blowup")
tf = 1.0
r = solve_ivp(fun, [t0, tf], y0,
              dense_output=True)
figure()
t = linspace(t0, tf, 1000)
plot(t, r["sol"](t)[0], "k")
ylim(0.0, 10.0); grid();
xlabel("$t$"); ylabel("$x(t)$")
tight_layout()
save("images/finite-time-blowup-2")
def f(x1x2):
    x1, x2 = x1x2
    dx1 = 1.0 if x1 < 0.0 else -1.0
    return array([dx1, 0.0])
figure()
x1 = x2 = linspace(-1.0, 1.0, 20)
gca().set_aspect(1.0)
quiver(*Q(f, x1, x2), color="k")
tight_layout()
save("images/discont")
def sigma(x):
  return 1 / (1 + exp(-x))
figure()
x = linspace(-7.0, 7.0, 1000)
plot(x, sigma(x), label="$y=\sigma(x)$")
grid(True)
xlim(-5, 5)
xticks([-5.0, 0.0, 5.0])
yticks([0.0, 0.5, 1.0])
xlabel("$x$")
ylabel("$y$")
legend()
pp.gcf().subplots_adjust(bottom=0.2)
save("images/sigmoid")
alpha = 2 / 3; beta = 4 / 3; delta = gamma = 1.0

def fun(t, y):
    x, y = y
    u = alpha * x - beta * x * y
    v = delta * x * y - gamma * y
    return array([u, v])
tf = 3.0
result = solve_ivp(
  fun, 
  t_span=(0.0, tf), 
  y0=[1.5, 1.5], 
  max_step=0.01)
x, y = result["y"][0], result["y"][1]
def display_streamplot():
    ax = gca()
    xr = yr = linspace(0.0, 2.0, 1000)
    def f(y):
        return fun(0, y)
    streamplot(*Q(f, xr, yr), color="grey")
def display_reference_solution():
    for xy in zip(x, y):
        x_, y_ = xy
        gca().add_artist(Circle((x_, y_), 
                         0.2, color="#d3d3d3"))
    gca().add_artist(Circle((x[0], y[0]), 0.1, 
                     color="#808080"))
    plot(x, y, "k")
def display_alternate_solution():
    result = solve_ivp(fun, 
                       t_span=[0.0, tf],
                       y0=[1.5, 1.575], 
                       max_step=0.01)
    x, y = result["y"][0], result["y"][1]
    plot(x, y, "k--")
figure()
display_streamplot()
display_reference_solution()
display_alternate_solution()
axis([0,2,0,2]); axis("square")
save("images/continuity")
def fun(t, y):
  x = y[0]
  dx = sqrt(abs(y))
  return [dx]
tspan = [0.0, 3.0]
t = linspace(tspan[0], tspan[1], 1000)
figure()
for x0 in [0.1, 0.01, 0.001, 0.0001, 0.0]:
    r = solve_ivp(fun, tspan, [x0], 
        dense_output=True)
    plot(t, r["sol"](t)[0], 
         label=f"$x_0 = {x0}$")
xlabel("$t$"); ylabel("$x(t)$")
legend()
pp.gcf().subplots_adjust(bottom=0.2)
save("images/eps")
