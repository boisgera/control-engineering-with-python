from numpy import *
from numpy.linalg import *
from numpy.testing import *
from matplotlib.pyplot import *
from scipy.integrate import *
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
fontsize = 35

rc = {
    "text.usetex": True,
    "pgf.preamble": [r"\usepackage{amsmath,amsfonts,amssymb}"], 
    #"font.family": "serif",
    "font.serif": [],
    #"font.sans-serif": [],
    "legend.fontsize": fontsize, 
    "axes.titlesize":  fontsize,
    "axes.labelsize":  fontsize,
    "xtick.labelsize": fontsize,
    "ytick.labelsize": fontsize,
    #"savefig.dpi": 300,
    #"figure.dpi": 300,
}
mpl.rcParams.update(rc)

# Web target: 160 / 9 inches (that's ~45 cm, this is huge) at 90 dpi 
# (the "standard" dpi for Web computations) gives 1600 px.
width_in = 160 / 9 

def save(name):
    cwd = os.getcwd()
    root = os.path.dirname(os.path.realpath(__file__))
    os.chdir(root)
    pp.savefig(name + ".svg")
    os.chdir(cwd)

def set_ratio(ratio=1.0, bottom=0.1, top=0.1, left=0.1, right=0.1):
    height_in = (1.0 - left - right)/(1.0 - bottom - top) * width_in / ratio
    pp.gcf().set_size_inches((width_in, height_in))
    pp.gcf().subplots_adjust(bottom=bottom, top=1.0-top, left=left, right=1.0-right)
from scipy.signal import place_poles
A = array([[0, 1], [0, 0]])
C = array([[1, 0]])
poles = [-1, -2]
K = place_poles(A.T, C.T, poles).gain_matrix
L = K.T
assert_almost_equal(K, [[3.0, 2.0]])
def fun(t, X_Xhat):
    x, x_hat = X_Xhat[0:2], X_Xhat[2:4]
    y, y_hat = C.dot(x), C.dot(x_hat)
    dx = A.dot(x)
    dx_hat = A.dot(x_hat) - L.dot(y_hat - y)
    return r_[dx, dx_hat]
y0 = [-2.0, 1.0, 0.0, 0.0]
result = solve_ivp(fun=fun, t_span=[0.0, 5.0], y0=y0, max_step=0.1)
figure()
t = result["t"]
y = result["y"]
plot(t, y[0], "b", label="$x_1$")
plot(t, y[2], "b:", alpha=0.5, label=r"$\hat{x}_1$")
plot(t, y[1], "g", label="$x_2$")
plot(t, y[3], "g:", alpha=0.5, label=r"$\hat{x}_2$")
grid(); legend()
save("images/observer-trajectories")
from scipy.linalg import solve_continuous_are
A = array([[0, 1], [0, 0]])
B = array([[0], [1]])
Q = array([[1, 0], [0, 1]]); R = array([[1]])
Sigma = solve_continuous_are(A.T, C.T, inv(Q), inv(R))
L = Sigma @ C.T @ R
eigenvalues, _ = eig(A - L @ C)
assert all([real(s) < 0 for s in eigenvalues])
figure()
x = [real(s) for s in eigenvalues]
y = [imag(s) for s in eigenvalues]
plot(x, y, "kx", ms=12.0)
xticks([-2, -1, 0, 1, 2])
yticks([-2, -1, 0, 1, 2])
plot([0, 0], [-2, 2], "k")
plot([-2, 2], [0, 0], "k")   
grid(True)
title("Eigenvalues")
axis("square")
axis([-2, 2, -2, 2])
save("images/poles-Kalman")
def fun(t, X_Xhat):
    x, x_hat = X_Xhat[0:2], X_Xhat[2:4]
    y, y_hat = C.dot(x), C.dot(x_hat)
    dx = A.dot(x)
    dx_hat = A.dot(x_hat) - L.dot(y_hat - y)
    return r_[dx, dx_hat]
y0 = [-2.0, 1.0, 0.0, 0.0]
result = solve_ivp(fun=fun, t_span=[0.0, 5.0], y0=y0, max_step=0.1)
figure()
t = result["t"]
y = result["y"]
plot(t, y[0], "b", label="$x_1$")
plot(t, y[2], "b:", alpha=0.5, label=r"$\hat{x}_1$")
plot(t, y[1], "g", label="$x_2$")
plot(t, y[3], "g:", alpha=0.5, label=r"$\hat{x}_2$")
grid(); legend()
save("images/observer-Kalman-trajectories")
