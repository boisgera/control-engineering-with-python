% Optimal Control
% 👤 [Sébastien Boisgérault](mailto:Sebastien.Boisgerault@mines-paristech.fr),
🏦 MINES ParisTech, PSL University
% ©️ [CC-BY 4.0 International](https://creativecommons.org/licenses/by/4.0/)

## 🐍 Imports

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
from numpy import *
from numpy.linalg import *
from numpy.testing import *
from scipy.linalg import *
from scipy.integrate import *
from matplotlib.pyplot import *
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

<!--

🐍 Streamplot Helper
--------------------------------------------------------------------------------

``` python
def Q(f, xs, ys):
    X, Y = meshgrid(xs, ys)
    v = vectorize
    fx = v(lambda x, y: f([x, y])[0])
    fy = v(lambda x, y: f([x, y])[1])
    return X, Y, fx(X, Y), fy(X, Y)
```

-->

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

## Why Optimal Control?

**Limitations of Pole Assignment**

- It is not always obvious what set of poles we should target
  (especially for large systems),

- We do not control explicitly the trade-off between "speed of convergence"
  and "intensity of the control" (large input values maybe costly or
  impossible).

---

Let

$$\dot{x} = A x + Bu$$

where

- $A \in \mathbb{R}^{n\times n}$, $B \in \mathbb{R}^{m\times n}$ and

- $x(0) = x_0 \in \mathbb{R}^n$ is given.

---

Find $u(t)$ that minimizes

$$
J = \int_0^{+\infty} x(t)^t Q x(t) + u(t)^t R u(t) \, dt
$$

where:

- $Q \in \mathbb{R}^{n \times n}$ and $R \in \mathbb{R}^{m\times m}$,

- (to be continued ...)

---

- $Q$ and $R$ are **symmetric** ($R^t = R$ and $Q^t = Q$),

- $Q$ and $R$ are **positive definite** (denoted "$>0$")

  $$x^t Q x \geq 0 \, \mbox{ and } \, x^t Q x = 0 \, \mbox{ iff }\, x=0$$

  and

  $$u^t R u \geq 0 \, \mbox{ and } \, u^t R u = 0 \, \mbox{ iff }\, u=0.$$

## Heuristics / Scalar Case

If $x \in \mathbb{R}$ and $u \in \mathbb{R}$,

$$
J = \int_0^{+\infty} q x(t)^2 + r u(t)^2 \, dt
$$

with $q > 0$ and $r > 0$.

---

When we minimize $J$:

- Only the relative values of $q$ and $r$ matters.

- Large values of $q$ penalize strongly non-zero states:

  $\Rightarrow$ fast convergence.

- Large values of $r$ penalize strongly non-zero inputs:

  $\Rightarrow$ small input values.

## Heuristics / Vector Case

If $x \in \mathbb{R}^n$ and $u \in \mathbb{R}^m$ and $Q$ and $R$ are
diagonal,

$$
Q = \mathrm{diag}(q_1, \cdots, q_n), \; R=\mathrm{diag}(r_1, \cdots, r_m),
$$

$$
J = \int_0^{+\infty} \sum_{i} q_i x_i(t)^2 + \sum_j r_j u_j(t)^2 \, dt
$$

with $q_i > 0$ and $r_j > 0$.

Thus we can control the cost of each component of $x$ and $u$ independently.

## 💎 Optimal Solution

Assume that $\dot{x} = A x + Bu$ is controllable.

- There is an optimal solution; it is a linear feedback

  $$u = - K x$$

- The closed-loop dynamics is asymptotically stable.

## 💎 Algebraic Riccati Equation

- The gain matrix $K$ is given by

  $$
  K = R^{-1} B^t \Pi,
  $$

  where $\Pi \in \mathbb{R}^{n \times n}$ is the unique matrix such that
  $\Pi^t = \Pi$, $\Pi > 0$ and

  $$
  \Pi B R^{-1} B^t \Pi - \Pi A - A^t \Pi - Q = 0.
  $$

## 🔎 Asymp. Stab. / Optimal Control

Consider the double integrator $\ddot{x} = u$

$$
\frac{d}{dt}
\left[\begin{array}{c} x \\ \dot{x} \end{array}\right]
=
\left[\begin{array}{cx} 0 & 1 \\ 0 & 0\end{array}\right]
\left[\begin{array}{c} x \\ \dot{x} \end{array}\right]
+
\left[\begin{array}{c} 0 \\ 1 \end{array}\right]
u
$$

(in standard form)

## 🐍 Problem Data

```python
A = array([[0, 1], [0, 0]])
B = array([[0], [1]])
Q = array([[1, 0], [0, 1]])
R = array([[1]])
```

## 🐍 Optimal Gain

```python
Pi = solve_continuous_are(A, B, Q, R)
K = inv(R) @ B.T @ Pi
```

## 🐍 Closed-Loop Asymp. Stab.

```python
eigenvalues, _ = eig(A - B @ K)
assert all([real(s) < 0 for s in eigenvalues])
```

## 📊 Eigenvalues Location

```python
figure()
x = [real(s) for s in eigenvalues]
y = [imag(s) for s in eigenvalues]
plot(x, y, "kx", ms=12.0)
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
xticks(arange(-5, 6)); yticks(arange(-5, 6))
plot([0, 0], [-5, 5], "k")
plot([-5, 5], [0, 0], "k")
grid(True)
title("Eigenvalues")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    axis("square")
    axis([-5, 5, -5, 5])
    save("images/poles-LQ")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/poles-LQ.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## 🐍 Simulation

```python
y0 = [1.0, 1.0]
def f(t, x):
    return (A - B @ K) @ x
```

## 🐍 Simulation

```python
result = solve_ivp(
  f, t_span=[0, 10], y0=y0, max_step=0.1
)
t = result["t"]
x1 = result["y"][0]
x2 = result["y"][1]
u = - (K @ result["y"]).flatten() # vect. -> scalar
```

## 📊 Input & State Evolution

```python
width = 160 / 9
height = width / (16 / 9)
figure(figsize=(width, height))
plot(t, x1, label="$x_1$")
plot(t, x2, label="$x_2$")
plot(t, u, label="$u$")
xlabel("$t$")
legend(loc="lower right")
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/poles-LQ-traj")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/poles-LQ-traj.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## 🐍 Optimal Gain

```python
Q = array([[10, 0], [0, 10]])
R = array([[1]])
Pi = solve_continuous_are(A, B, Q, R)
K = inv(R) @ B.T @ Pi
```

## 🐍 Closed-Loop Asymp. Stab.

```python
eigenvalues, _ = eig(A - B @ K)
assert all([real(s) < 0 for s in eigenvalues])
```

## 📊 Eigenvalues Location

```python
figure()
x = [real(s) for s in eigenvalues]
y = [imag(s) for s in eigenvalues]
plot(x, y, "kx", ms=12.0)
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
xticks(arange(-5, 6)); yticks(arange(-5, 6))
plot([0, 0], [-5, 5], "k")
plot([-5, 5], [0, 0], "k")
grid(True)
title("Eigenvalues")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    axis("square")
    axis([-5, 5, -5, 5])
    save("images/poles-LQ-2")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/poles-LQ-2.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## 🐍 Simulation

```python
result = solve_ivp(
  f, t_span=[0, 10], y0=y0, max_step=0.1
)
t = result["t"]
x1 = result["y"][0]
x2 = result["y"][1]
u = - (K @ result["y"]).flatten() # vect. -> scalar
```

## 📊 Input & State Evolution

```python
width = 160 / 9
height = width / (16 / 9)
figure(figsize=(width, height))
plot(t, x1, label="$x_1$")
plot(t, x2, label="$x_2$")
plot(t, u, label="$u$")
xlabel("$t$")
legend(loc="lower right")
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/poles-LQ-2-traj")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/poles-LQ-2-traj.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## 🐍 Optimal Gain

```python
Q = array([[1, 0], [0, 1]])
R = array([[10]])
Pi = solve_continuous_are(A, B, Q, R)
K = inv(R) @ B.T @ Pi
```

## 🐍 Closed-Loop Asymp. Stab.

```python
eigenvalues, _ = eig(A - B @ K)
assert all([real(s) < 0 for s in eigenvalues])
```

## 📊 Eigenvalues Location

```python
figure()
x = [real(s) for s in eigenvalues]
y = [imag(s) for s in eigenvalues]
plot(x, y, "kx", ms=12.0)
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
xticks(arange(-5, 6)); yticks(arange(-5, 6))
plot([0, 0], [-5, 5], "k")
plot([-5, 5], [0, 0], "k")
grid(True)
title("Eigenvalues")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    axis("square")
    axis([-5, 5, -5, 5])
    save("images/poles-LQ-3")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/poles-LQ-3.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## 🐍 Simulation

```python
result = solve_ivp(
  f, t_span=[0, 10], y0=y0, max_step=0.1
)
t = result["t"]
x1 = result["y"][0]
x2 = result["y"][1]
u = - (K @ result["y"]).flatten() # vect. -> scalar
```

## 📊 Input & State Evolution

```python
width = 160 / 9
height = width / (16 / 9)
figure(figsize=(width, height))
plot(t, x1, label="$x_1$")
plot(t, x2, label="$x_2$")
plot(t, u, label="$u$")
xlabel("$t$")
legend(loc="lower right")
```

---

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/poles-LQ-3-traj")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/poles-LQ-3-traj.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## 🧩 Optimal Value

Consider the controllable dynamics

$$
\dot{x} = A x + Bu
$$

and $u(t)$ the control that minimizes

$$
J = \int_{0}^{+\infty}  x(t)^t Q x(t) + u(t)^t R u(t) \, dt.
$$

---

Let

$$
j(x, u) := x^tQ x + u^t R u.
$$

**Q1 🧮.** Show that

$$
j(x(t), u(t)) = - \frac{d}{dt} x(t)^t \Pi x(t)
$$

**Q2 🧮.** What is the value of $J$?

---

## 🔒 Optimal Value

**Q1.**
We know that $u = -Kx$ where $K = R^{-1} B^t \Pi$
and $\Pi$ is a symmetric solution of

$$
\Pi BR^{-1} B^t \Pi - \Pi A - A^t \Pi - Q = 0.
$$

Since $R$ is symmetric,

$$
\Pi BR^{-1} B^t \Pi = \Pi B(R^{-1})^tR R^{-1} B^t \Pi = K^t R K
$$

and thus $$\Pi A + A^t \Pi = K^t R K - Q.$$

---

Since $\dot{x} = (A - B K ) x$,

$$
\begin{split}
\frac{d}{dt} x^t \Pi x &= x^t (\Pi (A - BK) + (A - BK)^t \Pi) x \\
& = x^t (\Pi A + A^t \Pi - \Pi BK - (BK)^t \Pi) x \\
& = x^t ( K^t R K - Q - K^t R K - K^t R K) x \\
& = x^t (- Q - K^t R K ) x^t \\
& = - x^t Q x - u^t R u \\
& = -j(x, u).
\end{split}
$$

---

**Q2.** Since the system is controllable, the optimal control makes the
origin of the closed-loop system asymptotically stable. Consequently,
$x(t) \to 0$ when $t \to +\infty$. Hence,

$$
\begin{split}
J &= \int_0^{+\infty} j(x, u) \, dt \\
  &= - \int_0^{+\infty} \frac{d}{dt} x^t \Pi x \, dt \\
  &= - \left[x^t \Pi x\right]_0^{+\infty} \\
  & = x(0)^t \Pi x(0).
\end{split}
$$

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
