% Ordinary Differential Equations
% [Sébastien Boisgérault](mailto:Sebastien.Boisgerault@mines-paristech.fr), MINES ParisTech, PSL University

## Preamble

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    from numpy import *
    from numpy.linalg import *
    from matplotlib.pyplot import *
    from mpl_toolkits.mplot3d import *

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: notebook :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    from numpy import *
    import matplotlib; matplotlib.use("nbAgg")
    %matplotlib notebook
    from matplotlib.pyplot import *

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

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

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## Vector Field

Let $n \in \mathbb{N}^*$ and $f:\mathbb{R}^n \to \mathbb{R}^n$.

Visualize $f(x)$ as an arrow with origin the point $x$.

In the plane ($n=2$), use [quiver](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.quiver.html) (Matplotlib).

## Q Helper

    def Q(f, xs, ys):
        X, Y = meshgrid(xs, ys)
        fx = vectorize(lambda x, y: f([x, y])[0])
        fy = vectorize(lambda x, y: f([x, y])[1])
        return X, Y, fx(X, Y), fy(X, Y)

## <i class="fa fa-eye"></i> Vector Field / Rotation

Consider $f(x,y) = (-y, x).$

    def f(xy):
        x, y = xy
        return array([-y, x])

## <i class="fa fa-area-chart"></i>

    figure()
    x = y = linspace(-1.0, 1.0, 20)
    gca().set_aspect(1.0); grid(True)
    quiver(*Q(f, x, y))

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    save("images/test_Q")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/test_Q.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## Ordinary Differential Equations (ODEs)

A solution of $\dot{x} = f(x)$ is

- a function $x:I \to \mathbb{R}^n$,

- defined on a (possibly unbounded) interval $I$ of $\mathbb{R}$,

- such that for every $t \in I,$

  $$\dot{x}(t) = dx(t)/dt = f(x(t)).$$

## <i class="fa fa-area-chart"></i>

```python
figure()
x = y = linspace(-1.0, 1.0, 20)
gca().set_aspect(1.0); grid(True)
streamplot(*Q(f, x, y), color="k")
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    save("images/test_Q2")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/test_Q2.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## Initial Value Problem (IVP)

Solutions $x(t)$, for $t\geq t_0$, of

$$
\dot{x} = f(x)
$$

such that

$$
x(t_0) = x_0 \in \mathbb{R}^n.
$$

---

The **initial condition** $(t_0, x_0)$ is made of

- the **initial time** $t_0 \in \mathbb{R}$ and

- the **initial value** or **initial state** $x_0 \in \mathbb{R}^n$.

The set $\mathbb{R}^n$ is the **state space**,  
$x(t)$ the **state at time** $t$.

## Higher-Order ODEs

Scalar differential equations structured as

$$
x^{(n)}(t) = f(x, \dot{x}, \ddot{x}, \dots, x^{(n-1)})
$$

can be converted to the standard form with the state

$$
y = (x, \dot{x}, \ddot{x}, \dots, x^{(n-1)}) \in \mathbb{R}^n
$$

---

$$
\begin{array}{ccl}
\dot{y}_1 &=& y_2 \\
\dot{y}_2 &=& y_3 \\
\vdots &\vdots& \vdots \\
\dot{y}_n &=& f(y_1, y_2, \dots, y_{n-1})
\end{array}
$$

## <i class="fa fa-eye"></i> Pendulum

![](images/static/pendulum.svg)

---

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
import matplotlib.animation as ani
from scipy.integrate import solve_ivp
from matplotlib.colors import to_rgb
from tqdm import tqdm

def Q(f, xs, ys):
    X, Y = meshgrid(xs, ys)
    fx = vectorize(lambda x, y: f([x, y])[0])
    fy = vectorize(lambda x, y: f([x, y])[1])
    return X, Y, fx(X, Y), fy(X, Y)

m=1.0; b=0.0; l=1.0; g=9.81
def f(theta_d_theta):
    theta, d_theta = theta_d_theta
    J = m * l * l
    d2_theta  = - b / J * d_theta
    d2_theta += - g / l * sin(theta)
    return array([d_theta, d2_theta])

neutral = grey_4 = to_rgb("#ced4da")
blue_5 = to_rgb("#339af0")
#grey_5 = to_rgb("#adb5bd")
grey_8 = to_rgb("#343a40")
good = to_rgb("#51cf66")
bad = to_rgb("#ff6b6b")

ft = lambda t, xy: f(xy)
fps = df = 60.0
dt = 1.0 / df
t_span = t_i, t_f = (0.0, 10.0)
t = arange(t_i, t_f + 0.1*dt, dt)

y0 = [3*pi/4, 0]
r = solve_ivp(fun=ft, y0=y0, t_span=t_span, t_eval=t, atol=1e-12, rtol=1e-15)
theta, dtheta = r.y
x = l * sin(theta)
y = -l * cos(theta)

height = width = 345 / 72.27
fig = figure(figsize=(width, height))
axis("equal")
gca().set_xlim(-1.1*l, 1.1*l)
gca().set_ylim(-1.1*l, 1.1*l)
theta = linspace(0, 2*pi, 1000)
plot(cos(theta), sin(theta), linewidth=2, linestyle="dashed", color=neutral, zorder=-100)
plot([0], [0],
    marker="o", markevery=[-1],
    ms=15.0,
    mew=5.0,
    markerfacecolor="white",
    markeredgecolor=grey_8,
    zorder=100)
axis("off")
subplots_adjust(0.0, 0.0, 1.0, 1.0)

line = plot(
    [0, x[0]], [0, y[0]],
    lw=5.0,
    ms=20.0,
    color=grey_8,
    marker="o", markevery=[-1],
    #markeredgecolor="white"
)[0]


num_frames = len(t)

def update(i):
    line.set_data([0, x[i]], [0, y[i]])

animation = ani.FuncAnimation(fig, func=update, frames=num_frames)
writer = ani.FFMpegWriter(fps=fps)
bar = tqdm(total=num_frames)
animation.save("videos/pendulum.mp4", writer=writer, dpi=300,
progress_callback = lambda i, n: bar.update(1))
bar.close()
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```{=html}
<video style="height:80vh;" controls>
  <source src="videos/pendulum.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
```

## <i class="fa fa-question-circle-o"></i> -- Model / Pendulum

- [</i><i class="fa fa-gear"></i>, </i><i class="fa fa-superscript"></i>]
  Establish the equations governing the pendulum dynamics
  when the mechanical energy of the system is constant.

- [</i><i class="fa fa-gear"></i>, </i><i class="fa fa-superscript"></i>]
  Generalize the dynamics when there is a friction torque
  $c = -b \dot{\theta}$ for some $b \geq 0$.

### <i class="fa fa-key"></i> -- Result

$$
m \ell^2 \ddot{\theta} + b \dot{\theta} + m g \ell \sin \theta = 0
$$

---

Introduce the rotational frequency $\omega = \dot{\theta}$ in rad/sec.

The pendulum dynamics is equivalent to:

$$
\begin{array}{lll}
\dot{\theta} &=& \omega \\
\dot{\omega} &=& - (b/m\ell^2) \omega -(g /\ell) \sin \theta
\end{array}
$$

---

    m=1.0; b=0.0; l=1.0; g=9.81
    def f(theta_d_theta):
        theta, d_theta = theta_d_theta
        J = m * l * l
        d2_theta  = - b / J * d_theta
        d2_theta += - g / l * sin(theta)
        return array([d_theta, d2_theta])

## <i class="fa fa-area-chart"></i>

    width = 345 / 72.27
    height = width / (16 / 9)
    figure(figsize=(width, height))
    theta = linspace(-1.5 * pi, 1.5 * pi, 100)
    d_theta = linspace(-5.0, 5.0, 100)
    grid(True)
    xticks([-pi, 0, pi], [r"$-\pi$", "$0$", r"$\pi$"], fontsize=10)
    yticks(fontsize=10)

    streamplot(*Q(f, theta, d_theta), color="k", linewidth=1.0)

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    save("images/streamplot_pendulum")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/streamplot_pendulum.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
# import matplotlib.animation as ani
# from matplotlib.colors import to_rgb
# from scipy.integrate import solve_ivp
# from tqdm import tqdm


# neutral = grey_4 = to_rgb("#ced4da")
# blue_5 = to_rgb("#339af0")
# #grey_5 = to_rgb("#adb5bd")
# #grey_8 = to_rgb("#343a40")
# good = to_rgb("#51cf66")
# bad = to_rgb("#ff6b6b")

# ft = lambda t, y: f(y)
# fps = df = 60.0
# dt = 1.0 / df
# t_span = t_i, t_f = (0.0, 10.0)
# t = np.arange(t_i, t_f + 0.1*dt, dt)

# y0s = [[-pi/2+0.01, 0]]
# colors = [good]
# xys = []
# for y0 in tqdm(y0s):
#     r = solve_ivp(fun=ft, y0=y0, t_span=t_span, t_eval=t)
#     xys.append(r.y)


# fig = figure()
# x = linspace(-1.1*pi/2, 1.1*pi/2, 1000)
# y = linspace(-5.0, 5.0, 1000)
# streamplot(*Q(f, x, y), color=grey_4)
# plot([0], [0], lw=3.0, marker="o", ms=10.0, markevery=[-1],
#         markeredgecolor="white", color=neutral)
# axis("square")
# axis("off")

# lines = []
# for x, y in xys:
#     line = plot(
#         [x[0]], [y[0]],
#         lw=3.0,
#         ms=10.0,
#         color=blue_5,
#         marker="o", markevery=[-1],
#         markeredgecolor="white")[0]
#     lines.append(line)
# tight_layout()

# num_frames = len(t) * len(lines)

# def gamma(x):
#     return pow(x, 0.5)

# def update(i):
#     j, k = divmod(i, len(t))
#     x, y = xys[j]
#     line = lines[j]
#     line.set_data(x[:k+1], y[:k+1])

# animation = ani.FuncAnimation(fig, func=update, frames=num_frames)
# writer = ani.FFMpegWriter(fps=fps)
# bar = tqdm(total=num_frames)
# animation.save("videos/pendulum2.mp4", writer=writer, dpi=300,
# progress_callback = lambda i, n: bar.update(1))
# bar.close()
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

<!--
```{=html}
<video style="width:100vw;" controls>
  <source src="videos/pendulum2.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
```
-->

## <i class="fa fa-question-circle-o"></i> -- Model / Pendulum

- [<i class="fa fa-flask"></i>, <i class="fa fa-area-chart"></i>]
  Determine an approximation of the least possible angular velocity
  $\omega_0 > 0$ such that when $\theta(0) = 0$ and
  $\dot{\theta}(0) = \omega_0$, the pendulum reaches (or overshoots)
  $\theta(t) = \pi$ for some $t>0$.

- [<i class="fa fa-lightbulb-o"></i>, <i class="fa fa-superscript"></i>]
  Answer the same question analytically.

<style>

.reveal section img {
  border:0;
  height:50vh;
  width:auto;

}

.reveal section img.medium {
  border:0;
  max-width:50vh;
}

.reveal section img.icon {
  display:inline;
  border:0;
  width:1em;
  margin:0em;
  box-shadow:none;
  vertical-align:-10%;
}

.reveal code {
  font-family: Inconsolata, monospace;
}

.reveal pre code {
  font-size: 1.5em;
  line-height: 1.5em;
  /* max-height: 80wh; won't work, overriden */
}

input {
  font-family: "Source Sans Pro", Helvetica, sans-serif;
  font-size: 42px;
  line-height: 54.6px;
}

</style>

<link href="https://fonts.googleapis.com/css?family=Inconsolata:400,700" rel="stylesheet">

<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.css" rel="stylesheet">
