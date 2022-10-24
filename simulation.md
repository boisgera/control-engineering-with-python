% Simulation
% 👤 [Sébastien Boisgérault](sebastien.boisgerault@minesparis.psl.eu) 


### Control Engineering with Python

- 📖 [Documents (GitHub)](https://github.com/boisgera/control-engineering-with-python)

- ©️ [License CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

- 🏦 [Mines ParisTech, PSL University](https://mines-paristech.eu/)



## Symbols

|     |             |     |                        |
| --- | ----------- | --- | ---------------------- |
| 🐍  | Code        | 🔍  | Example                |
| 📈  | Graph       | 🧩  | Exercise               |
| 🏷️  | Definition  | 💻  | Computation (Computer) |
| 💎  | Theorem     | 🧮  | Computation (By Hand)  |
| 📝  | Remark      | 🧠  | Theory                 |
| ℹ️  | Information | 🗝️  | Hint                   |
| ⚠️  | Warning     | 🔓  | Solution               |


## 🐍 Imports

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
from numpy import *
from numpy.linalg import *
from matplotlib.pyplot import *
from mpl_toolkits.mplot3d import *
```

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

    width

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## 🐍 Stream Plot Helper

```python
def Q(f, xs, ys):
    X, Y = meshgrid(xs, ys)
    fx = vectorize(lambda x, y: f([x, y])[0])
    fy = vectorize(lambda x, y: f([x, y])[1])
    return X, Y, fx(X, Y), fy(X, Y)
```

## 🏷️ Simulation

Numerical approximation solution $x(t)$ to the IVP

$$
\dot{x} = f(x), \; x(t_0) = x_0
$$

on some finite **time span** $[t_0, t_f]$.

## 🏷️ Euler Scheme

Pick a (small) fixed **time step** $\Delta t > 0$.

Then use repeatedly the approximation:

$$
\begin{split}
x(t + \Delta t)
  & \simeq x(t) + \Delta t \times \dot{x}(t) \\
  & = x(t) + \Delta t \times f(x(t)) \\
x(t + 2\Delta t)
  & \simeq x(t+\Delta t) + \Delta t \times \dot{x}(t+ \Delta t) \\
  & = x(t+\Delta t) + \Delta t \times f(x(t+\Delta t)) \\
x(t+3\Delta t)
  & \simeq \cdots
\end{split}
$$

to compute a sequence of states $x_k \simeq x(t+k \Delta t)$.


## 🐍 Euler Scheme

```python
def basic_solve_ivp(f, t_span, y0, dt=1e-3):
    t0, t1 = t_span
    ts, xs = [t0], [y0]
    while ts[-1] < t1:
        t, x = ts[-1], xs[-1]
        t_next, x_next = t + dt, x + dt * f(x)
        ts.append(t_next); xs.append(x_next)
    return (array(ts), array(xs).T)
```

## 📖 Usage - Arguments

- `f`, vector field ($n$-dim $\to$ $n$-dim),

- `t_span`, time span `(t0, t1)`,

- `y0`, initial state ($n$-dim),

- `dt`, time step.

## 📖 Usage - Returns

- `t`, 1-dim array

  `t = [t0, t0 + dt, ...]`.

- `x`, 2-dim array, shape `(n, len(t))`

  `x[i][k]`: value of `x_i(t_k)`.

## 🔍 Rotation

$$
\left|
\begin{split}
\dot{x}_1 &= -x_2 \\
\dot{x}_2 &= +x_1
\end{split}
\right.
\;\; \mbox{ with } \;\;
\left|
\begin{array}{l}
x_1(0) = 1\\
x_2(0) = 0
\end{array}
\right.
$$

-----

### 🐍 💻

```python
def f(x):
    x1, x2 = x
    return array([-x2, x1])
t0, t1 = 0.0, 5.0
y0 = array([1.0, 0.0])

t, x = basic_solve_ivp(f, (t0, t1), y0)
```

## 📈 Trajectories

```python
figure()
plot(t, x[0], label="$x_1$")
plot(t, x[1], label="$x_2$")
grid(True)
xlabel("time $t$")
legend()
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/rotation")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/rotation.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

------

### 📈 Trajectories (State Space)

Display a set of solutions in the background

```python
figure()
xs = linspace(-3.0, 3.0, 50)
ys = linspace(-1.5, 1.5, 50)
streamplot(*Q(f, xs, ys), color="lightgrey")
```

------------

### 📈...

```python
x1, x2 = x[0], x[1]
plot(x1, x2, "k");
plot(x1[0], x2[0], "ko")
dx1, dx2 = x1[-1] - x1[-2], x2[-1] - x2[-2]
arrow(
    x1[-1], x2[-1], dx1, dx2,
    width=0.02, color="k", zorder=10)
grid(); axis("equal")
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/rotation2")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/rotation2.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## ⚠️ Don't do this at home!

Now that you understand the basics

- ☠️ **Do NOT use this basic solver (anymore)!**

- ☠️ **Do NOT roll your own ODE solver !**

Instead

- ❤️ **Use a feature-rich and robust solver.**

(Solvers are surprisingly hard to get right.)

## 📖 Scipy Integrate

For example, use:

```python
from scipy.integrate import solve_ivp
```

📖 Documentation: [`solve_ivp`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html)

**Features:** time-dependent vector field, error control, dense outputs, multiple
integration schemes, etc.


## 🔍 Rotation

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

---------------------

### 🐍 Rotation

```python
def fun(t, y):
    x1, x2 = y
    return array([-x2, x1])
t_span = [0.0, 2*pi]
y0 = [1.0, 0.0]
result = solve_ivp(fun=fun, t_span=t_span, y0=y0)
```

-----------------------

### ⚠️ Non-Autonomous Systems

The solver is designed for time-dependent systems:

$$
\dot{x} = f(t, x)
$$

The `t` argument in the definition of `fun` is mandatory,
even if the returned value doesn't depend on it (when the system is
effectively time-invariant).

----------------------------

### 🐍 Result "Bunch"

The `result` is a dictionary-like object with attributes:

- `t` : array, time points, shape `(n_points,)`,

- `y` : array, values of the solution at t, shape `(n, n_points)`,

- ...

(See 📖 [`solve_ivp` documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html))

-----------------------------

### 🐍

```python
rt = result["t"]
x1 = result["y"][0]
x2 = result["y"][1]
```

----------------------

### 📈

```python
figure()
t = linspace(0, 2*pi, 1000)
plot(t, cos(t), "k--")
plot(t, sin(t), "k--")
plot(rt, x1, ".-", label="$x_1(t)$")
plot(rt, x2, ".-", label="$x_2(t)$")
xlabel("$t$"); grid(); legend()
```


::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/solve_ivp_1")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/solve_ivp_1.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::



## Variable Step Size

The step size is:

- **variable**: $t_{n+1} - t_n$ may not be constant,

- **automatically selected** by the solver,

The solver shall meet the user specification,
but should select the largest step size to do so
to minimize the number of computations.

Optionally, you can specify a `max_step` (default: $+\infty$).

## Error Control

We generally want to control the (local) error $e(t)$:
the difference between the numerical solution and the exact one.

- `atol` is the **absolute tolerance** (default: $10^{-6}$),

- `rtol` is the **relative tolerance** (default: $10^{-3}$).

The solver ensures (approximately) that at each step:

$$
|e(t)| \leq \mathrm{atol} + \mathrm{rtol} \times |x(t)|
$$

-----

### 🐍 Solver Options

**Example:**

```python
options = {
    # at least 20 data points
    "max_step": 2*pi/20,
    # standard absolute tolerance
    "atol"    : 1e-6,
    # very large relative tolerance
    "rtol"    : 1e9
}
```

----------------

### 🐍 Simulation

```python
result = solve_ivp(
    fun=fun, t_span=t_span, y0=y0,
    **options
)
rt = result["t"]
x1 = result["y"][0]
x2 = result["y"][1]
```

------------------

### 📈 Graph

```python
figure()
t = linspace(0, 2*pi, 20)
plot(t, cos(t), "k--")
plot(t, sin(t), "k--")
plot(rt, x1, ".-", label="$x_1(t)$")
plot(rt, x2, ".-", label="$x_2(t)$")
xlabel("$t$"); grid(); legend()
```


::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/solve_ivp_2")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/solve_ivp_2.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

----------

### Dense Outputs

Using a small `max_step` is usually the wrong way to "get more data points"
since this will trigger many (potentially expensive) evaluations of `fun`.

Instead, use dense outputs: the solver may return
the discrete data `result["t"]` and `result["y"]`
**and** an approximate
solution `result["sol"]` **as a function of `t`**
with little extra computations.

-------------

### 🐍 Solver Options

```python
options = {
    "dense_output": True
}
```

------------

### 🐍 Simulation

```python
result = solve_ivp(
    fun=fun, t_span=t_span, y0=y0,
    **options
)
rt = result["t"]
x1 = result["y"][0]
x2 = result["y"][1]
sol = result["sol"]
```
-----------------

### 📈 Graph

```python
figure()
t = linspace(0, 2*pi, 1000)
plot(t, sol(t)[0], "-", label="$x_1(t)$")
plot(t, sol(t)[1], "-", label="$x_2(t)$")
plot(rt, x1, ".", color="C0")
plot(rt, x2, ".", color="C1")
xlabel("$t$"); grid(); legend()
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/solve_ivp_3")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/solve_ivp_3.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

<style>

.reveal p {
  text-align: left;
}

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
background: white;
font-size: 1.5em;
line-height: 1.5em;
/_ max-height: 80wh; won't work, overriden _/
}

/_
.reveal .slides .left {
text-align: left;
}
_/

input {
font-family: "Source Sans Pro", Helvetica, sans-serif;
font-size: 42px;
line-height: 54.6px;
}

code span.kw {
color: inherit;
font-weight: normal;
}

code span.cf { /_ return _/
color: inherit;
font-weight: normal;
}

code span.fl { /_ floats _/
color: inherit;
}

code span.dv { /_ ints _/
color: inherit;
}

code span.co { /_ comments _/
font-style: normal;
color: #adb5bd; /_ gray 5 _/}

code span.st { /_ strings _/
color: inherit;
}

code span.op { /_ +, = _/
color: inherit;
}

/*** Details ******************************************************************/
details h1, details h2, details h3{
  display: inline;
}


details summary {
  cursor: pointer;
  list-style: '🔒 ';
}

details[open] summary {
  cursor: pointer;
  list-style: '🔓 ';
}

summary::-webkit-details-marker {
  display: none
}


details[open] summary ~ * {
  animation: sweep .5s ease-in-out;
}
@keyframes sweep {
  0%    {opacity: 0}
  100%  {opacity: 1}
}


</style>

<link href="https://fonts.googleapis.com/css?family=Inconsolata:400,700" rel="stylesheet">

<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.css" rel="stylesheet">
