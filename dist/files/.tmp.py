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
def f(xy):
    x, y = xy
    dx = -2*x + y
    dy = -2*y + x
    return array([dx, dy])
figure()
x = y = linspace(-5.0, 5.0, 1000)
streamplot(*Q(f, x, y), color="k")
plot([0], [0], "k.", ms=20.0)
axis("square")
axis("off")
tight_layout()
save("images/globally-attractive")
import matplotlib.animation as ani
from matplotlib.colors import to_rgb
from tqdm import tqdm


neutral = grey_4 = to_rgb("#ced4da")
#grey_5 = to_rgb("#adb5bd")
#grey_8 = to_rgb("#343a40")
good = to_rgb("#51cf66")
bad = to_rgb("#ff6b6b")

ft = lambda t, y: f(y)
fps = df = 60.0
dt = 1.0 / df
t_span = t_i, t_f = (0.0, 3.0)
t = np.arange(t_i, t_f + dt, dt)

y0s = [[-4.0, 1.0], [4.0, -1.0]]
colors = [good, good]
xys = []
for y0 in tqdm(y0s):
    r = solve_ivp(fun=ft, y0=y0, t_span=t_span, t_eval=t)
    xys.append(r.y)


fig = figure()
x = y = linspace(-5.0, 5.0, 1000)
streamplot(*Q(f, x, y), color=grey_4)
plot([0], [0], lw=3.0, marker="o", ms=10.0, markevery=[-1],
        markeredgecolor="white", color=neutral)
axis("square")
axis("off")

lines = []
for x, y in xys:
    line = plot(
        [x[0]], [y[0]],
        lw=3.0,
        ms=10.0,
        color=neutral,
        marker="o", markevery=[-1],
        markeredgecolor="white")[0]
    lines.append(line)
tight_layout()

num_frames = len(t) * len(lines)

def gamma(x):
    return pow(x, 0.5)

def update(i):
    j, k = divmod(i, len(t))
    x, y = xys[j]
    line = lines[j]
    line.set_data(x[:k+1], y[:k+1])
    alpha = gamma(k / (len(t)-1))
    final_color = colors[j]
    line.set_color(
      tuple((1-alpha)*array(neutral) + alpha*array(final_color))
    )

animation = ani.FuncAnimation(fig, func=update, frames=num_frames)
writer = ani.FFMpegWriter(fps=fps)
bar = tqdm(total=num_frames)
animation.save("videos/globally-attractive.mp4", writer=writer, dpi=300,
progress_callback = lambda i, n: bar.update(1))
bar.close()
def f(xy):
    x, y = xy
    dx = -2*x + y**3
    dy = -2*y + x**3
    return array([dx, dy])
figure()
x = y = linspace(-5.0, 5.0, 1000)
streamplot(*Q(f, x, y), color="k")
plot([0], [0], "k.", ms=10.0)
axis("square")
axis("off")
tight_layout()
save("images/locally-attractive")
import matplotlib.animation as ani
from matplotlib.colors import to_rgb
from tqdm import tqdm


neutral = grey_4 = to_rgb("#ced4da")
#grey_5 = to_rgb("#adb5bd")
#grey_8 = to_rgb("#343a40")
good = to_rgb("#51cf66")
bad = to_rgb("#ff6b6b")

ft = lambda t, y: f(y)
fps = df = 60.0
dt = 1.0 / df
t_span = t_i, t_f = (0.0, 3.0)
t = np.arange(t_i, t_f + dt, dt)

y0s = [[-2.4, 0.0], [-1.8, 0.0], [-1.2, 0.0]]
colors = [bad, good, good]
xys = []
for y0 in tqdm(y0s):
    r = solve_ivp(fun=ft, y0=y0, t_span=t_span, t_eval=t)
    xys.append(r.y)


fig = figure()
x = y = linspace(-5.0, 5.0, 1000)
streamplot(*Q(f, x, y), color=grey_4)
plot([0], [0], lw=3.0, marker="o", ms=10.0, markevery=[-1],
        markeredgecolor="white", color=neutral)
axis("square")
axis("off")

lines = []
for x, y in xys:
    line = plot(
        [x[0]], [y[0]],
        lw=3.0,
        ms=10.0,
        color=neutral,
        marker="o", markevery=[-1],
        markeredgecolor="white")[0]
    lines.append(line)
tight_layout()

num_frames = len(t) * len(lines)

def gamma(x):
    return pow(x, 0.5)

def update(i):
    j, k = divmod(i, len(t))
    x, y = xys[j]
    line = lines[j]
    line.set_data(x[:k+1], y[:k+1])
    alpha = gamma(k / (len(t)-1))
    final_color = colors[j]
    line.set_color(
      tuple((1-alpha)*array(neutral) + alpha*array(final_color))
    )

animation = ani.FuncAnimation(fig, func=update, frames=num_frames)
writer = ani.FFMpegWriter(fps=fps)
bar = tqdm(total=num_frames)
animation.save("videos/locally-attractive.mp4", writer=writer, dpi=300,
progress_callback = lambda i, n: bar.update(1))
bar.close()
def f(xy):
    x, y = xy
    dx = -2*x + y
    dy =  2*y - x
    return array([dx, dy])
figure()
x = y = linspace(-5.0, 5.0, 1000)
streamplot(*Q(f, x, y), color="k")
plot([0], [0], "k.", ms=10.0)
axis("square")
axis("off")
tight_layout()
save("images/not-attractive")
import matplotlib.animation as ani
from matplotlib.colors import to_rgb
from tqdm import tqdm


neutral = grey_4 = to_rgb("#ced4da")
#grey_5 = to_rgb("#adb5bd")
#grey_8 = to_rgb("#343a40")
good = to_rgb("#51cf66")
bad = to_rgb("#ff6b6b")

ft = lambda t, y: f(y)
fps = df = 60.0
dt = 1.0 / df
t_span = t_i, t_f = (0.0, 3.0)
t = np.arange(t_i, t_f + dt, dt)

y0s = [[-4*0.9659258262890683, -4*0.2588190451025208],
       [-4*0.9659258262890683, -4*0.2588190451025208 + 0.2],
       [0.2*0.9659258262890683, 0.2*0.2588190451025208 - 0.2]]
colors = [good, bad, bad]
xys = []
for y0 in tqdm(y0s):
    r = solve_ivp(fun=ft, y0=y0, t_span=t_span, t_eval=t)
    xys.append(r.y)


fig = figure()
x = y = linspace(-5.0, 5.0, 1000)
streamplot(*Q(f, x, y), color=grey_4)
plot([0], [0], lw=3.0, marker="o", ms=10.0, markevery=[-1],
        markeredgecolor="white", color=neutral)
axis("square")
axis("off")

lines = []
for x, y in xys:
    line = plot(
        [x[0]], [y[0]],
        lw=3.0,
        ms=10.0,
        color=neutral,
        marker="o", markevery=[-1],
        markeredgecolor="white")[0]
    lines.append(line)
tight_layout()

num_frames = len(t) * len(lines)

def gamma(x):
    return pow(x, 0.5)

def update(i):
    j, k = divmod(i, len(t))
    x, y = xys[j]
    line = lines[j]
    line.set_data(x[:k+1], y[:k+1])
    alpha = gamma(k / (len(t)-1))
    final_color = colors[j]
    line.set_color(
      tuple((1-alpha)*array(neutral) + alpha*array(final_color))
    )

animation = ani.FuncAnimation(fig, func=update, frames=num_frames)
writer = ani.FFMpegWriter(fps=fps)
bar = tqdm(total=num_frames)
animation.save("videos/not-attractive.mp4", writer=writer, dpi=300,
progress_callback = lambda i, n: bar.update(1))
bar.close()
m = l = b = 1; g=9.81

def f(theta_omega):
    theta, omega = theta_omega
    d_theta = omega
    d_omega = - b / (m * l * l) * omega
    d_omega -=  (g / l) * sin(theta)
    return (d_theta, d_omega)
figure()
theta = linspace(-2*pi*(1.2), 2*pi*(1.2), 1000)
d_theta = linspace(-5.0, 5.0, 1000)
streamplot(*Q(f, theta, d_theta), color="k")
plot([-2*pi, -pi, 0 ,pi, 2*pi], 5*[0.0], "k.")
xticks([-2*pi, -pi, 0 ,pi, 2*pi],
[r"$-2\pi$", r"$\pi$", r"$0$", r"$\pi$", r"$2\pi$"])
grid(True)
tight_layout()
save("images/pendulum-friction")
b = 0
figure()
streamplot(*Q(f, theta, d_theta), color="k")
plot([-2*pi, -pi, 0 ,pi, 2*pi], 5*[0.0], "k.")
xticks([-2*pi, -pi, 0 ,pi, 2*pi],
[r"$-2\pi$", r"$\pi$", r"$0$", r"$\pi$", r"$2\pi$"])
grid(True)
tight_layout()
save("images/pendulum-no-friction")
def f(xy):
    x, y = xy
    r = sqrt(x*x + y*y)
    dx = x + x * y - (x + y) * r
    dy = y - x * x + (x - y) * r
    return array([dx, dy])
figure()
x = y = linspace(-2.0, 2.0, 1000)
streamplot(*Q(f, x, y), color="k")
plot([1], [0], "k.", ms=20.0)
axis("square")
axis("off")
tight_layout()
save("images/attractive2")
import matplotlib.animation as ani
from matplotlib.colors import to_rgb
from tqdm import tqdm

neutral = grey_4 = to_rgb("#ced4da")
#grey_5 = to_rgb("#adb5bd")
#grey_8 = to_rgb("#343a40")
good = to_rgb("#51cf66")
bad = to_rgb("#ff6b6b")

ft = lambda t, y: f(y)
fps = df = 60.0
dt = 1.0 / df
t_span = t_i, t_f = (0.0, 10.0)
t = np.arange(t_i, t_f + 0.1*dt, dt)

y0s = [[1.5*cos(theta), 1.5*sin(theta)] for theta in linspace(0, (11/12)*2*pi, 12)]
# colors = [good] * len(y0s)
xys = []
for y0 in tqdm(y0s):
    r = solve_ivp(fun=ft, y0=y0, t_span=t_span, t_eval=t)
    xys.append(r.y)


fig = figure()
x = y = linspace(-2.0, 2.0, 1000)
streamplot(*Q(f, x, y), color=grey_4)
plot([1], [0], lw=3.0, marker="o", ms=10.0, markevery=[-1],
        markeredgecolor="white", color=neutral)
axis("square")
axis("off")

lines = []
for x, y in xys:
    line = plot(
        [x[0]], [y[0]],
        lw=3.0,
        ms=10.0,
        #color=neutral,
        marker="o", markevery=[-1],
        markeredgecolor="white")[0]
    lines.append(line)
tight_layout()

num_frames = len(t)

def gamma(x):
    return pow(x, 0.5)

def update(i):
  for line, (x, y) in zip(lines, xys):
      line.set_data(x[:i+1], y[:i+1])
    # j, k = divmod(i, len(t))
    # x, y = xys[j]
    # line = lines[j]
    # line.set_data(x[:k+1], y[:k+1])
    # alpha = gamma(k / (len(t)-1))
    # final_color = colors[j]
    # line.set_color(
    #   tuple((1-alpha)*array(neutral) + alpha*array(final_color))
    # )

animation = ani.FuncAnimation(fig, func=update, frames=num_frames)
writer = ani.FFMpegWriter(fps=fps)
bar = tqdm(total=num_frames)
animation.save("videos/pathological.mp4", writer=writer, dpi=300,
progress_callback = lambda i, n: bar.update(1))
bar.close()

# Third-Party Libraries
import numpy as np
import matplotlib.pyplot as plt

# Local Library
import mivp

# ------------------------------------------------------------------------------

# Vector field
def fun(t, xy):
    x, y = xy
    dx = -2*x + y
    dy = -2*y + x
    return array([dx, dy])

# Streamplot
fig = figure()
x = y = linspace(-5.0, 5.0, 1000)
streamplot(*Q(lambda xy: fun(0, xy), x, y), color=grey_4)
plot([0], [0], lw=3.0, marker="o", ms=10.0, markevery=[-1],
        markeredgecolor="white", color=neutral)
axis("square")
axis("off")
tight_layout()

# Time span & frame rate
t_span = (0.0, 10.0)

df = 60.0
dt = 1.0 / df
t = np.arange(t_span[0], t_span[1], dt)
t = np.r_[t, t_span[1]]

# Initial set boundary
y0 = [2.5, 0.0]
radius = 2.0
xc, yc = y0

def boundary(t):  # we assume that t is a 1-dim array
    return np.array(
        [
            [xc + radius * np.cos(theta), yc + radius * np.sin(theta)]
            for theta in 2 * np.pi * t
        ]
    )

# Precision
rtol = 1e-6  # default: 1e-3
atol = 1e-12  # default: 1e-6

# ------------------------------------------------------------------------------

data = mivp.solve_alt(
    fun=fun,
    t_eval=t,
    boundary=boundary,
    boundary_rtol=0.0,
    boundary_atol=0.1,
    rtol=rtol,
    atol=atol,
    method="LSODA",
)

good = to_rgb("#51cf66")
bad = to_rgb("#ff6b6b")
mivp.generate_movie(data, filename="videos/gas.mp4", fps=df,
    axes=gca(), zorder=1000, color=good, linewidth=3.0,
)

# Third-Party Libraries
import numpy as np
import matplotlib.pyplot as plt

# Local Library
import mivp

# ------------------------------------------------------------------------------

# Vector field
def fun(t, xy):
    x, y = xy
    r = np.sqrt(x * x + y * y)
    dx = x + x * y - (x + y) * r
    dy = y - x * x + (x - y) * r
    return [dx, dy]

# Streamplot
fig = figure()
x = y = linspace(-2.0, 2.0, 1000)
streamplot(*Q(f, x, y), color=grey_4)
plot([1], [0], lw=3.0, marker="o", ms=10.0, markevery=[-1],
        markeredgecolor="white", color=neutral)
axis("square")
axis("off")
tight_layout()

# Time span & frame rate
t_span = (0.0, 10.0)

df = 60.0
dt = 1.0 / df
t = np.arange(t_span[0], t_span[1], dt)
t = np.r_[t, t_span[1]]

# Initial set boundary
y0 = [1.0, 0.0]
radius = 0.5
n = 10000
xc, yc = y0

def boundary(t):  # we assume that t is a 1-dim array
    return np.array(
        [
            [xc + radius * np.cos(theta), yc + radius * np.sin(theta)]
            for theta in 2 * np.pi * t
        ]
    )

# Precision
rtol = 1e-6  # default: 1e-3
atol = 1e-12  # default: 1e-6

# ------------------------------------------------------------------------------

data = mivp.solve_alt(
    fun=fun,
    t_eval=t,
    boundary=boundary,
    boundary_rtol=0.0,
    boundary_atol=0.1,
    rtol=rtol,
    atol=atol,
    method="LSODA",
)

bad = to_rgb("#ff6b6b")
mivp.generate_movie(data, filename="videos/movie.mp4", fps=df,
    axes=gca(), zorder=1000, color=bad, linewidth=3.0,
)
def f(xy):
    x, y = xy
    q = x**2 + y**2 * (1 + (x**2 + y**2)**2)
    dx = (x**2 * (y - x) + y**5) / q
    dy = y**2 * (y - 2*x) / q
    return array([dx, dy])
figure()
x = y = linspace(-1.0, 1.0, 1000)
streamplot(*Q(f, x, y), color="k")
xticks([-1, 0, 1])
plot([0], [0], "k.", ms=10.0)
axis("square")
axis("off")
tight_layout()
save("images/vinograd")
def fun(t, xy):
    return f(xy)
eps = 1e-10; xy0 = (0, eps)
sol = solve_ivp(
  fun=fun,
  y0=xy0,
  t_span=(0.0, 100.0),
  dense_output=True)["sol"]
t = linspace(0.0, 100.0, 10000)
xt, yt = sol(t)
figure()
x = y = linspace(-1.0, 1.0, 1000)
streamplot(*Q(f, x, y), color="#ced4da")
xticks([-1, 0, 1])
plot([0], [0], "k.", ms=10.0)
plot(xt, yt, color="C0")
axis("square")
axis("off")
save("images/unstable")
