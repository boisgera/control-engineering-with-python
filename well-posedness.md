---
title: Well-Posedness
author:
  - "🧙‍♂️ [Sébastien Boisgérault](sebastien.boisgerault@minesparis.psl.eu) -- 🏦 Mines Paris -- PSL"
licence:
  - "[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)"
---

## Control Engineering with Python

- ©️ License Creative Commons [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

- 🏠 [GitHub Homepage](https://github.com/boisgera/control-engineering-with-python>)

## Notations

|     |             |     |                        |
| --- | ----------- | --- | ---------------------- |
| 🐍  | Code        | 🔍  | Example                |
| 📈  | Graph       | 🧩  | Exercise               |
| 🏷️  | Definition  | 💻  | Computation (Computer) |
| 💎  | Theorem     | 🧮  | Computation (Hand)     |
| 📝  | Remark      | 🧠  | Theory                 |
| ℹ️  | Information | 🗝️  | Hint                   |
| ⚠️  | Warning     | 🔓  | Solution               |

## 🐍 Imports

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
from numpy import *
from numpy.linalg import *
from scipy.integrate import solve_ivp
from matplotlib.pyplot import *
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

## 🏷️ Well-Posedness

Make sure that a system is "sane" (not "pathological"):

**Well-Posedness:**

- **Existence** +
- **Uniqueness** +
- **Continuity**.

We will define and study each one in the sequel.

## 🔍 Local vs Global

So far, we have only dealt with **global** solutions $x(t)$ of IVPs,
defined for any $t \geq t_0$.

This concept is sometimes too stringent.

---

Consider for example:

$\dot{x} = x^2$ and $x(0)=1.$

---

### 🐍 💻 📈

```python
def fun(t, y):
    return y * y
t0, tf, y0 = 0.0, 3.0, array([1.0])
result = solve_ivp(fun, t_span=[t0, tf], y0=y0)
figure()
plot(result["t"], result["y"][0], "k")
xlim(t0, tf); xlabel("$t$"); ylabel("$x(t)$")
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/finite-time-blowup")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/finite-time-blowup.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

---

### 🏷️ Local vs Global

Ouch.

There is actually no **global** solution.

However there is **local** solution $x(t)$,
defined for $t \in \left[t_0, \tau\right[$
for some $\tau > t_0$.

---

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

---

### 🐍 💻 📈

```python
tf = 1.0
r = solve_ivp(fun, [t0, tf], y0,
              dense_output=True)
figure()
t = linspace(t0, tf, 1000)
plot(t, r["sol"](t)[0], "k")
ylim(0.0, 10.0); grid();
xlabel("$t$"); ylabel("$x(t)$")
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/finite-time-blowup-2")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/finite-time-blowup-2.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

---

This local solution is also **maximal**:

You cannot extend this solution beyond $\tau=1.0$.

## 🏷️ Maximal Solution

A (local) solution $x :[0, \tau[$ to an IVP is **maximal** if there is no other
solution

- defined on $[0, \tau'[$ with $\tau' > \tau$,

- whose restriction to $[0, \tau[$ is $x$.

## 🧩 Maximal Solutions

### 1. 🧮

Find a solution $x(t)$ of

$$
\dot{x} = x^2, \; x(0) \neq 0.
$$

🗝️ **Hint:** assume that $x(t) \neq 0$ then compute

$$
\frac{d}{dt} \frac{1}{x(t)}.
$$

---

### 2. 🧠

Make sure that your solution is maximal.

## 🔓 Maximal Solutions

### 1. 🔓

As long as $x(t) \neq 0$,

$$
\frac{d}{dt} \frac{1}{x} =
- \frac{\dot{x}}{x^2} = 1.
$$

---

By integration, this leads to

$$
\frac{1}{x(t)} - \frac{1}{x(0)} = -t
$$

and thus provides

$$
x(t) = \frac{1}{\frac{1}{x(0)} - t} = \frac{x(0)}{1 - x(0) t}.
$$

which is indeed a solution as long as the denominator is not zero.

---

### 2. 🔓

If $x(0) < 0$, this solution is valid for all $t\geq 0$ and thus maximal.

If $x(0) > 0$, the solution is defined until $t=1/x(0)$ where it blows up.
Thus, this solution is also maximal.

## 🙁 Bad News (1/3)

Sometimes things get worse than simply having no global solution.

## 🔍 No Local Solution

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

## 📈 No Local Solution

```python
def f(x1x2):
    x1, x2 = x1x2
    dx1 = 1.0 if x1 < 0.0 else -1.0
    return array([dx1, 0.0])
figure()
x1 = x2 = linspace(-1.0, 1.0, 20)
gca().set_aspect(1.0); grid(True)
quiver(*Q(f, x1, x2), color="k")
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/discont")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/discont.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## 🧠 No Local Solution

This system has no solution, not even a local one, when $x(0) = (0,0)$.

## Proof

- Assume that $x: [0, \tau[ \to \mathbb{R}$ is a local solution.

- Since $\dot{x}(0) = -1 < 0$,
  for some small enough $0 < \epsilon < \tau$ and any
  $t \in \left]0, \epsilon\right]$, we have $x(t) < 0$.

- Consequently, $\dot{x}(t) = +1$ and thus by integration

  $$
  x(\epsilon) = x(0) + \int_0^{\epsilon} \dot{x}(t) \, dt = \epsilon > 0,
  $$

which is a contradiction.

## 🙂 Good News (1/3)

However, a local solution exists under very mild assumptions.

## 💎 Existence

If $f$ is continuous,

- There is a (at least one) **local** solution to the IVP

  $\dot{x} = f(x)$ and $x(t_0) = x_0$.

- Any local solution on some $\left[t_0, \tau \right[$
  can be extended to a (at least one) **maximal** one
  on some $\left[t_0, t_{\infty}\right[$.

**📝 Note:** a maximal solution is **global** iff $t_{\infty} = +\infty$.

## 💎 Maximal Solutions

A solution on $\left[t_0, \tau \right[$ is maximal if and only if either

- $\tau = +\infty$ : the solution is global, or

- $\tau < +\infty$ and $\displaystyle \lim_{t \to \tau} \|x(t)\| = +\infty.$

In plain words : a non-global solution cannot be extended further in time
if and only if it "blows up".

## 💎 Corollary

Let's assume that a local maximal solution exists.

You wonder if this solution is defined in $[t_0, t_f[$ or blows up before $t_f$.

For example, you wonder if a solution is global
(if $t_f = +\infty$ or $t_f < +\infty$.)

## 🧠 Prove existence

**TODO.** Show that any solution which defined on some
sub-interval $[t_0, \tau]$ with $\tau < t_f$ would is bounded.

Then, no solution can be maximal on any
such $[0, \tau[$ (since it doesn't blow up !). Since a maximal
solution does exist, its domain is $[0, t_{\infty}[$ with $t_{\infty} \geq t_f$.

**$\Rightarrow$ a solution is defined on $[t_0, t_f[$.**

## 🧩 Sigmoid

Consider the dynamical system

$$
\dot{x} = \sigma(x) := \frac{1}{1 + e^{-x}}.
$$

---


::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
def sigma(x):
  return 1 / (1 + exp(-x))
figure()
x = linspace(-7.0, 7.0, 1000)
xlim(-5, 5)
plot(x, sigma(x), color="k", label="$y=\sigma(x)$")
xticks([-5.0, 0.0, 5.0])
yticks([0.0, 0.5, 1.0])
xlabel("$x$")
ylabel("$y$")
legend()
pp.gcf().subplots_adjust(bottom=0.2)
save("images/sigmoid")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/sigmoid.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

---

### 1. 🧮 Existence

Show that there is a (at least one) maximal solution to each initial condition.

---

### 2. 🧮 Global

Show that any such solution is global.

---

## 🔓 Sigmoid

---

### 1. 🔓 Existence

The sigmoid function $\sigma$ is continuous.

Consequently, [💎 Existence] proves the existence of a (at least one)
maximal solution.

---

### 2. 🔓 Global

Let $x: \left[0, \tau \right[ \to \mathbb{R}$ be a maximal solution to the IVP.
We have

$$
0 \leq \dot{x}(t) = \sigma(x(t)) \leq 1, \; 0 \leq t < \tau
$$

and by integration,

$$
|x(t)| \leq |x(0)| + t
$$

Thus, it cannot blow-up in finite time; by [💎 Maximal Solutions], it is global.



## 🧩 Pendulum

Consider the pendulum, subject to a torque $c$

$$
ml^2 \ddot{\theta} + b \dot{\theta} + mg \ell \sin \theta = c(\theta, \dot{\theta})
$$

We assume that the torque provides a bounded power:

$$
P = c(\theta, \dot{\theta}) \dot{\theta} \leq M < +\infty.
$$

---

**Q1 🧮.**

Show that for any initial condition $t_0$,
$\theta(t_0) = \theta_0$ and $\dot{\theta}(t_0) = \omega_0$, there is
a solution to the IVP which is global.

🗝️ **Hint.** Compute the derivative with respect to $t$ of

$$
E = \frac{1}{2} m\ell^2 \dot{\theta}^2 - m g \ell \cos \theta
$$

## 🧩 Linear Systems

Let $A \in \mathbb{R}^{n \times n}$ and $x_0 \in \mathbb{R}^n$. Consider

$$
\dot{x} = A x \; \mbox{ and } \; x(0) = x_0
$$

---

**Q1 🧮.** Show that $y(t) = \|x(t)\|^2$ is differentiable and
satisfies $y(t) \geq 0$ and
$\dot{y}(t) \leq \alpha y(t)$ for some $\alpha \geq 0$.

**Q2 🧮.** Compute the derivative of $y(t) e^{-\alpha t}$ and conclude that
$0 \leq y(t) \leq y(0) e^{\alpha t}$.

**Q3 🧮.** Prove that any maximal solution $x(t)$ of the initial IVP is global.

## 🏷️ Uniqueness

In the current context, **uniqueness** means uniqueness of the maximal solution
to an IVP.

(why does uniqueness of local solution does not make sense?)

## 🙁 Bad News (2/3)

Uniqueness of solutions, even the maximal ones, is not granted either.

## 🔍 Non-Uniqueness

The IVP

$$\dot{x} = \sqrt{x}, \;x(0) = 0$$

has several maximal (global) solutions.

## Proof

For any $\tau \geq 0$, $x_{\tau}$ is a solution:

$$
x\_{\tau}(t) =
\left|
\begin{array}{ll}
0 & \mbox{if} \; t \leq \tau, \\
1/4 \times (t-\tau)^2 & \mbox{if} \; t > \tau.
\end{array}
\right.
$$

## 🙂 Good News (2/3)

However, uniqueness of maximal solution holds under mild assumptions.

## 🏷️ Jacobian Matrix

$$
x=(x_1, \dots, x_n), \;f(x) = (f_1(x), \dots, f_n(x)).
$$

**Jacobian matrix** of $f$:

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

## 💎 Uniqueness

If $\partial f/\partial x$ exists and is continuous,
the maximal solution is unique.

## 🙁 Bad News (3/3)

An infinitely small error in the initial value could result in a finite
error in the solution, even in finite time.

That would severely undermine the utility of any approximation method.

## 🏷️ Continuity

Instead of denoting $x(t)$ the solution, use $x(t, x_0)$ to emphasize the
dependency w.r.t. the initial state.

**Continuity w.r.t. the initial state** means that
if $x(t, x_0)$ is defined on $[t_0, \tau]$ and $t\in [t_0, \tau]$:

$$
x(t, y) \to x(t, x_0) \; \mbox{when} \; y \to x_0
$$

and that this convergence is uniform w.r.t. $t$.

## 🙂 Good News (3/3)

However, continuity w.r.t. the initial value holds under mild assumptions.

## 💎 Continuity

Assume that $\partial f / \partial x$ exists and is continuous.

Then the dynamical system is continous w.r.t. the initial state.

## 🔍 Prey-Predator

Let

$$
\begin{array}{rcl}
\dot{x} &=& \alpha x - \beta xy \\
\dot{y} &=& \delta x y - \gamma y \\
\end{array}
$$

with $\alpha = 2 / 3$, $\beta = 4 / 3$, $\delta = \gamma = 1.0$.

## 🐍

```python
alpha = 2 / 3; beta = 4 / 3; delta = gamma = 1.0

def f(t, y):
    x, y = y
    u = alpha * x - beta * x * y
    v = delta * x * y - gamma * y
    return array([u, v])
```

## 💻

```python
tf = 3.0
result = solve_ivp(f, t_span=[0.0, tf], y0=[1.5, 1.5], max_step=0.01)
x = result["y"][0]
y = result["y"][1]
```

## 📈

```python
def display_streamplot():
    ax = gca()
    xr = yr = linspace(0.0, 2.0, 1000)
    streamplot(*Q(lambda y: f(0,y), xr, yr), color="grey")
```

## 📈

```python
def display_reference_solution():
    ax = gca()
    for xy in zip(x, y):
        x_, y_ = xy
        ax.add_artist(Circle((x_, y_), 0.2, color="#d3d3d3"))
    ax.add_artist(Circle((x[0], y[0]), 0.1, color="#808080"))
    plot(x, y, "k")
```

## 📈

```python
def display_alternate_solution():
    result = solve_ivp(f, t_span=[0.0, tf], y0=[1.5, 1.575], max_step=0.01)
    x = result["y"][0]
    y = result["y"][1]
    plot(x, y, "k--")
```

## 📈

```python
figure()
display_streamplot()
display_reference_solution()
display_alternate_solution()
axis([0,2,0,2]); axis("square")
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    save("images/continuity")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/continuity.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

---

## 🧩 Continuity

Let $h \geq 0$ and $x^h(t)$ be the solution of

$$\dot{x} = x, \; x^h(0) = 1+ h.$$

**Q1 🧮.** Let $\epsilon > 0$ and $\tau \geq 0$;
find the smallest $\delta > 0$ such that
$|h| < \delta$ ensures that
$$\mbox{for any $t \in [t_0, \tau]$}, |x^{h}(t) - x^0(t)| < \epsilon$$

**Q2 🧮.** What is the behavior of $\delta$ when $\tau$ goes to infinity?

## 🧩 Continuity Issues

Consider
$$\dot{x} = \sqrt{|x|}, \; x(0)=x_0.$$

**Q1 💻.** Solve numerically this IVP for $t \in [0,1]$ and $x_0 = 0$.
Then, solve it again for $x_0 = 0.1$, $x_0=0.01$, etc.

---

**Q2 🔬.**
Does the solution seem to be continuous with respect to the initial value?

**Q3 🧠.**
Explain this experimental result.

## 🧩 Prey-Predator

Let

$$
\begin{array}{rcl}
\dot{x} &=& \alpha x - \beta xy \\
\dot{y} &=& \delta x y - \gamma y \\
\end{array}
$$

with $\alpha = 2 / 3$, $\beta = 4 / 3$, $\delta = \gamma = 1.0$.

---

**Q1 🧠.** Show that the system is well-posed.

**Hint 🗝️.** Compute

$$
d/dt(\delta x - \gamma \ln x +\beta y - \alpha \ln y)
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
$$
