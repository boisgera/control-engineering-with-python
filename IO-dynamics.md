% I/O Behavior
% 👤 [Sébastien Boisgérault](sebastien.boisgerault@minesparis.psl.eu) 


### Control Engineering with Python

- 📖 [Documents (GitHub)](https://github.com/boisgera/control-engineering-with-python)

- ©️ [License CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

- 🏦 [Mines ParisTech, PSL University](https://mines-paristech.eu/)



## Symbols

|     |             |     |                        |
| --- | ----------- | --- | ---------------------- |
| 🐍  | Code        | 🔍  | Worked Example         |
| 📈  | Graph       | 🧩  | Exercise               |
| 🏷️  | Definition  | 💻  | Numerical Solution     |
| 💎  | Theorem     | 🧮  | Analytical Solution    |
| 📝  | Remark      | 🧠  | Theory                 |
| ℹ️  | Information | 🗝️  | Hint                   |
| ⚠️  | Warning     | 🔓  | Solution               |




## 🐍 Imports

```python
from numpy import *
from numpy.linalg import *
from scipy.linalg import *
from matplotlib.pyplot import *
from mpl_toolkits.mplot3d import *
from scipy.integrate import solve_ivp
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
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
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


🐍 Streamplot Helper
--------------------------------------------------------------------------------

```python
def Q(f, xs, ys):
    X, Y = meshgrid(xs, ys)
    v = vectorize
    fx = v(lambda x, y: f([x, y])[0])
    fy = v(lambda x, y: f([x, y])[1])
    return X, Y, fx(X, Y), fy(X, Y)
```


## 🧭 Context

 1. **System initially at rest.** $x(0) = 0.$

 2. **Black box.** The system state $x(t)$ is unknown.

 3. **Input/Output (I/O).** The input determines the output:

    $$
    u(t), \, t\geq 0  \; \to \; y(t), \, t\geq 0.
    $$

--------------------------------------------------------------------------------

The [variation of constants method](https://en.wikipedia.org/wiki/Variation_of_parameters) yields

  $$
  y(t) = \int_0^{t} C e^{A(t-\tau)} B u(\tau) \, d\tau + D u(t).
  $$

## 🏷️ Signals & Causality


A **signal** is a time-dependent function 

$$
x(t) \in \mathbb{R}^n, \; t \in \mathbb{R}.
$$

It is **causal** if

$$
t< 0 \; \Rightarrow \; x(t) = 0.
$$

## 📝 Convention


In the sequel, we will assume that time-dependent functions defined only 
for non-negative times

$$
x(t), \, t \geq 0
$$

are zero for negative times

$$
x(t) = 0, \; t < 0.
$$

With this convention, they become causal signals.


## 🏷️ Heaviside function


The **Heaviside function** is the causal signal defined by

$$
e(t) = \left|
\begin{array}{c}
1 & \mbox{if } \; t\geq 0, \\
0 & \mbox{if } \; t < 0.
\end{array}
\right.
$$

🏷️ Synonym: **(unit) step signal.**

## 🏷️ Impulse Response

The system **impulse response** is defined by:

$$
H(t) = (C e^{At} B) \times e(t) + D \delta(t) \in \mathbb{R}^{p \times m}
$$

## 📝 Notes


- the formula is valid for general (**MIMO**) systems.  

  🏷️ **MIMO** = multiple-input & multiple-output.

- $\delta(t)$ is the **unit impulse** signal, 
  we'll get back to it (in the meantime, you may assume that $D=0$).


## 📝 SISO Systems


When $u(t) \in \mathbb{R}$ and $y(t) \in \mathbb{R}$ the system is
**SISO**.

🏷️ **SISO** = single-input & single-output.

Then $H(t)$ is a $1 \times 1$ matrix.

We identify it with its unique coefficient $h(t)$:

$$
H(t) \in \mathbb{R}^{1\times 1} = [h(t)], \; h(t) \in \mathbb{R}.
$$



## 💎 I/O Behavior


Let $u(t)$, $x(t)$, $y(t)$ be causal signals such that:

$$
\left|
  \begin{array}{rcl}
  \dot{x}(t) &=& A x(t) + B u(t) \\
        y(t) &=& C x(t) + Du(t)
  \end{array}
\right.,
\, t\geq 0
\; \mbox{ and } \;
x(0) = 0.
$$

Then

$$
y(t) = (H \ast u) (t) := \int_{-\infty}^{+\infty} H(t - \tau) u(\tau) \, d\tau .
$$

## 🏷️ Convolution


The operation $\ast$ is called a **convolution**.


## 🔍 Impulse Response


Consider the SISO system
  
$$
\left| 
\begin{array}{ccl}
\dot{x} &=& ax + u \\
y &=& x \\
\end{array}
\right.
$$

where $a \neq 0$.

--------------------------------------------------------------------------------

We have

$$
\begin{split}
H(t) &= (C e^{At} B) \times e(t) + D \delta(t)\\
     &= [1]e^{[a]t} [1] e(t) + [0] \delta(t) \\
     &= [e(t)e^{at}]
\end{split}
$$

--------------------------------------------------------------------------------

When $u(t) = e(t)$ for example,

$$
\begin{split}
y(t) 
  &= \int_{-\infty}^{+\infty} e(t - \tau)e^{a(t-\tau)} e(\tau) \, d\tau \\
  &= \int_{0}^{t} e^{a(t- \tau)} \, d\tau \\
  &= \int_{0}^{t} e^{a \tau} \, d\tau  \\
  &= \frac{1}{a} \left(e^{a t} - 1 \right)
\end{split} 
$$


## 🧩 Integrator


Let 

$$
\left| 
\begin{array}{ccc}
\dot{x} &=& u \\
y &=& x \\
\end{array}
\right.
$$

where $u \in \mathbb{R}$, $x \in \mathbb{R}$ and $y \in \mathbb{R}$.


--------------------------------------------------------------------------------

### 1. 🧮 

Compute the impulse response of the system.

## 🔓 Integrator


--------------------------------------------------------------------------------

### 1. 🔓

$$
\begin{split}
H(t) &= (C e^{At} B) \times e(t) + D \delta(t)\\
     &= [1]e^{[0]t} [1] e(t) + [0] \delta(t) \\
     &= [e(t)]
\end{split}
$$

## 🧩 Double Integrator


Let 

$$
\left| 
\begin{array}{ccc}
\dot{x}_1 &=& x_2 \\
\dot{x}_2 &=& u \\
y &=& x_1 \\
\end{array}
\right.
$$

where $u \in \mathbb{R}$, $x=(x_1, x_2) \in \mathbb{R}^2$ and $y \in \mathbb{R}$.



--------------------------------------------------------------------------------

### 1. 🧮 

Compute the impulse response of the system.
  

## 🔓 Double Integrator


--------------------------------------------------------------------------------

### 1. 🔓

$$
\begin{split}
H(t) &= (C \exp(At) B) \times e(t) + D \delta(t)\\
     &= \displaystyle \left[\begin{array}{cc} 1 & 0 \end{array}\right]
        \exp \left(
        \left[\begin{array}{cc}
        0 & 1 \\
        0 & 0
        \end{array}\right]
         t \right) \left[\begin{array}{c} 0 \\ 1 \end{array}\right] e(t)  + [0] \delta(t) \\
     &= \displaystyle \left[\begin{array}{cc} 1 & 0 \end{array}\right]
        \left[\begin{array}{cc}
        1 & t \\
        0 & 1
        \end{array}\right]
        \left[\begin{array}{c} 0 \\ 1 \end{array}\right] e(t) \\
&= [t e(t)]
\end{split}
$$

## 🧩 Gain


Let 

$$
y = K u
$$

where $u \in \mathbb{R}^m$, $y \in \mathbb{R}^p$ and 
$K \in \mathbb{R}^{p \times m}$.

--------------------------------------------------------------------------------

### 1. 🧮 

Compute the impulse response of the system.
  

## 🔓 Gain


--------------------------------------------------------------------------------

### 1. 🔓
  
The I/O behavior can be represented by $\dot{x} = 0x+0u$ and $y= 0 \times x + K u$
(for example). Thus,

$$
\begin{split}
H(t) &= (C \exp(At) B) \times e(t) + D \delta(t)\\
     &= 0 + K \delta(t)\\
     &= K \delta(t) 
\end{split}
$$

## 🧩 MIMO System


Let 
$$
H(t) := 
\left[
\begin{array}{cc}
e^{t} e(t) & e^{-t} e(t)
\end{array}
\right]
$$

--------------------------------------------------------------------------------

### 1. 🧮 

Find a linear system with matrices $A$, $B$, $C$, $D$ 
whose impulse response is $H(t)$.


--------------------------------------------------------------------------------

### 2. 🧮 

Is there another 4-uple of matrices $A$, $B$, $C$, $D$ with the same
impulse response? 


--------------------------------------------------------------------------------

### 3. 🧮 

Same question but with a matrix $A$ of a different size?

## 🔓 MIMO System


--------------------------------------------------------------------------------

### 1. 🔓

Since

$$
\exp
\left(
  \left[
\begin{array}{rr}
  +1 & 0 \\
  0 & -1
  \end{array}
\right] t
\right)
= 
\left[
  \begin{array}{rr}
  e^{+t} & 0 \\
  0 & e^{-t}
  \end{array}
\right],
$$

the following matrices work:

$$
A = \left[
  \begin{array}{rr}
  +1 & 0 \\
  0 & -1
  \end{array}
\right], \;
B = \left[
  \begin{array}{cc}
  1 & 0 \\
  0 & 1
  \end{array}
\right], \;
C= \left[
  \begin{array}{cc}
  1 & 1 \\
  \end{array}
\right], \;
D = \left[
  \begin{array}{cc}
  0 & 0 \\
  \end{array}
\right].
$$



--------------------------------------------------------------------------------

### 2. 🔓

Since
$$
\begin{split}
H(t) &= (C \exp(At) B) \times e(t) + D \delta(t)\\
     &= ((-C) \exp(At) (-B)) \times e(t) + D \delta(t)
\end{split}
$$
changing $B$ and $C$ to be
$$
B = \left[
  \begin{array}{rr}
  -1 & 0 \\
  0 & -1
  \end{array}
\right], \;
C= \left[
  \begin{array}{rr}
  -1 & -1 \\
  \end{array}
\right], \;
$$
doesn't change the impulse response.


--------------------------------------------------------------------------------

### 3. 🔓

We can also easily add a scalar dynamics (say $\dot{x}_3 = 0$)
that doesn't influence the impulse response. 

The following matrices also work

$$
A = \left[
  \begin{array}{rrr}
  +1 & 0 & 0\\
  0 & -1 & 0 \\
  0 & 0  & 0
  \end{array}
\right], \;
B = \left[
  \begin{array}{cc}
  1 & 0\\
  0 & 1\\
  0 & 0
  \end{array}
\right], $$

$$
C= \left[
  \begin{array}{cc}
  1 & 1 & 0 \\
  \end{array}
\right], \;
D = \left[
  \begin{array}{cc}
  0 & 0\\
  \end{array}
\right].
$$


## 🏷️ Laplace Transform


Let $x(t)$, $t\in\mathbb{R}$ be a scalar signal.

It **Laplace transform** is the function of $s$ given by:

$$
x(s) = \int_{-\infty}^{+\infty} x(t) e^{-st} \, dt.
$$

## Domain & Codomain


The Laplace transform of a signal is a complex-valued function; 
its domain is a subset of the complex plane.

$$
s \in D \, \Rightarrow \, x(s) \in \mathbb{C}.
$$

--------------------------------------------------------------------------------

If $x(t)$ is a causal signal of **sub-exponential growth**

$$
|x(t)| \leq k e^{\sigma t} e(t), \, t \in \mathbb{R}, 
$$ 

($k \geq 0$ and $\sigma \in \mathbb{R}$), 
its Laplace transform is defined on an open half-plane:

$$
\Re (s) > \sigma \; \Rightarrow \; x(s) \in \mathbb{C}.
$$

 
## ⚠️ Notation

We use the same symbol (here "$x$") to denote: 

  - a signal $x(t)$ and

  - its Laplace transform $x(s)$
 
They are two equivalent representations of the same "object", 
but different mathematical "functions". 

If you fear some ambiguity, use named variables, e.g.:

  $$
  x(t=1) \, \mbox{ or } \, x(s=1) \, \mbox{ instead of } \, x(1).
  $$

## Vector/Matrix-Valued Signals


The Laplace transform 

  - of a vector-valued signal $x(t) \in \mathbb{R}^n$ or

  - of a matrix-valued signal $X(t) \in \mathbb{R}^{m \times n}$ 
  
are computed elementwise.

--------------------------------------------------------------------------------

$$
x_{i}(s) := \int_{-\infty}^{+\infty} x_{i}(t) e^{-st} \, dt.
$$

$$
X_{ij}(s) := \int_{-\infty}^{+\infty} X_{ij}(t) e^{-st} \, dt.
$$


## 🏷️ Rational Signals


We will only deal with **rational** (and causal) signals:

  $$
  x(t) = \left(\sum_{\lambda \in \Lambda} p_{\lambda}(t) e^{\lambda t} \right) e(t)
  $$

where: 

  - $\Lambda$ is a finite subset of $\mathbb{C}$,

  - for every $\lambda \in \Lambda$, $p_{\lambda}(t)$ is a polynomial in $t$.


## 📝


They are called **rational** since

  $$
  x(s) = \frac{n(s)}{d(s)}
  $$

where $n(s)$ and $d(s)$ are polynomials; also

$$
\deg n(s) \leq \deg d(s).
$$


## 🔍 Exponential


Let 

$$
x(t) = e^{a t} e(t), \; t\in \mathbb{R}
$$ 
for some $a \in \mathbb{R}$. Then

$$
\begin{split}
x(s) &= \int_{-\infty}^{+\infty} e^{at} e(t) e^{-s t} \, dt = \int_0^{+\infty} e^{(a-s) t} \, dt. \\
\end{split}
$$

--------------------------------------------------------------------------------


If $\Re(s) > a$, then 
$$
\left|e^{(a-s) t}\right| \leq e^{-(\Re (s) -a) t};
$$
the function $t \in \left[0, +\infty\right[ \mapsto e^{(a-s) t}$ is integrable
and

$$
x(s) = \left[\frac{e^{(a-s) t}}{a-s} \right]^{+\infty}_0 = \frac{1}{s-a}.
$$


## 💻 Symbolic Computation


```python
import sympy
from sympy.abc import t, s
from sympy.integrals.transforms \
    import laplace_transform    

def L(f):
    return laplace_transform(f, t, s)[0]
```

--------------------------------------------------------------------------------

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```{.no-exec lang=python}
>>> from sympy.abc import a
>>> xt = sympy.exp(a*t)
>>> xs = L(xt)
>>> xs
1/(-a + s)
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: notebook :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
from sympy.abc import a
xt = sympy.exp(a*t)
xs = L(xt)
xs
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## 🧩 Ramp


Let

$$
x(t) = t e(t), \; t\in\mathbb{R}.
$$

--------------------------------------------------------------------------------

### 1. 🧮

Compute analytically the Laplace Transform of $x(t)$.

--------------------------------------------------------------------------------

### 2. 💻

Compute symbolically the Laplace Transform of $x(t)$.

## 🔓 Ramp


--------------------------------------------------------------------------------

### 1. 🔓

$$
\begin{split}
x(s) 
 &= \int_{-\infty}^{+\infty} t e(t) e^{-s t} \, dt \\
 &= \int_0^{+\infty} t e^{-s t} \, dt. \\
\end{split}
$$

--------------------------------------------------------------------------------

By integration by parts,
$$
\begin{split}
x(s) 
  &= \left[t\frac{e^{-st}}{-s} \right]^{+\infty}_0 - \int_0^{+\infty} \frac{e^{-s t}}{-s} \, dt \\
  &= \frac{1}{s} \int_0^{+\infty} e^{-s t} \, dt \\
  &= \frac{1}{s} \left[\frac{e^{-st}}{-s} \right]^{+\infty}_0 \\
  &= \frac{1}{s^2}
\end{split}
$$

--------------------------------------------------------------------------------

### 2. 🔓

With SymPy, we have accordingly:

```{.no-exec lang=python}
>>> xt = t
>>> xs = L(xt)
>>> xs
s**(-2)
```


## 🏷️ Transfer Function 

Let $H(t)$ be the impulse response of a system.

Its Laplace transform $H(s)$ is the system **transfer function**.


## 💎


For LTI systems in standard form,

$$
H(s) = C [sI - A]^{-1} B + D.
$$

## 💎 Operational Calculus


$$
y(t) = (H \ast u)(t)
\; \Longleftrightarrow \;
y(s) = H(s) \times u(s)
$$


## Graphical Language


Control engineers used **block diagrams** to describe (combinations of) 
dynamical systems, with

  - "boxes" to determine the relation between input signals and output signals and

  - "wires" to route output signals to inputs signals.


## Feedback Block-Diagram


![](images/static/feedback-alt.svg)  

--------------------------------------------------------------------------------

  - **Triangles** denote **gains** (scalar or matrix multipliers),

  - **Adders** sum (or substract) signals.

--------------------------------------------------------------------------------

  - **LTI systems** can be specified by:

      - (differential) equations,

      - the impulse response,

      - the transfer function.

## Equivalent Systems


![](images/static/equivalent-systems.svg)  


## 🧩 Feedback Block-Diagram


Consider the system depicted 
in the [Feedback Block-Diagram] picture.


--------------------------------------------------------------------------------

### 1. 🧮

Compute its transfer function.

## 🔓 Feedback Block-Diagram


--------------------------------------------------------------------------------

### 1. 🔓

The diagram logic translates into:

$$
y(s) = \frac{1}{s} \left(u(s) - k y(s)\right),
$$

and thus

$$
\left(1 - \frac{k}{s}\right) y(s) =\frac{1}{s} u(s)
$$

--------------------------------------------------------------------------------

or equivalently

$$
y(s) = \frac{1}{s- k} u(s).
$$

Thus, the transfer function of this SISO system is

$$
h(s) = \frac{1}{s- k}.
$$






## 🤔 Impulse Response



Why refer to $h(t)$ as the system "impulse response"?

By the way, what's an impulse?


## Impulse Approximations


Pick a time constant $\varepsilon > 0$ and define

$$
\delta_{\varepsilon}(t) := \frac{1}{\varepsilon} e^{-t/\varepsilon} e(t).
$$

## 🐍


```python
def delta(t, eps):
    return exp(-t / eps) / eps * (t >= 0)
```


## 📈


```python
figure()
t = linspace(-1, 4, 1000)
for eps in [1.0, 0.5, 0.25]:
    plot(t, delta(t, eps), 
         label=rf"$\varepsilon={eps}$")
xlabel("$t$"); title(r"$\delta_{\varepsilon}(t)$") 
legend()
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/impulses")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/impulses.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


## In the Laplace Domain


$$
\begin{split}
\delta_{\varepsilon}(s) 
  &= \int_{-\infty}^{+\infty} \delta_{\varepsilon}(t) e^{-st} \, dt \\
  &= \frac{1}{\varepsilon} \int_{0}^{+\infty} e^{-(s + 1/\varepsilon)t} \, dt \\
  &= \frac{1}{\varepsilon} 
      \left[ 
      \frac{e^{-(s+1/\varepsilon)t}}{-(s+1/\varepsilon)} 
      \right]^{+\infty}_0 = \frac{1}{1 + \varepsilon s}\\
\end{split}
$$

(assuming that $\Re(s) > -1/\varepsilon$)

--------------------------------------------------------------------------------

  - The "limit" of the signal $\delta_{\varepsilon}(t)$ when $\varepsilon \to 0$
    is not defined *as a function* (issue for $t=0$) but as a **generalized
    function** $\delta(t)$, the **unit impulse**. 

  - This technicality can be avoided in the Laplace domain where
      $$
      \delta(s) = \lim_{\varepsilon \to 0} \delta_{\varepsilon}(s)
      =
      \lim_{\varepsilon \to 0} \frac{1}{1 + \varepsilon s} = 1.
      $$

--------------------------------------------------------------------------------

Thus, if $y(t) = (h \ast u)(t)$ and

 1. $u(t) = \delta(t)$ then

 2. $y(s) = h(s) \times \delta(s) = h(s) \times 1 = h(s)$

 3. and thus $y(t) = h(t)$.

**Conclusion:**
the impulse response $h(t)$ is the output of the system when
the input is the unit impulse $\delta(t)$.


## 🏷️ I/O Stability


A system is **I/O-stable** if there is a $K \geq 0$ such that

$$
\|u(t)\| \leq M, \, t\geq 0
$$

$$
\Rightarrow
$$


$$
\|y(t)\| \leq K M, \, t\geq 0. 
$$

🏷️ More precisely, **BIBO-stability** ("bounded input, bounded output").


## 🏷️ Transfer Function Poles


A **pole** of the transfer function $H(s)$ is a $s \in \mathbb{C}$ such that
for at least one element $H_{ij}(s)$,

$$
|H_{ij}(s)| = +\infty.
$$

## 💎 I/O-Stability Criteria


A system is I/O-stable if and only if all its poles are in the open left-plane,
i.e. such that

$$
\Re (s)< 0.
$$

## 💎 Internal Stability $\Rightarrow$ I/O-Stability


If the system $\dot{x} = A x$ is asymptotically stable,
then for any matrices $B$, $C$, $D$ of compatible shapes,

$$
\begin{split}
\dot{x} &= A x + B u \\
y &= C x + Du
\end{split}
$$

is I/O-stable.

## 🔍 Fully Actuated & Measured System


If $B=I$, $C=I$ and $D=0$, that is

  $$
  \dot{x} = A x +u, \; y = x
  $$

then $H(s) = [sI-A]^{-1}$. 

--------------------------------------------------------------------------------

Therefore, $s$ is a pole of $H$ iff it's an eigenvalue of $A$.

Thus, in this case, asymptotic stability and I/O-stability are equivalent.

(This equivalence actually holds under much weaker conditions.)

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
background-color: white;
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

section p.author {
  text-align: center;
  margin: auto;
}

</style>

<link href="https://fonts.googleapis.com/css?family=Inconsolata:400,700" rel="stylesheet">

<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.css" rel="stylesheet">

