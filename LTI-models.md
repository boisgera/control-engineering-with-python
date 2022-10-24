% Linear Models
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


## 🐍 Streamplot Helper

```python
def Q(f, xs, ys):
    X, Y = meshgrid(xs, ys)
    v = vectorize
    fx = v(lambda x, y: f([x, y])[0])
    fy = v(lambda x, y: f([x, y])[1])
    return X, Y, fx(X, Y), fy(X, Y)
```


🧭 Preamble
--------------------------------------------------------------------------------

## 🏷️ Non-autonomous Systems


Their structure is

$$
\dot{x} = f(x, u)
$$

where $x \in \mathbb{R}^n$ and $u \in \mathbb{R}^m$, that is 

$$
f: \mathbb{R}^n \times \mathbb{R}^m \to \mathbb{R}^n.
$$

🏷️ Inputs
--------------------------------------------------------------------------------

The vector-valued $u$ is the **system input**.

This quantity may depend on the time $t$
 
$$
u: t \in \mathbb{R} \mapsto u(t) \in \mathbb{R}^m,
$$

(actually it may also depend on some state, but we will adress this later).

📝
--------------------------------------------------------------------------------

A solution of 

$$\dot{x} = f(x, u), \; x(t_0) = x_0$$ 

is merely a solution of 

$$\dot{x} = h(t,x), \; x(t_0) = x_0,$$

where

$$h(t, x) := f(x, u(t)).$$


## 🏷️ Outputs


We may complement the system dynamics with an equation

$$
y = g(x, u) \in \mathbb{R}^p
$$

The vector $y$ refers to the **systems output**, usually the quantities that
we can effectively measure in a system (the state $x$ itself may be unknown).


🧭 Linear Systems
--------------------------------------------------------------------------------

## Standard Form


Input $u \in \mathbb{R}^m$, state $x \in \mathbb{R}^n$, 
output $y \in \mathbb{R}^p$.

  $$
  \begin{array}{c}
  \dot{x} &=& A x + B u \\
  y       &=& C x + D u
  \end{array}
  $$


## Matrix Shape


$A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n\times m}$,
$C \in \mathbb{R}^{p \times n}$, $D \in \mathbb{R}^{p \times m}$.

  $$
  \left[
  \begin{array}{c|c}
  A &  B \\
  \hline
  C &  D
  \end{array} 
  \right]
  $$

## 💎 Well-Posedness 


When $u=0$, 

$$
\dot{x} = A x =: f(x) 
\; \Rightarrow \;
\frac{\partial f}{\partial x}(x) = A
$$

The vector field $f$ is continuously differentiable

$\Rightarrow$ **The system is well-posed.**

## 💎 Equilibrium 


When $u=0$, since

$$
\dot{x} = A x =: f(x)
$$

$$
f(0) = A 0 = 0
$$

$\Rightarrow$ **the origin $x=0$ is always an equilibrium.**  

(the only one in the state space if $A$ is invertible).


## 🤔 Why "Linear" ?

Assume that:

  - $\dot{x}_1 = A x_1 + B u_1$, $x_1(0) = x_{10}$,

  - $\dot{x}_2 = A x_2 + B u_2$, $x_2(0) = x_{20}$,

--------------------------------------------------------------------------------

Set
  
  - $u_3 = \lambda u_1 + \mu u_2$ and

  - $x_{30} = \lambda x_{10} + \mu x_{20}$.

for some $\lambda$ and $\mu$.


--------------------------------------------------------------------------------

Then, if 

$$x_3 = \lambda x_1 + \mu x_2,$$

we have

$$
\dot{x}_3 = A x_3 + B u_3, \; x_3(0) = x_{30}.
$$


## 💎 Dynamics Decomposition


The solution of

$$
\dot{x} = A x + Bu, \; x(0) = x_0
$$

is the sum $x(t)=x_1(t)+x_2(t)$ where 

  - $x_1(t)$ is the solution to the **internal dynamics** and

  - $x_2(t)$ is the solution to the **external dynamics**.

## 🏷️ Internal/External

  - The **internal dynamics** is controlled by the initial value $x_0$ only
(there is no input, $u=0$).

    $$
    \dot{x}_1 = A x_1, \; x_1(0) = x_0,
    $$

  - The **external dynamics** is controlled by the input $u(t)$ only (the system is 
initially at rest, $x_0=0$).
  
    $$
    \dot{x}_2 = A x_2 + Bu, \;  x_2(0) = 0.
    $$


## 🏷️ LTI Systems

These systems are actually linear and  **time-invariant** (hence **LTI**) systems. Time-invariant means that when $x(t)$ is a solution of

$$
\dot{x} = A x + Bu, \; x(0) = x_0,
$$

then $x(t- t_0)$ is a solution of 

$$
\dot{x} = A x + Bu(t-t_0), \; x(t_0) = x_0.
$$



## 🔍 Heat Equation


![](images/static/heat-simple.svg)

## Simplified Model


  - Four cells numbered 1 to 4 are arranged in a row.

  - The first cell has a heat source, the last one a temperature sensor.

  - The heat sink/source is increasing the temperature of its cell 
    of $u$ degrees by second.

  - If the temperature of a cell is $T$ and the one of a neighbor is
    $T_n$, $T$ increases of $T_n - T$ by second.

--------------------------------------------------------------------------------

Given the geometric layout:

  - $d T_1/dt = u + (T_2 - T_1)$

  - $d T_2/dt = (T_1 - T_2) + (T_3 - T_2)$

  - $d T_3/dt = (T_2 - T_3) + (T_4 - T_3)$

  - $d T_4/dt = (T_3 - T_4)$

  - $y = T_4$

--------------------------------------------------------------------------------

Set $x = (T_1, T_2, T_3, T_4)$. 

The model is linear and its standard matrices are:

$$
A = \left[
  \begin{array}{rrrr}
-1 & 1 & 0 & 0   \\
1  & -2 & 1 & 0 \\
0 & 1 & -2 & 1  \\
0 & 0 & 1 & -1 
\end{array}
\right]
$$

--------------------------------------------------------------------------------

$$
B = \left[
  \begin{array}{c}
  1 \\ 0 \\ 0 \\ 0
  \end{array} 
  \right], \;
C = 
\left[ 
\begin{array}{cccc}
0 & 0 & 0 & 1
\end{array}
\right],
\; D = [0]
$$


🧭 Linearization
--------------------------------------------------------------------------------

## Nonlinear to Linear


Consider the nonlinear system

$$
\begin{array}{ccc}
\dot{x} &=& f(x, u) \\
      y &=& g(x, u)
\end{array}
$$ 

--------------------------------------------------------------------------------

Assume that $x_e$ is an equilibrium when $u=u_e$ (cst):

$$
f(x_e, u_e) = 0
$$

and let 
  
  $$
  y_e := g(x_e, u_e).
  $$

--------------------------------------------------------------------------------

Define the error variables 

  - $\Delta x := x - x_e$, 
  
  - $\Delta u := u - u_e$ and

  - $\Delta y := y - y_e$.

--------------------------------------------------------------------------------

As long as the error variables stay small

$$
f(x, u) 
\simeq
\overbrace{f(x_e, u_e)}^0 + 
\frac{\partial f}{\partial x}(x_e, u_e) \Delta x
+ \frac{\partial f}{\partial u}(x_e, u_e) \Delta u
$$

$$
g(x, u) 
\simeq
\overbrace{g(x_e, u_e)}^{y_e} + 
\frac{\partial g}{\partial x}(x_e, u_e) \Delta x
+ \frac{\partial g}{\partial u}(x_e, u_e) \Delta u
$$

--------------------------------------------------------------------------------

Hence, the error variables satisfy *approximately*

$$
\begin{array}{c}
d(\Delta x)/dt &=& A \Delta x + B \Delta u \\
\Delta y       &=& C \Delta x + D \Delta u
\end{array}
$$

with

$$
\left[
\begin{array}{c|c}
A &  B \\
\hline
C &  D
\end{array} 
\right]
= 
\left[
\begin{array}{c|c}
\frac{\partial f}{\partial x} &  \frac{\partial f}{\partial u} \\
\hline
\frac{\partial g}{\partial x} &  \frac{\partial g}{\partial u}
\end{array} 
\right](x_e, u_e)
$$

## 🔍 Example


The system

$$
\begin{array}{cc}
\dot{x} &=& -2x + y^3 \\
\dot{y} &=& -2y + x^3
\end{array}
$$
  
has an equilibrium at $(0, 0)$.

--------------------------------------------------------------------------------

The corresponding error variables satisfy $\Delta x = x$ and $\Delta y = y$, thus
$$
\frac{d \Delta x}{dt} =\dot{x} = -2 x + y^3 = -2 \Delta x + (\Delta y)^3 \approx -2 \Delta x
$$
$$
\frac{d \Delta y}{dt} =\dot{y} = -2 y + x^3 = -2 \Delta y + (\Delta x)^3 \approx -2 \Delta y
$$

--------------------------------------------------------------------------------

$$
\begin{array}{cc}
\dot{x} &=& -2x + y^3 \\
\dot{y} &=& -2y + x^3
\end{array}
$$

$\to$

$$
\begin{array}{cc}
\dot{x} &\approx& -2x  \\
\dot{y} &\approx& -2y 
\end{array}
$$

--------------------------------------------------------------------------------

### 🐍 Vector fields


```python
def f(xy):
    x, y = xy
    dx = -2*x + y**3
    dy = -2*y + x**3
    return array([dx, dy])
```

--------------------------------------------------------------------------------


```python
def fl(xy):
    x, y = xy
    dx = -2*x
    dy = -2*y
    return array([dx, dy])
```

--------------------------------------------------------------------------------

### 📈 Stream Plot


```python
figure()
x = y = linspace(-1.0, 1.0, 1000)
streamplot(*Q(f, x, y), color="k")
blue_5 = "#339af0"
streamplot(*Q(fl, x, y), color=blue_5) 
plot([0], [0], "k.", ms=10.0)
axis("square")
axis("off")
```


::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/linearization")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/linearization.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


## 🔍 Linearization


Consider

$$
\dot{x} = -x^2 + u, \; y = x u
$$

If we set $u_e = 1$, the system has an equilibrium at $x_e = 1$
(and also $x_e = -1$ but we focus on the former) and the corresponding
$y$ is $y_e = x_e u_e = 1$.

--------------------------------------------------------------------------------

Around this configuration $(x_e, u_e) = (1, 1)$, we have

$$
\frac{\partial (-x^2+u)}{\partial x} = -2x_e = -2,
\; \frac{\partial (-x^2+u)}{\partial u} = 1,
$$

and

$$
\frac{\partial x u }{\partial x} = u_e = 1,
\; \frac{\partial x u}{\partial u} = x_e = 1.
$$

--------------------------------------------------------------------------------

Thus, the approximate, linearized dynamics around this equilibrium is

$$
\begin{array}{rcr}
d(x-1)/dt &=& -2 (x - 1) + (u - 1) \\
y -1      &=&  (x - 1) + (u - 1)
\end{array}
$$


## 💎 Asymptotic Stability


The equilibrium $0$ is locally 
asymptotically stable for 

$$
\frac{d \Delta x}{dt} = A \Delta x
$$ 

where $A = \partial f (x_e, u_e) / \partial x.$

$\Rightarrow$

The equilibrium $x_e$ is locally asymptotically 
stable for 

$$
\dot{x} = f(x, u_e).
$$

## ⚠️ Converse Result


  - The converse is not true : the nonlinear system may be asymptotically
    stable but not its linearized approximation (e.g. consider $\dot{x} = -x^3$).

  - If we replace local **asymptotic stability** with local **exponential stability**,
    the requirement that locally

    $$
    \|x(t) - x_e\| \leq A e^{-\sigma t} \|x(0) - x_e\|
    $$
    
    for some $A >0$ and $\sigma > 0$, then it works.




## 🧩 Pendulum


A pendulum submitted to a torque $c$ is governed by

$$
m \ell^2 \ddot{\theta} + b \dot{\theta} + m g \ell \sin \theta = c.
$$

We assume that only the angle $\theta$ is measured.

--------------------------------------------------------------------------------

### 1. 🧮

Let $x=(\theta, \dot{\theta})$, $u=c$ and $y=\theta$.

What are the function $f$ and $g$ that determine the nonlinear
dynamics of the pendulum?

--------------------------------------------------------------------------------

### 2. 🧮

Show that for any angle $\theta_e$ there is a constant value $c_e$
of the torque such that $x_e = (\theta_e, 0)$ is an equilibrium.

--------------------------------------------------------------------------------

### 3. 🧮

Compute the linearized dynamics of the pendulum around this equilibrium
and put it in the standard form (compute $A$, $B$, $C$ and $D$).

## 🔓 Pendulum


--------------------------------------------------------------------------------

### 1. 🔓

The 2nd-order differential equation

$$
m \ell^2 \ddot{\theta} + b \dot{\theta} + m g \ell \sin \theta = c.
$$

is equivalent to the first-order differential equation

$$
\frac{d}{dt}
\left[
  \begin{array}{c} 
    \theta \\ 
    \omega
  \end{array}
\right]
=
\left[
  \begin{array}{c} 
    \omega \\ 
    -(b /m\ell^2)\omega - (g/\ell) \sin \theta + c / m\ell^2 
  \end{array}
\right]
$$

--------------------------------------------------------------------------------

Hence, with $x=(\theta, \dot{\theta})$, $u=c$ and $y=\theta$, we have

$$
\begin{array}{ccc}
\dot{x} &=& f(x, u) \\
      y &=& g(x, u)
\end{array}
$$ 

with 

$$
\begin{array}{lll}
f((\theta, \omega), c) &=& \left(\omega, -(b /m\ell^2)\omega - (g/\ell) \sin \theta + c / m\ell^2 \right) \\
g((\theta, \omega), c) &=& \theta.
\end{array}
$$

--------------------------------------------------------------------------------

### 2. 🔓

Let $\theta_e$ in $\mathbb{R}$. If $c=c_e$, the state 
$x_e:=(\theta_e, 0)$ is an equilibrium if and only if $f((\theta_e, 0), c_e)=0$, 
that is

$$
\left[
  \begin{array}{c} 
    0 \\ 
    0 - (g/\ell) \sin \theta_e + c_e / m\ell^2 
  \end{array}
\right]
=
\left[
  \begin{array}{c} 
    0 \\ 
    0
  \end{array}
\right]
$$

which holds if and only if

$$
c_e = m g \ell  \sin \theta_e.
$$

--------------------------------------------------------------------------------

### 3. 🔓

We have

$$
A = \frac{\partial f}{\partial x} (x_e, c_e)
=
\left[
  \begin{array}{rr}
    0 & 
    1 \\
    - (g/\ell) \cos \theta_e & 
    -(b /m\ell^2) \\
  \end{array}
\right]
$$

$$
B = \frac{\partial f}{\partial u} (x_e, u_e) =
\left[
  \begin{array}{c}
    0 \\
    1/m\ell^2
    \end{array}
\right]
$$

$$
C = \frac{\partial g}{\partial x_e} (x_e, u_e)
= 
\left[
  \begin{array}{cc}
    1 \\
    0
  \end{array}
\right],
\;
D = \frac{\partial g}{\partial u_e} (x_e, u_e)
=
0
$$

--------------------------------------------------------------------------------

Thus,

$$
\begin{split}
\frac{d}{dt}\Delta \theta & \approx \Delta \omega \\
\frac{d}{dt}\Delta \omega & \approx -(g/\ell) \cos (\theta_e) \Delta \theta -(b/m\ell^2) \Delta \omega + \Delta c /m \ell^2 \\
\end{split}
$$

and obviously, as far as the output goes,

$$
\Delta \theta \approx \Delta \theta.
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

