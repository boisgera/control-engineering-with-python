% Ordinary Differential Equations
% [Sébastien Boisgérault](mailto:Sebastien.Boisgerault@mines-paristech.fr), MINES ParisTech, PSL University

Preamble
--------------------------------------------------------------------------------

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


Introduction
================================================================================

Vector Field
--------------------------------------------------------------------------------

Let $n \in \mathbb{N}^*$ and $f:\mathbb{R}^n \to \mathbb{R}^n$. 

Visualize $f(x)$ as an arrow with origin the point $x$.

In the plane ($n=2$), use [quiver](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.quiver.html) (Matplotlib).


Q Helper
--------------------------------------------------------------------------------

    def Q(f, xs, ys):
        X, Y = meshgrid(xs, ys)
        fx = vectorize(lambda x, y: f([x, y])[0])
        fy = vectorize(lambda x, y: f([x, y])[1])
        return X, Y, fx(X, Y), fy(X, Y)

<i class="fa fa-eye"></i> Vector Field / Rotation
--------------------------------------------------------------------------------

Consider $f(x,y) = (-y, x).$

    def f(xy):
        x, y = xy
        return array([-y, x])

<i class="fa fa-area-chart"></i>
--------------------------------------------------------------------------------

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

Ordinary Differential Equations (ODEs)
--------------------------------------------------------------------------------

A solution of $\dot{x} = f(x)$ is

- a function $x:I \to \mathbb{R}^n$,

- defined on a (possibly unbounded) interval $I$ of $\mathbb{R}$,

- such that for every $t \in I,$

  $$\dot{x}(t) = dx(t)/dt = f(x(t)).$$

<i class="fa fa-area-chart"></i>
--------------------------------------------------------------------------------

``` python
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

Initial Value Problem (IVP)
--------------------------------------------------------------------------------

Solutions $x(t)$, for $t\geq t_0$, of

$$
\dot{x} = f(x)
$$

such that

$$
x(t_0) = x_0 \in \mathbb{R}^n.
$$


--------------------------------------------------------------------------------

The **initial condition** $(t_0, x_0)$ is made of 

  - the **initial time** $t_0 \in \mathbb{R}$ and 

  - the **initial value** or **initial state** $x_0 \in \mathbb{R}^n$.
 
The set $\mathbb{R}^n$ is the **state space**,  
$x(t)$ the **state at time** $t$.


Higher-Order ODEs
--------------------------------------------------------------------------------

Scalar differential equations structured as

  $$
  x^{(n)}(t) = f(x, \dot{x}, \ddot{x}, \dots, x^{(n-1)})
  $$

can be converted to the standard form with the state
 
  $$
  y = (x, \dot{x}, \ddot{x}, \dots, x^{(n-1)}) \in \mathbb{R}^n
  $$

--------------------------------------------------------------------------------

  $$
  \begin{array}{ccl}
  \dot{y}_1 &=& y_2 \\
  \dot{y}_2 &=& y_3 \\
  \vdots &\vdots& \vdots \\
  \dot{y}_n &=& f(y_1, y_2, \dots, y_{n-1})
  \end{array}
  $$


<i class="fa fa-eye"></i> Pendulum
--------------------------------------------------------------------------------

![](images/static/pendulum.svg)

--------------------------------------------------------------------------------

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

``` python
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

<i class="fa fa-question-circle-o"></i> -- Model / Pendulum
--------------------------------------------------------------------------------

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

--------------------------------------------------------------------------------

Introduce the rotational frequency $\omega = \dot{\theta}$ in rad/sec. 

The pendulum dynamics is equivalent to:

  $$
  \begin{array}{lll}
  \dot{\theta} &=& \omega \\
  \dot{\omega} &=& - (b/m\ell^2) \omega -(g /\ell) \sin \theta  
  \end{array}
  $$

--------------------------------------------------------------------------------

    m=1.0; b=0.0; l=1.0; g=9.81
    def f(theta_d_theta):
        theta, d_theta = theta_d_theta
        J = m * l * l
        d2_theta  = - b / J * d_theta 
        d2_theta += - g / l * sin(theta)
        return array([d_theta, d2_theta])
            

<i class="fa fa-area-chart"></i>
--------------------------------------------------------------------------------

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

``` python
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

<i class="fa fa-question-circle-o"></i> -- Model / Pendulum
--------------------------------------------------------------------------------

  - [<i class="fa fa-flask"></i>, <i class="fa fa-area-chart"></i>] 
    Determine an approximation of the least possible angular velocity 
    $\omega_0 > 0$ such that when $\theta(0) = 0$ and 
    $\dot{\theta}(0) = \omega_0$, the pendulum reaches (or overshoots)
    $\theta(t) = \pi$ for some $t>0$.

  - [<i class="fa fa-lightbulb-o"></i>, <i class="fa fa-superscript"></i>] 
    Answer the same question analytically.

Numerical Solution (Basic)
--------------------------------------------------------------------------------

Given a finite **time span** $[t_0, t_f]$ and a small enough **time step**
$\Delta t > 0$, we can use the approximation:

  $$
  \begin{split}
  x(t + \Delta t) 
    & \simeq x(t) + \Delta t \times \dot{x}(t) \\
    & = x(t) + \Delta t \times f(x(t)) \\
  \end{split}
  $$

to compute a sequence of states $x_k \in \mathbb{R}^n$ such that:

  $$
  x(t = t_0 + k \Delta t) \simeq x_k.
  $$


Euler Scheme
--------------------------------------------------------------------------------

(Fixed-step & explicit version) 

    def basic_solve_ivp(f, t0, x0, dt, t_f):
        ts, xs = [t0], [x0]
        while ts[-1] < t_f:
            t, x = ts[-1], xs[-1]
            t_next, x_next = t + dt, x + dt * f(x)
            ts.append(t_next); xs.append(x_next)
        return (array(ts), array(xs).T)

--------------------------------------------------------------------------------

Why the final transposition (`.T`)? 

So that when

`t, x = basic_solve_ivp(...)`,

`x[i]` refers to the values of the `i`th component of `x`.

(without the `.T`, it would be `x[:][i]`)



<i class="fa fa-eye"></i> Rotation / Solution
--------------------------------------------------------------------------------

  $$
  \left|
  \begin{split}
  \dot{x} &= -y \\
  \dot{y} &= +x
  \end{split}
  \right.,
  \; \mbox{ with } \;
  \left|
  \begin{array}{l}
  x(0) = 1\\
  y(0) = 0
  \end{array}
  \right.
  $$


--------------------------------------------------------------------------------

    def f(xy):
        x, y = xy
        return array([-y, x])
    t0, x0 = 0.0, array([1.0, 0.0])
    dt, tf = 0.001, 5.0
    t, x = basic_solve_ivp(f, t0, x0, dt, tf)

<i class="fa fa-area-chart"></i> Trajectories
--------------------------------------------------------------------------------

    figure()
    plot(t, x[0])
    plot(t, x[1])
    grid(True)


::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/rotation")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/rotation.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


<i class="fa fa-area-chart"></i> Trajectories (State Space)
--------------------------------------------------------------------------------

Represent solutions fragments in the background

    xs = ys = linspace(-1.5, 1.5, 50)
    x0, x1 = x

<i class="fa fa-area-chart"></i> ...
--------------------------------------------------------------------------------

    figure()
    streamplot(*Q(f, xs, ys), color="lightgrey")
    plot(x0, x1, "k"); plot(x0[0], x1[0], "ko")
    dx0, dx1 = x0[-1] - x0[-2], x1[-1] - x1[-2]
    arrow(x[0][-1], x[1][-1], dx0, dx1, width=0.02, color="k", zorder=10)
    grid(); axis("equal")

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/rotation2")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/rotation2.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


Beyond the Basic Solver
--------------------------------------------------------------------------------

Many issues that our basic solver doesn't address:

  - time-dependent vector field,

  - error control,

  - dense outputs,

  - and more ...

--------------------------------------------------------------------------------

Instead, use:

    from scipy.integrate import solve_ivp

Documentation: [`solve_ivp`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html) (Scipy)


<i class="fa fa-eye"></i> IVP / Rotation
--------------------------------------------------------------------------------

Compute the solution $x(t)$ for $t\in[0,2\pi]$ of the IVP:

  $$
  \left|
  \begin{split}
  \dot{x}_1 &= -x_2 \\
  \dot{x}_2 &= +x_1
  \end{split}
  \right.
  \; \mbox{ with } \;
  \left|
  \begin{array}{l}
  x_1(0) = 1\\
  x_2(0) = 0
  \end{array}
  \right.
  $$


<i class="fa fa-eye"></i> Solver Interface / Rotation
--------------------------------------------------------------------------------

    def fun(t, y):
        x1, x2 = y
        return array([-x2, x1])
    t_span = [0.0, 2*pi]
    y0 = [1.0, 0.0]
    result = solve_ivp(fun=fun, t_span=t_span, y0=y0)

Result Structure
--------------------------------------------------------------------------------

The `result` is a dictionary-like object (a "bunch").

Its fields:

  - `t` : array, time points, shape `(n_points,)`,

  - `y` : array, values of the solution at t, shape `(n, n_points)`,

  - ...

  (See [`solve_ivp` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html))


Non-Autonomous Systems
--------------------------------------------------------------------------------

<i class="fa fa-warning"></i> The solver may apply to
systems that are not time-invariant

  $$
  \dot{y} = f(t, y)
  $$ 

The `t` argument in the definition of `fun` is mandatory, 
even if the returned value doesn't depend on it (time-invariant system).

--------------------------------------------------------------------------------

    r_t = result["t"]
    x_1 = result["y"][0]
    x_2 = result["y"][1]

<i class="fa fa-area-chart"></i>
--------------------------------------------------------------------------------

    figure()
    t = linspace(0, 2*pi, 1000)
    plot(t, cos(t), "k--")
    plot(t, sin(t), "k--")
    bold = {"lw": 2.0, "ms": 10.0}
    plot(r_t, x_1, ".-", label="$x_1(t)$", **bold)
    plot(r_t, x_2, ".-", label="$x_2(t)$", **bold)
    xlabel("$t$"); grid(); legend()

--------------------------------------------------------------------------------

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/solve_ivp_1")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/solve_ivp_1.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::



Variable Step Size
--------------------------------------------------------------------------------

The step size is:

  - variable: $t_{n+1} - t_n$ may not be constant, 

  - automatically selected by the algorithm,

The solver shall meet the user specification,
but should select the largest step size to do so 
to minimize the number of computations.

Optionally, you can specify a `max_step` (default: $+\infty$).


Error Control
--------------------------------------------------------------------------------

We generally want to control the (local) error $e(t)$:   
the difference between the numerical solution and the exact one.

  - `atol` is the **absolute tolerance** (default: $10^{-6}$),

  - `rtol` is the **relative tolerance** (default: $10^{-3}$).

The solver ensures (approximately) that at each step:

  $$
  |e(t)| \leq \mathrm{atol} + \mathrm{rtol} \times |x(t)|
  $$

--------------------------------------------------------------------------------

    options = {
        # at least 20 data points
        "max_step": 2*pi / 20, 
        # standard absolute tolerance
        "atol"    : 1e-6,        
        # very large relative tolerance
        "rtol"    : 1e9 
    }

--------------------------------------------------------------------------------

    result = solve_ivp(
        fun=fun, t_span=t_span, y0=y0, 
        **options
    )
    r_t = result["t"]
    x_1 = result["y"][0]
    x_2 = result["y"][1]

<i class="fa fa-area-chart"></i>
--------------------------------------------------------------------------------

    figure()
    t = linspace(0, 2*pi, 20)
    plot(t, cos(t), "k--")
    plot(t, sin(t), "k--")
    bold = {"lw": 2.0, "ms": 10.0}
    plot(r_t, x_1, ".-", label="$x_1(t)$", **bold)
    plot(r_t, x_2, ".-", label="$x_2(t)$", **bold)
    xlabel("$t$"); grid(); legend()

--------------------------------------------------------------------------------

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/solve_ivp_2")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/solve_ivp_2.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


Dense Outputs
--------------------------------------------------------------------------------

Using a small `max_step` is usually the wrong way to "get more data points" 
since this will trigger many (potentially expensive) evaluations of `fun`.

Instead, use dense outputs: the solver may return  
the discrete data `result["t"]` and `result["y"]` 
**and** an approximate 
solution `result["sol"]` **as a function of `t`**
with little extra computations.

--------------------------------------------------------------------------------

    options = {
        "dense_output": True
    }

--------------------------------------------------------------------------------

    result = solve_ivp(
        fun=fun, t_span=t_span, y0=y0, 
        **options
    )
    r_t = result["t"]
    x_1 = result["y"][0]
    x_2 = result["y"][1]
    sol = result["sol"]

--------------------------------------------------------------------------------

    figure()
    t = linspace(0, 2*pi, 1000)
    plot(t, cos(t), "k--")
    plot(t, sin(t), "k--")
    bold = {"lw": 2.0, "ms": 10.0}
    plot(t, sol(t)[0], "-", label="$x_1(t)$", **bold)
    plot(t, sol(t)[1], "-", label="$x_2(t)$", **bold)
    plot(r_t, x_1, ".", color="C0", **bold)
    plot(r_t, x_2, ".", color="C1", **bold)
    xlabel("$t$"); grid(); legend()

--------------------------------------------------------------------------------

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/solve_ivp_3")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/solve_ivp_3.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::



Well-Posedness
================================================================================

Well-Posedness of an IVP
--------------------------------------------------------------------------------

**Well-Posedness** = Existence + Uniqueness + Continuity

A set of properties that ensures that common problems with IVPs cannot happen.

We are going to detail each property


Preamble: Local vs Global
--------------------------------------------------------------------------------

So far, we have only dealt with **global** solutions $x(t)$ of IVPs,
defined for any $t \geq t_0$.


This concept is sometimes too stringent.

--------------------------------------------------------------------------------

Consider for example:

$\dot{x} = x^2$ and $x(0)=1.$

-----

    def fun(t, y):
        return y * y
    t0, tf, y0 = 0.0, 3.0, array([1.0])
    result = solve_ivp(fun, t_span=[t0, tf], y0=y0)
    figure()
    plot(result["t"], result["y"][0], "k")
    xlim(t0, tf); xlabel("$t$"); ylabel("$x(t)$")


::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/finite-time-blowup")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/finite-time-blowup.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

--------------------------------------------------------------------------------

Ouch.

There is actually no **global** solution. 

However there is **local** solution $x(t)$, 
defined for $t \in \left[t_0, \tau\right[$
for some $\tau > t_0$.

--------------------------------------------------------------------------------

Indeed, the function

$$
x(t) = \frac{1}{1 - t}
$$

satisfies

$$
\dot{x}(t) = \frac{d}{dt} x(t) = -\frac{-1}{(1 - t)^2} 
=  (x(t))^2.
$$

But it's defined only for $t<1.$


<i class="fa fa-area-chart"></i>
--------------------------------------------------------------------------------

    tf = 1.0
    result = solve_ivp(fun, t_span=[t0, tf], y0=y0, max_step=0.01)
    figure()
    plot(result["t"], result["y"][0], "k")
    ylim(0.0, 10.0); grid(); xlabel("$t$"); ylabel("$x(t)$")

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/finite-time-blowup-2")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/finite-time-blowup-2.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


--------------------------------------------------------------------------------

This local solution is also **maximal**:

You cannot extend this solution beyond $\tau=1.0$.

Maximal Solution
--------------------------------------------------------------------------------

A solution $x :[0, \tau[$ to an IVP is **maximal** if there is no other solution
 
  - defined on $[0, \tau'[$ with $\tau' > \tau$,
  
  - whose restriction to $[0, \tau[$ is $x$.

<i class="fa fa-question-circle-o"></i> -- Local/Maximal Solution
--------------------------------------------------------------------------------

  - [<i class="fa fa-superscript"></i>] Find a local solution $x(t)$
    of $\dot{x} = x^2$ such that $x(0) = x_0$ under the assumption
    that $x(t) \neq 0$ when $t\geq 0$.

    <i class="fa fa-key"></i> **Hint:** compute $d(1/x(t))/dt.$

  - \[<i class="fa fa-lightbulb-o"></i>\] Find for every $x_0 \neq 0$
    a maximal solution. When is it global?

Bad News (1/3)
--------------------------------------------------------------------------------

Sometimes things get worse than simply having no global solution.

<i class="fa fa-eye"></i> -- No Local Solution
--------------------------------------------------------------------------------

Consider the scalar IVP with initial value $x(0) = (0,0)$ and right-hand side

  $$
  f(x_1,x_2) = 
  \left|
  \begin{array}{rl}
  (+1,0) & \mbox{if } \; x_1< 0 \\
  (-1,0) & \mbox{if } \; x_1 \geq 0.
  \end{array}
  \right.
  $$

<i class="fa fa-area-chart"></i> -- No Local Solution
--------------------------------------------------------------------------------

    def f(x1x2):
        x1, x2 = x1x2
        dx1 = 1.0 if x1 < 0.0 else -1.0
        return array([dx1, 0.0])
    figure()
    x1 = x2 = linspace(-1.0, 1.0, 20)
    gca().set_aspect(1.0); grid(True)
    quiver(*Q(f, x1, x2), color="k") 


::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/discont")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/discont.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


<i class="fa fa-lightbulb-o"></i> -- No Local Solution
--------------------------------------------------------------------------------

This system has no solution, not even a local one, when $x(0) = (0,0)$.

Proof
--------------------------------------------------------------------------------

  - Assume that $x: [0, \tau[ \to \mathbb{R}$ is a local solution.

  - Since $\dot{x}(0) = -1 < 0$,
    for some small enough $0 < \epsilon < \tau$ and any 
    $t \in \left]0, \epsilon\right]$, we have $x(t) < 0$. 

  - Consequently, $\dot{x}(t) = +1$ and thus by integration

    $$
    x(\epsilon) =  x(0) + \int_0^{\epsilon} \dot{x}(t) \, dt = \epsilon > 0,
    $$
  
    which is a contradiction.  
    
Good News (1/3)
--------------------------------------------------------------------------------

However, a local solution exists under very mild assumptions.


Existence
--------------------------------------------------------------------------------

If $f$ is continuous, 

  - There is a (at least one) **local** solution to the IVP

    $\dot{x} = f(x)$ and $x(t_0) = x_0$.

  - Any local solution on some $\left[t_0, \tau \right[$ 
    can be extended to a (at least one) **maximal** one 
    on some $\left[t_0, t_{\infty}\right[$.

**Note:** a maximal solution is **global** iff $t_{\infty} = +\infty$.

Theorem -- Characterization of Maximal Solutions
--------------------------------------------------------------------------------

A solution on $\left[t_0, \tau \right[$ is maximal if and only if either

  - $\tau = +\infty$ : the solution is global, or

  - $\tau < +\infty$ and $\displaystyle \lim_{t \to \tau} \|x(t)\| = +\infty.$

In plain words : a non-global solution cannot be extended further in time 
if and only if it "blows up".

Corollary
--------------------------------------------------------------------------------

Let's assume that a local maximal solution exists.

You wonder if this solution is defined in $[t_0, t_f[$ or blows up before $t_f$.

For example, you wonder if a solution is global  
(if $t_f = +\infty$ or $t_f < +\infty$.)


<i class="fa fa-lightbulb-o"></i> Prove existence on $[0, t_f[$
--------------------------------------------------------------------------------

**TODO.** Show that any solution which defined on some
sub-interval $[t_0, \tau]$ with $\tau < t_f$ would is bounded.

Then, no solution can be maximal on any
such $[0, \tau[$ (since it doesn't blow up !). Since a maximal
solution does exist, its domain is $[0, t_{\infty}[$ with $t_{\infty} \geq t_f$.

**$\Rightarrow$ a solution is defined on $[t_0, t_f[$.**

<i class="fa fa-question-circle-o"></i> -- Existence / Sigmoid
--------------------------------------------------------------------------------


Consider

  $$
  \dot{x} = \frac{1}{1 + e^{-x}} \mbox{ with } x(0) = x_0 \in \mathbb{R}
  $$


  - [</i><i class="fa fa-superscript"></i>] 
    Show that there is a (at least one) maximal solution.

  - [<i class="fa fa-superscript"></i>] 
    Show that any such solution is global.

<i class="fa fa-question-circle-o"></i> -- Existence / Pendulum
--------------------------------------------------------------------------------

Consider the pendulum, subject to a torque $c$

$$
ml^2 \ddot{\theta} + b \dot{\theta} + mg \ell \sin \theta = c
$$

We assume that the torque provides a bounded power:

$$
P(t) = c(t) \dot{\theta}(t) \leq M < +\infty.
$$

--------------------------------------------------------------------------------

  - [</i><i class="fa fa-superscript"></i>] Show that for any initial condition
    $t_0$, $\theta(t_0) = \theta_0$ and $\dot{\theta}(t_0) = \omega_0$, there is
    a solution to the IVP which is global.

    <i class="fa fa-key"></i> **Hint.** Compute the derivative with respect to $t$ of
    $$
    E = \frac{1}{2} m\ell^2 \dot{\theta}^2 - m g \ell \cos \theta
    $$

<i class="fa fa-question-circle-o"></i> -- Existence / Linear Systems
--------------------------------------------------------------------------------

Let $A \in \mathbb{R}^{n \times n}$ and $x_0 \in \mathbb{R}^n$. Consider
  $$
  \dot{x} = A x \; \mbox{ and } \; x(0) = x_0
  $$

<i class="fa fa-bullseye"></i> **Aim.** Show that any maximal solution is global.


--------------------------------------------------------------------------------

  - [</i><i class="fa fa-superscript"></i>] 
    Show that $y(t) = \|x(t)\|^2$ is differentiable and 
    satisfies $y(t) \geq 0$ and 
    $\dot{y}(t) \leq \alpha y(t)$ for some $\alpha \geq 0$.

  - [</i><i class="fa fa-superscript"></i>]
    Compute the derivative of $y(t) e^{-\alpha t}$ and conclude that
    $0 \leq y(t) \leq y(0) e^{\alpha t}$.

  - [</i><i class="fa fa-superscript"></i>]
    Prove that any maximal solution $x(t)$ of the initial IVP is global.

Bad News (2/3)
--------------------------------------------------------------------------------

Uniqueness of solutions, even the maximal ones, is not granted either.

(Note: why does uniqueness of local solution does not make sense?)


<i class="fa fa-eye"></i> -- Non-Uniqueness
--------------------------------------------------------------------------------

The IVP 

$\dot{x} = \sqrt{x}$, $x(0) = 0$ 

has several maximal (global) solutions. 

Proof
--------------------------------------------------------------------------------

For any $\tau \geq 0$, $x_{\tau}$ is a solution:

$$
x_{\tau}(t) = 
\left| 
\begin{array}{ll}
0 & \mbox{if} \; t \leq \tau, \\
1/4 \times (t-\tau)^2 & \mbox{if} \; t > \tau.
\end{array}
\right.
$$

Good News (2/3)
--------------------------------------------------------------------------------

However, uniqueness of maximal solution holds under mild assumptions.


Notation -- Jacobian Matrix
--------------------------------------------------------------------------------

Let $x=(x_1, \dots, x_n)$ and $f(x) = (f_1(x), \dots, f_n(x))$.   
The **Jacobian matrix** of $f$ is defined as

$$
\frac{\partial f}{\partial x}
:=
\left[
  \begin{array}{ccc}
  \frac{\partial f_1}{\partial x_1} & \cdots & \frac{\partial f_1}{\partial x_n} \\
  \vdots & \vdots & \vdots \\
  \frac{\partial f_n}{\partial x_1} & \cdots & \frac{\partial f_n}{\partial x_n} \\
  \end{array}
\right]
$$

(when all the partial derivatives are defined).

Uniqueness
--------------------------------------------------------------------------------

If $\partial f/\partial x$ exists and is continuous,  
the maximal solution is unique.

Bad News (3/3)
--------------------------------------------------------------------------------

An infinitely small error in the initial value could result in a finite
error in the solution, even in finite time.

That would undermine the utility of any approximation method.


Definition -- Continuity
--------------------------------------------------------------------------------

Instead of denoting $x(t)$ the solution, use $x(t, x_0)$ to emphasize the
dependency w.r.t. the initial state.

**Continuity w.r.t. the initial state** means that
if $x(t, x_0)$ is defined on $[t_0, \tau]$ and $t\in [t_0, \tau]$:

$$
x(t, y) \to x(t, x_0) \; \mbox{when} \; y \to x_0
$$

and that this convergence is uniform w.r.t. $t$.

Good News (3/3)
--------------------------------------------------------------------------------

However, continuity wrt the initial value holds under mild assumptions.


Continuity
--------------------------------------------------------------------------------

Assume that $\partial f / \partial x$ exists and is continuous.  

Then the dynamical system is continous w.r.t. the initial state.


<i class="fa fa-eye"></i> Continuity / Prey-Predator
--------------------------------------------------------------------------------

    alpha = 2 / 3; beta = 4 / 3; delta = gamma = 1.0
    def f(t, y):
        x, y = y 
        u = alpha * x - beta * x * y
        v = delta * x * y - gamma * y
        return array([u, v])

--------------------------------------------------------------------------------

    tf = 3.0
    result = solve_ivp(f, t_span=[0.0, tf], y0=[1.5, 1.5], max_step=0.01)
    x = result["y"][0]
    y = result["y"][1]


<i class="fa fa-area-chart"></i>
--------------------------------------------------------------------------------

    def display_streamplot(): 
        ax = gca()
        xr = yr = linspace(0.0, 2.0, 1000)
        streamplot(*Q(lambda y: f(0,y), xr, yr), color="grey")

<i class="fa fa-area-chart"></i>
--------------------------------------------------------------------------------

    def display_reference_solution():
        ax = gca()
        for xy in zip(x, y):
            x_, y_ = xy
            ax.add_artist(Circle((x_, y_), 0.2, color="#d3d3d3"))
        ax.add_artist(Circle((x[0], y[0]), 0.1, color="#808080"))
        plot(x, y, "k")

<i class="fa fa-area-chart"></i>
--------------------------------------------------------------------------------

    def display_alternate_solution():
        result = solve_ivp(f, t_span=[0.0, tf], y0=[1.5, 1.575], max_step=0.01)
        x = result["y"][0]
        y = result["y"][1]
        plot(x, y, "k--")


<i class="fa fa-area-chart"></i>
--------------------------------------------------------------------------------

    figure()
    display_streamplot()
    display_reference_solution()
    display_alternate_solution()
    axis([0,2,0,2]); axis("square")

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    save("images/continuity")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/continuity.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


--------------------------------------------------------------------------------

### <i class="fa fa-question-circle-o"></i> -- Continuity / Initial Value

Let $h \geq 0$ and $x^h(t)$ be the solution of $\dot{x} = x$ 
and $x^h(0) = 1+ h$.

  - [<i class="fa fa-superscript"></i>]. Let $\epsilon > 0$ and $\tau \geq 0$; 
    find the smallest  $\delta > 0$ such that 
    $|h| < \delta$ ensures that
    $$\mbox{for any $t \in [t_0, \tau]$}, |x^{h}(t) - x^0(t)| < \epsilon$$

--------------------------------------------------------------------------------

  - [<i class="fa fa-superscript"></i>]. What is the behavior of
    $\delta$ when $\tau$ goes to infinity?


<i class="fa fa-question-circle-o"></i> -- Continuity / Initial Value
--------------------------------------------------------------------------------

Consider $\dot{x} = \sqrt{|x|}$, $x(0)=x_0$.

  - [<i class="fa fa-laptop"></i>]
    Solve numerically this IVP for $t \in [0,1]$ and $x_0 = 0$. 
    Then, solve it again for $x_0 = 0.1$, $x_0=0.01$, etc.

  - [<i class="fa fa-flask"></i>]
    Does the solution seem to be continuous with respect to the initial value?

  - [<i class="fa fa-lightbulb-o"></i>] 
    Explain this experimental result.


<i class="fa fa-question-circle-o"></i> -- Well-Posedness / Prey-Predator
--------------------------------------------------------------------------------

Let

$$
\begin{array}{rcl}
\dot{x} &=& \alpha x - \beta xy \\
\dot{y} &=& \delta x y - \gamma y \\
\end{array}
$$

with $\alpha = 2 / 3$, $\beta = 4 / 3$, $\delta = \gamma = 1.0$.

--------------------------------------------------------------------------------

  - [<i class="fa fa-lightbulb-o"></i>] Show that the system is well-posed.

  - [<i class="fa fa-lightbulb-o"></i>, <i class="fa fa-superscript"></i>]
    Show that if $x(0) > 0$ and $y(0) > 0$, the maximal solution is global.
    
    <i class="fa fa-key"></i> **Hint.** Compute
    $$
    d/dt(\delta x - \gamma \ln x +\beta y - \alpha \ln y)
    $$

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