% Linear Systems
% 👤 [Sébastien Boisgérault](mailto:Sebastien.Boisgerault@mines-paristech.fr)
  🏦 Mines Paris, PSL University
% ©️ [CC-BY 4.0 International](https://creativecommons.org/licenses/by/4.0/)


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


Preamble
================================================================================

Inputs
--------------------------------------------------------------------------------

It's handy to introduce non-autonomous ODEs.

There are designated as

$$
\dot{x} = f(x, u)
$$

where $x \in \mathbb{R}^n$ and $u \in \mathbb{R}^m$, that is 

$$
f: \mathbb{R}^n \times \mathbb{R}^m \to \mathbb{R}^n.
$$

--------------------------------------------------------------------------------

The vector-valued $u$ is the **system input**.

This quantity may depend on the time $t$
 
$$
u: t \in \mathbb{R} \mapsto u(t) \in \mathbb{R}^m,
$$

(actually it may also depend on some state, but we will adress this later).

--------------------------------------------------------------------------------

A solution of 

$\dot{x} = f(x, u)$ and $x(t_0) = x_0$ 

is merely a solution of 

$\dot{x} = h(t,x)$ and $x(t_0) = x_0$, 

where

$h(t, x) = f(x, u(t))$.


Outputs
--------------------------------------------------------------------------------

We may complement the system dynamics with an equation

$$
y = g(x, u) \in \mathbb{R}^p
$$

The vector $y$ refers to the **systems output**, usually the quantities that
we can effectively measure in a system (the state $x$ itself may be unknown).


What Are Linear Systems?
================================================================================

Standard Form
--------------------------------------------------------------------------------

Input $u \in \mathbb{R}^m$, state $x \in \mathbb{R}^n$, 
output $y \in \mathbb{R}^p$.

  $$
  \begin{array}{c}
  \dot{x} &=& A x + B u \\
  y       &=& C x + D u
  \end{array}
  $$


Matrix Size
--------------------------------------------------------------------------------

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

Well-Posedness 
--------------------------------------------------------------------------------

When $u=0$, 

$$
\dot{x} = A x =: f(x) 
\; \Rightarrow \;
\frac{\partial f}{\partial x}(x) = A
$$

The vector field $f$ is continuously differentiable

$\Rightarrow$

The system is well-posed.

Equilibrium 
--------------------------------------------------------------------------------

When $u=0$, since

$$
\dot{x} = A x =: f(x)
$$

$$
f(0) = A 0 = 0
$$

$\Rightarrow$ the origin $x_e=0$ is always an equilibrium  
(the only one in the state space if $A$ is invertible).


Why "Linear" ?
--------------------------------------------------------------------------------

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


Internal + External Dynamics
--------------------------------------------------------------------------------

**Corollary:** Since $(x_0, u) = (x_0, 0) + (0, u)$ the solution of 

$$
\dot{x} = A x + Bu, \; x(0) = x_0
$$

is the sum of the solutions $x_1$ and $x_2$ of:

--------------------------------------------------------------------------------

the **internal dynamics**

$$
\dot{x}_1 = A x_1, \; x_1(0) = x_0
$$

(behavior controlled by the initial value only, no input)

and the **external dynamics**:

$$
\dot{x}_2 = A x_2 + Bu, \; x_2(0) = 0
$$

(behavior controlled by the input, the systems is initially at rest)



   
LTI Systems
--------------------------------------------------------------------------------

They are actually referred to as **linear time-invariant (LTI)** 
systems: 

When $x(t)$ is a solution of

$$
\dot{x} = A x + Bu, \; x(0) = x_0,
$$

then $x(t- t_0)$ is a solution of 

$$
\dot{x} = A x + Bu(t-t_0), \; x(t_0) = x_0.
$$



🔍 Linear System / Heat Equation
--------------------------------------------------------------------------------

![](images/static/heat-simple.svg)

Simplified Model
--------------------------------------------------------------------------------

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


Linearization
================================================================================

Nonlinear to Linear
--------------------------------------------------------------------------------

Consider the nonlinear system

$$
\begin{array}{ccc}
\dot{x} &=& f(x, u) \\
      y &=& g(x, u)
\end{array}
$$ 

Assume that $x_e$ is an equilibrium when $u=u_e$ (cst):

$$
f(x_e, u_e) = 0
$$

and let 
  
  $$
  y_e = g(x_e, u_e)
  $$

--------------------------------------------------------------------------------

Define the error variables 

  - $\Delta x = x - x_e$, 
  
  - $\Delta u = u - u_e$ and

  - $\Delta y = y - y_e$.

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

🔍 Example
--------------------------------------------------------------------------------

The system

$$
\begin{array}{cc}
\dot{x} &=& -2x + y^3 \\
\dot{y} &=& -2y + x^3
\end{array}
$$
  
has an equilibrium at $(0, 0)$.

--------------------------------------------------------------------------------

The corresponding error variables satisfy  
$\Delta x = x$ and $\Delta y = y$, thus
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


🐍 Vector fields
--------------------------------------------------------------------------------

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


📈 Stream plot
--------------------------------------------------------------------------------

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


Asymptotic Stability
--------------------------------------------------------------------------------

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
\dot{x} = f(x, u_e)
$$

⚠️ Converse Result
--------------------------------------------------------------------------------

  - The converse is not true : the nonlinear system may be asymptotically
    stable but not its linearized approximation (e.g. consider $\dot{x} = -x^3$).

  - If we replace local *asymptotic stability* with local *exponential stability*,
    the requirement that locally

    $$
    \|x(t) - x_e\| \leq A e^{-\sigma t} \|x(0) - x_e\|
    $$
    
    for some $A >0$ and $\sigma > 0$, then it works.



🔍 Linearization
--------------------------------------------------------------------------------

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


🧩 Pendulum
--------------------------------------------------------------------------------

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

🔓 Pendulum
--------------------------------------------------------------------------------

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


Internal Dynamics
================================================================================

--------------------------------------------------------------------------------

We study the behavior of the solution

$$
\dot{x} = A x, \; x(0) = x_0 \in \mathbb{R}^n
$$

We try to get some understanding with the simplest cases first.

Scalar Case, Real-Valued
--------------------------------------------------------------------------------

$$
\dot{x} = a x
$$

$a \in \mathbb{R}$, $x(0) = x_0 \in \mathbb{R}$.

--------------------------------------------------------------------------------

**Solution:**
$$
x(t) = e^{a t} x_0
$$

**Proof:**
$$
\frac{d}{dt} e^{at} x_0 = a e^{at} x_0 = a x(t)
$$
and
$$
x(0) = e^{a \times 0} x_0 = x_0.
$$

📈 Trajectory
--------------------------------------------------------------------------------
    
```python    
a = 2.0; x0 = 1.0
figure()
t = linspace(0.0, 3.0, 1000)
plot(t, exp(a*t)*x0, "k")
xlabel("$t$"); ylabel("$x(t)$"); title(f"$a={a}$")
grid(); axis([0.0, 2.0, 0.0, 10.0])
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-2")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-2.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

📈
--------------------------------------------------------------------------------

```python
figure()
plot(real(a), imag(a), "x", color="k", ms=10.0)
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$")
grid(True)
```


::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout() 
save("images/scalar-LTI-2-poles")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-2-poles.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::



📈
--------------------------------------------------------------------------------
    
```python
a = 1.0; x0 = 1.0
figure()
t = linspace(0.0, 3.0, 1000)
plot(t, exp(a*t)*x0, "k")
xlabel("$t$"); ylabel("$x(t)$"); title(f"$a={a}$")
grid(); axis([0.0, 2.0, 0.0, 10.0])
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-1")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-1.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


📈
--------------------------------------------------------------------------------

```python
figure()
plot(real(a), imag(a), "x", color="k", ms=10.0)
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$")
grid(True)
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-1-poles")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-1-poles.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

📈
--------------------------------------------------------------------------------

```python
a = 0.0; x0 = 1.0
figure()
t = linspace(0.0, 3.0, 1000)
plot(t, exp(a*t)*x0, "k")
xlabel("$t$"); ylabel("$x(t)$"); title(f"$a={a}$")
grid(); axis([0.0, 2.0, 0.0, 10.0])
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-0")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-0.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

📈
--------------------------------------------------------------------------------

```python
figure()
plot(real(a), imag(a), "x", color="k", ms=10.0)
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$")
grid(True)
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-0-poles")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-0-poles.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

📈
--------------------------------------------------------------------------------

```python
a = -1.0; x0 = 1.0
figure()
t = linspace(0.0, 3.0, 1000)
plot(t, exp(a*t)*x0, "k")
xlabel("$t$"); ylabel("$x(t)$"); title(f"$a={a}$")
grid(); axis([0.0, 2.0, 0.0, 10.0])
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-m1")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-m1.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

📈
--------------------------------------------------------------------------------

```python
figure()
plot(real(a), imag(a), "x", color="k", ms=10.0)
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$")
grid(True)
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-m1-poles")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-m1-poles.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


📈
--------------------------------------------------------------------------------

```python
a = -2.0; x0 = 1.0
figure()
t = linspace(0.0, 3.0, 1000)
plot(t, exp(a*t)*x0, "k")
xlabel("$t$"); ylabel("$x(t)$"); title(f"$a={a}$")
grid(); axis([0.0, 2.0, 0.0, 10.0])
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-m2")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-m2.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


📈
--------------------------------------------------------------------------------

```python
figure()
plot(real(a), imag(a), "x", color="k", ms=10.0)
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$")
grid(True)
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-m2-poles")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-m2-poles.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Analysis
--------------------------------------------------------------------------------

  - The origin is globally asymptotically stable when $a < 0.0$:  
    $a$ is in the open left-hand plane,

  - In this case, define the time constant $\tau = - 1 / a$:

    $$
    x(t) = e^{at} x_0 = e^{-t/\tau} x_0
    $$

--------------------------------------------------------------------------------

$\tau$ controls the time it take for the solution 
to (almost) reach to the origin:

  - when $t = \tau$, $|x(t)|$ is $\simeq$ $1/3$ of $|x_0|$;  

  - when $t = 3 \tau$, $|x(t)|$ is $\simeq$ $5 \%$ of $|x_0|$.


Vector Case, Diagonal, Real-Valued
--------------------------------------------------------------------------------

$$
\dot{x}_1 = a_1 x_1, \; x_1(0) = x_{10}
$$

$$
\dot{x}_2 = a_2 x_2, \; x_2(0) = x_{20}
$$

i.e.

$$
A = \left[
\begin{array}{cc}
a_1 &   0 \\
  0 & a_2
\end{array}
\right]
$$

--------------------------------------------------------------------------------

**Solution:** by linearity

$$
x(t) =   e^{a_1 t} \left[\begin{array}{c} x_{10} \\ 0 \end{array}\right] 
       + e^{a_2 t} \left[\begin{array}{c} 0 \\ x_{20} \end{array}\right] 
$$


📈
--------------------------------------------------------------------------------

```python
a1 = -1.0; a2 = 2.0; x10 = x20 = 1.0
figure()
t = linspace(0.0, 3.0, 1000)
x1 = exp(a1*t)*x10; x2 = exp(a2*t)*x20
xn = sqrt(x1**2 + x2**2)
plot(t, xn , "k")
plot(t, x1, "k--")
plot(t, x2 , "k--")
xlabel("$t$"); ylabel("$\|x(t)\|$"); title(f"$a_1={a1}, \; a_2={a2}$")
grid(); axis([0.0, 2.0, 0.0, 10.0])
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-m1p2")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-m1p2.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


📈
--------------------------------------------------------------------------------

```python
figure()
plot(real(a1), imag(a1), "x", color="k", ms=10.0)
plot(real(a2), imag(a2), "x", color="k", ms=10.0)
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a_1={a1}, \; a_2={a2}$")
grid(True)
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-m1p2-poles")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-m1p2-poles.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

📈
--------------------------------------------------------------------------------

```python
a1 = -1.0; a2 = -2.0; x10 = x20 = 1.0
figure()
t = linspace(0.0, 3.0, 1000)
x1 = exp(a1*t)*x10; x2 = exp(a2*t)*x20
xn = sqrt(x1**2 + x2**2)
plot(t, xn , "k")
plot(t, x1, "k--")
plot(t, x2 , "k--")
xlabel("$t$"); ylabel("$\|x(t)\|$"); title(f"$a_1={a1}, \; a_2={a2}$")
grid(); axis([0.0, 2.0, 0.0, 10.0])
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-m1m2")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-m1m2.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

📈
--------------------------------------------------------------------------------

```python
figure()
plot(real(a1), imag(a1), "x", color="k", ms=10.0)
plot(real(a2), imag(a2), "x", color="k", ms=10.0)
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a_1={a1}, \; a_2={a2}$")
grid(True)
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-m1m2-poles")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-m1m2-poles.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Analysis
--------------------------------------------------------------------------------

  - The rightmost $a_i$ determines the asymptotic behavior,

  - The origin is globally asymptotically stable 
    only when every $a_i$ is in the open left-hand plane.

Scalar Case, Complex-Valued
--------------------------------------------------------------------------------

$$
\dot{x} = a x
$$

$a \in \mathbb{C}$, $x(0) = x_0 \in \mathbb{C}$.

--------------------------------------------------------------------------------

**Solution:** formally, the same old solution

$$
x(t) = e^{at} x_0
$$

But now, $x(t) \in \mathbb{C}$:

if $a = \sigma + i \omega$ and $x_0 = |x_0| e^{i \angle x_0}$

$$
|x(t)| = |x_0| e^{\sigma t} \, \mbox{ and } \, \angle x(t) = \angle x_0 + \omega t.
$$

📈
--------------------------------------------------------------------------------

```python
a = 1.0j; x0=1.0
figure()
t = linspace(0.0, 20.0, 1000)
plot(t, real(exp(a*t)*x0), label="$\Re(x(t))$")
plot(t, imag(exp(a*t)*x0), label="$\mathrm{Im}(x(t))$")
xlabel("$t$")
legend(); grid()
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-alt-1")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-alt-1.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

--------------------------------------------------------------------------------

```python
fig = figure()
ax = fig.add_subplot(111, projection="3d")
zticks = ax.set_zticks
ax.plot(t, real(exp(a*t)*x0), imag(exp(a*t)*x0))
xticks([0.0, 20.0]); yticks([]); zticks([])
ax.set_xlabel("$t$")
ax.set_ylabel("$\Re(x(t))$")
ax.set_zlabel("$\mathrm{Im}(x(t))$")
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-3d")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-3d.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

📈
--------------------------------------------------------------------------------

```python
figure()
plot(real(a), imag(a), "x", color="k", ms=10.0)
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$")
grid(True)
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-1j-poles")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-1j-poles.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


📈
--------------------------------------------------------------------------------

```python
a = -0.5 + 1.0j; x0=1.0
figure()
t = linspace(0.0, 20.0, 1000)
plot(t, real(exp(a*t)*x0), label="$\Re(x(t))$")
plot(t, imag(exp(a*t)*x0), label="$\mathrm{Im}(x(t))$")
xlabel("$t$")
legend(); grid()
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-alt-2")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-alt-2.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


📈
--------------------------------------------------------------------------------

```python
fig = figure()
ax = fig.add_subplot(111, projection="3d")
zticks = ax.set_zticks
ax.plot(t, real(exp(a*t)*x0), imag(exp(a*t)*x0))
xticks([0.0, 20.0]); yticks([]); zticks([])
ax.set_xlabel("$t$")
ax.set_ylabel("$\Re(x(t))$")
ax.set_zlabel("$\mathrm{Im}(x(t))$")
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-3d-2")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-3d-2.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

📈
--------------------------------------------------------------------------------

```python
figure()
plot(real(a), imag(a), "x", color="k", ms=10.0)
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$")
grid(True)
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
tight_layout()
save("images/scalar-LTI-m11j-poles")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/scalar-LTI-m11j-poles.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


Analysis
--------------------------------------------------------------------------------

  - the origin is globally asymptotically stable if $a$ is in the open left-hand plane:
    $$\Re (a) < 0$$

  - if $a= \sigma + i \omega$,

      - $\tau = -1 /\sigma$ is the time constant related of the speed of convergence,

      - $\omega$ the (rotational) frequency of the (damped) oscillations.

--------------------------------------------------------------------------------

Only one step left before the (almost) general case ...

Exponential Matrix
--------------------------------------------------------------------------------

If $M \in \mathbb{C}^{n \times n}$,
the **exponential** is defined as:

$$
e^{M} = \sum_{k=0}^{+\infty} \frac{M^k}{k !} \in \mathbb{C}^{n \times n}
$$

--------------------------------------------------------------------------------


### ⚠️

The exponential of a matrix $M$ is *not* 
the matrix with elements $e^{M_{ij}}$ (the elementwise exponential).

  - elementwise exponential: **`exp`** (`numpy` module),

  - exponential: **`expm`** (`scipy.linalg` module).


🧩 Exponential Matrix
--------------------------------------------------------------------------------

Let 
  
$$
M = 
\left[
\begin{array}{cc}
0 & 1 \\
1 & 0
\end{array}
\right]
$$

--------------------------------------------------------------------------------

### 1. 🧮

Compute the exponential of $M$.

🗝️ **Hint:**

$$
\cosh x := \frac{e^x + e^{-x}}{2}, \; 
\sinh x := \frac{e^x - e^{-x}}{2}.
$$

--------------------------------------------------------------------------------

### 2. 🐍 💻 🔬 

Compute numerically: 

  - `exp(M)` (`numpy`) 
  
  - `expm(M)` (`scipy.linalg`)

and check the results consistency.

🔓 Exponential Matrix
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------

### 1. 🔓

We have 

$$
M = 
\left[
\begin{array}{cc}
0 & 1 \\
1 & 0
\end{array}
\right], \;
M^2 = 
\left[
\begin{array}{cc}
1 & 0 \\
0 & 1
\end{array}
\right]
= I
$$

and hence for any $j \in \mathbb{N}$,

$$
M^{2j+1} = 
\left[
\begin{array}{cc}
0 & 1 \\
1 & 0
\end{array}
\right], \;
M^{2j} = 
\left[
\begin{array}{cc}
1 & 0 \\
0 & 1
\end{array}
\right]
= I.
$$

--------------------------------------------------------------------------------

$$
\begin{split}
e^{M} 
  &= \sum_{k=0}^{+\infty} \frac{M^k}{k !} \\
  &= \left( \sum_{j=0}^{+\infty} \frac{1}{(2j) !} \right)I 
   + \left(\sum_{j=0}^{+\infty} \frac{1}{(2j+1) !} \right)M \\
  &= \left(\sum_{k=0}^{+\infty} \frac{1^k + (-1)^k}{2(k !)} \right)I 
   + \left(\sum_{k=0}^{+\infty} \frac{1^k - (-1)^k}{2(k !)} \right)M \\   
  &= (\cosh 1)I + (\sinh 1)M
\end{split}
$$

--------------------------------------------------------------------------------

Thus, 

$$
e^M = 
\left[
\begin{array}{cc}
\cosh 1 & \sinh 1 \\
\sinh 1 & \cosh 1
\end{array}
\right].
$$

--------------------------------------------------------------------------------

### 2. 🔓

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```{lang=python .no-exec} 
>>> M = [[0.0, 1.0], [1.0, 0.0]]
```

```{lang=python .no-exec} 
>>> exp(M)
array([[1.        , 2.71828183],
       [2.71828183, 1.        ]])
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: notebook :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
M = [[0.0, 1.0], [1.0, 0.0]]
exp(M)
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```{lang=python .no-exec} 
>>> expm(M)
array([[1.54308063, 1.17520119],
       [1.17520119, 1.54308063]])
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: notebook :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```{lang=python .no-exec} 
expm(M)
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

--------------------------------------------------------------------------------

These results are consistent:

::: slides ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```{.no-exec lang=python}
>>> array([[exp(0.0), exp(1.0)], 
...        [exp(1.0), exp(0.0)]])
array([[1.        , 2.71828183],
       [2.71828183, 1.        ]])
```

```{.no-exec lang=python}
>>> array([[cosh(1.0), sinh(1.0)], 
...        [sinh(1.0), cosh(1.0)]])
array([[1.54308063, 1.17520119],
       [1.17520119, 1.54308063]])
```
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: notebook :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
array([[exp(0.0), exp(1.0)], 
       [exp(1.0), exp(0.0)]])
```

```python
array([[exp(0.0), exp(1.0)], 
       [exp(1.0), exp(0.0)]])
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## 📝


Note that

$$
\begin{align}
\frac{d}{dt} e^{A t} &= \frac{d}{dt} \sum_{n=0}^{+\infty} \frac{A^n}{n!} t^n \\ 
&= \sum_{n=1}^{+\infty} \frac{A^{n}}{(n-1)!} t^{n-1} \\
&= A \sum_{n=1}^{+\infty} \frac{A^{n-1}}{(n-1)!} t^{n-1} 
= A e^{A t}
\end{align}
$$

--------------------------------------------------------------------------------

Thus, for any $A \in \mathbb{C}^{n\times n}$ and $x_0 \in \mathbb{C}^n$, 

$$
\frac{d}{dt} (e^{A t} x_0) 
= A (e^{At} x_0)
$$

💎 Internal Dynamics
--------------------------------------------------------------------------------

The solution of

$$
\dot{x} = A x\; \mbox{ and } \; x(0) = x_0
$$

is

$$
x(t) = e^{A t} x_0.
$$

🧩 G.A.S. $\Leftrightarrow$ L.A.
--------------------------------------------------------------------------------

📝 For any dynamical system, if the origin is a globally asymptotically stable 
equilibrium, then it is a locally attractive equilbrium.

💎 **For linear systems**, the converse result also holds. 

🚀 Let's prove this!

--------------------------------------------------------------------------------

### 1. 🧠

Show that for any linear system $\dot{x} = A x$, if the origin is locally
attractive, then it is also globally attractive. 


--------------------------------------------------------------------------------

### 2. 🧠

Show that linear system $\dot{x} = A x$, if the origin is globally attractive,
then it is also globally asymptotically stable.

🗝️ **Hint:** Consider the solutions $e_k(t) := e^{At}e_k$ associated to 
$e_k(0)=e_k$ where $(e_1, \dots, e_n)$ is the canonical basis of the 
state space.


🔓 G.A.S. $\Leftrightarrow$ L.A.
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------

### 1. 🔓

If the origin is locally attractive, then there is a $\varepsilon > 0$ such 
that for any $x_0 \in \mathbb{R}^n$ such that $\|x_0\| \leq \varepsilon$,

$$
\lim_{t \to +\infty} e^{At} x_0 = 0.
$$

--------------------------------------------------------------------------------

Now, let any $x_0 \in \mathbb{R}^n$. Since the norm of $\varepsilon x_0 /\|x_0\|$
is $\varepsilon$, and by linearity of $e^{At}$, we obtain

$$
\begin{split}
  \lim_{t \to +\infty} e^{At} x_0 
    &= \lim_{t \to +\infty} e^{At} \left(\frac{\|x_0\|}{\varepsilon} \varepsilon \frac{x_0}{\|x_0\|} \right) \\
    &= \frac{\|x_0\|}{\varepsilon} \lim_{t \to +\infty} e^{At} \left(\varepsilon \frac{x_0}{\|x_0\|} \right)\\
    &= 0.
\end{split}
$$

Thus the origin is globally attractive.

--------------------------------------------------------------------------------

### 2. 🔓

Let $X_0$ be a bounded set of $\mathbb{R}^n$. Since 
$$
x_0 = \sum_{k=1}^n x_{0k} e_k,
$$

the solution $x(t)$ of $\dot{x}=Ax$, $x(0)=x_0$ satisfies
$$
\begin{split}
x(t)
&= e^{At} x_0 = e^{At} \left(\sum_{k=1}^n x_{0k} e_k\right) 
= \sum_{k=1}^n x_{0k} e^{At} e_k.
\end{split}
$$

--------------------------------------------------------------------------------

$$
\begin{split}
\|x(t)\|
  &= \left\| \sum_{k=1}^n x_{0k} e^{At} e_k \right\| \\
  &\leq \sum_{k=1}^n |x_{0k}| \left\| e^{At} e_k \right\| \\
  &= \sum_{k=1}^n |x_{0k}| \left\| e_k(t) \right\| \\
  &\leq \left(\sum_{k=1}^n |x_{0k}|\right) \max_{k=1, \dots, n} \|e_k(t)\|
\end{split}
$$

--------------------------------------------------------------------------------

Since $X_0$ is bounded, there is a $\alpha > 0$ such that for any $x_0 = (x_{01}, \dots, x_{0n})$ in $X_0$,

$$
\|x_0\|_1 := \sum_{k=1}^n |x_{0k}| \leq \alpha.
$$

Since for every $k=1, \dots, n$, $\lim_{t\to +\infty} \|e_k(t)\| =0$,

$$
\lim_{t\to +\infty} \max_{k=1, \dots, n} \|e_k(t)\| =0.
$$

--------------------------------------------------------------------------------

Finally

$$
\begin{split}
\|x(t, x_0)\|
  &\leq \left(\sum_{k=1}^n |x_{0k}| \right) \max_{k=1, 
  \dots, n} \|e_k(t)\| \\
    &\leq \alpha \max_{k=1, \dots, n} \|e_k(t)\| \\
\end{split}
$$

Thus $\|x(t, x_0)\| \to 0$ when $t \to \infty$, uniformly w.r.t. $x_0 \in X_0$.
In other words, the origin is globally asymptotically stable.

🏷️ Eigenvalue & Eigenvector
--------------------------------------------------------------------------------

Let $A \in \mathbb{C}^n$. If $x \neq 0 \in \mathbb{C}^n$, $s\in \mathbb{C}$
and

$$
A x = s x
$$

$x$ is an **eigenvector of $A$**, $s$ is an **eigenvalue** of $A$.

The **spectrum** of $A$ is the set of its eigenvalues.   
It is  characterized by:

$$
\sigma(A) := \{s \in \mathbb{C} \; | \; \det (sI -A) = 0\}.
$$


🏷️ Modes & Poles
--------------------------------------------------------------------------------

Consider the system $\dot{x} = Ax$.

  - a **mode** of the system is an eigenvector of $A$,

  - a **pole** of the system is an eigenvalue of $A$.

💎 Stability Criteria
--------------------------------------------------------------------------------

Let $A \in \mathbb{C}^{n \times n}$.

The origin of $\dot{x} = A x$ is globally asymptotically stable 

$$\Longleftrightarrow$$
   
all eigenvalues of $A$ have a negative real part.

$$\Longleftrightarrow$$

$$
\max \{\Re \, s \; | \; s \in \sigma(A)\} < 0.
$$

--------------------------------------------------------------------------------

### Why does this criteria work?

Assume that: 

  - **$A$ is diagonalizable.**
    

(📝 very likely unless $A$ has some special structure.)


--------------------------------------------------------------------------------

Let $\sigma(A) = \{\lambda_1, \dots, \lambda_n\}.$ 

There is an invertible matrix $P \in \mathbb{C}^{n \times n}$ such that

$$
P^{-1} A P = \mathrm{diag}(\lambda_1, \dots, \lambda_n) =
\left[
\begin{array}{cccc}
\lambda_1 & 0         & \cdots & 0 \\
0         & \lambda_2 & \cdots & 0 \\
\vdots    & \vdots    & \vdots & \vdots \\
0         & \cdots    & \cdots & \lambda_n
\end{array}
\right] 
$$

--------------------------------------------------------------------------------

Thus, if $y = P^{-1} x$, $\dot{x} = A x$ is equivalent to

$$
\left|
\begin{array}{ccc}
\dot{y}_1 &=& \lambda_1 y_1 \\
\dot{y}_2 &=& \lambda_2 y_2 \\
\vdots &=& \vdots \\
\dot{y}_n &=& \lambda_n y_n \\
\end{array}
\right.
$$

The system is G.A.S. iff each component of the system is, 
which holds iff $\Re \lambda_i < 0$ for each $i$.

🧩 Spring-Mass System
--------------------------------------------------------------------------------

Consider the scalar ODE 

$$
\ddot{x} + k x = 0, \; \mbox{ with } k > 0
$$

--------------------------------------------------------------------------------

###  1. 🧮 

Represent this system as a first-order ODE.

--------------------------------------------------------------------------------

### 2. 🧠 🧮 
  
Is this system asymptotically stable? 

--------------------------------------------------------------------------------

### 3. 🧠 🧮

Do the solutions have oscillatory components?

Find the set of associated rotational frequencies.

--------------------------------------------------------------------------------

### 4. 🧠 🧮 

Same set of questions (1., 2., 3.) for

$$
\ddot{x} + b \dot{x} + k x = 0
$$ 

when $b>0$.


🔓 Spring-Mass System
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------

### 1. 🔓

$$
\frac{d}{dt}
\left[
  \begin{array}{c}
  x \\
  \dot{x}
  \end{array}
\right]
=
\left[
  \begin{array}{rr}
  0  & 1 \\
  -k & 0
  \end{array}
\right]
\left[
  \begin{array}{c}
  x \\
  \dot{x}
  \end{array}
\right]
= A 
\left[
  \begin{array}{c}
  x \\
  \dot{x}
  \end{array}
\right]
$$

--------------------------------------------------------------------------------

### 2. 🔓

We have

$$
\max \{\Re \, s \; | \; s \in \sigma(A)\} = 0,
$$

hence the system is not globally asymptotically stable.

--------------------------------------------------------------------------------

### 3. 🔓


Since

$$
\det (sI -A) 
=
\det 
  \left(
    \begin{array}{rr}
    s  & -1 \\
    k & s
  \end{array}
  \right)
=s^2 +k,
$$

the spectrum of $A$ is 

$$
\sigma (A) 
= \{s \in \mathbb{C} \; | \; \det (sI -A) = 0\} 
= \left\{ i\sqrt{k}, -i \sqrt{k} \right\}.
$$

--------------------------------------------------------------------------------

The system poles are $\pm i\sqrt{k}$. 

The general solution $x(t)$ can be decomposed as
$$
x(t) = x_+ e^{i\sqrt{k} t} + x_- e^{-i\sqrt{k}t}.
$$

Thus the components of $x(t)$ oscillate at the rotational frequency

$$
\omega = \sqrt{k}.
$$



--------------------------------------------------------------------------------

### 4. 🔓


$$
\frac{d}{dt}
\left[
  \begin{array}{c}
  x \\
  \dot{x}
  \end{array}
\right]
=
\left[
  \begin{array}{rr}
  0  & 1 \\
  -k & -b
  \end{array}
\right]
\left[
  \begin{array}{c}
  x \\
  \dot{x}
  \end{array}
\right]
= A 
\left[
  \begin{array}{c}
  x \\
  \dot{x}
  \end{array}
\right]
$$

--------------------------------------------------------------------------------

$$
\det (sI -A) 
=
\det 
  \left(
    \begin{array}{rr}
    s  & -1 \\
    k & s +b
  \end{array}
  \right)
=s^2 + bs+ k,
$$

--------------------------------------------------------------------------------

Let $\Delta := b^2 - 4k$. If $b \geq 2\sqrt{k}$, then $\Delta \geq 0$ and

$$
\sigma(A) = \left\{ \frac{-b +\sqrt{\Delta}}{2}, \frac{-b - \sqrt{\Delta}}{2} \right\}.
$$

Otherwise,

$$
\sigma(A) = \left\{ \frac{-b + i \sqrt{-\Delta}}{2}, \frac{-b - i \sqrt{-\Delta}}{2} \right\}.
$$

--------------------------------------------------------------------------------

Thus, if $b \geq 2\sqrt{k}$,

$$
\max \{\Re \, s \; | \; s \in \sigma(A)\} 
= \frac{-b +\sqrt{b^2 - 4k}}{2}
< 0
$$

and otherwise

$$
\max \{\Re \, s \; | \; s \in \sigma(A)\} 
= -\frac{b}{2} < 0.
$$

In each case, the system is globally asymptotically stable.

--------------------------------------------------------------------------------

If $b \geq 2\sqrt{k}$, the poles are real-valued; 
the components of the solution do not oscillate.

If $0 < b < 2\sqrt{k}$, the imaginary part of the poles is

$$
\pm \frac{\sqrt{4k - b^2}}2 = \pm \sqrt{k - (b/2)^2},
$$

thus the solution components oscillate at the rotational frequency

$$
\omega = \sqrt{k - (b/2)^2}.
$$


🧩 Integrator Chain
--------------------------------------------------------------------------------

Consider the system

$$
\dot{x} = J x 
\; \mbox{ with } \; 
J = 
\left[
\begin{array}{cccc}
0 & 1 & 0 & \cdots & 0 \\
0 & 0 & 1 & \cdots & 0 \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
0 & 0 & 0 & \cdots & 1 \\
0 & 0 & 0 & \cdots & 0
\end{array}
\right]
$$

--------------------------------------------------------------------------------

### 1. 🧮 

Compute the solution $x(t)$ when 

$$
x(0) =
\left[
\begin{array}{c}
0 \\
\vdots \\
0 \\
1
\end{array}
\right].
$$


--------------------------------------------------------------------------------

### 2. 🦊 🧮 


Compute the solution for an arbitrary $x(0)$

$$
x(0) =
\left[
\begin{array}{c}
x_{1}(0) \\
\vdots \\
\vdots \\
x_{n}(0)
\end{array}
\right].$$


--------------------------------------------------------------------------------

### 3. 🧮 

Same questions for the system 

$$
\dot{x} = (\lambda I + J)x
$$ 

for some $\lambda \in \mathbb{C}$. 

🗝️ **Hint:** Find the ODE satisfied by $y(t):= x(t)e^{-\lambda t}$.

--------------------------------------------------------------------------------

### 4. 🧮

Is the system asymptotically stable ? 

--------------------------------------------------------------------------------

### 5. 🧠

Why does the stability analysis of this system matter ?


🔓 Integrator Chain
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------

### 1. 🔓

Let $x=(x_1, \dots, x_n)$.

The ODE $\dot{x} = J x$ is equivalent to:
$$
\begin{array}{lcl}
\dot{x}_1 &=& x_2 \\
\dot{x}_2 &=& x_3 \\
\vdots &\vdots & \vdots \\
\dot{x}_{n-1} &=& x_n \\
\dot{x}_n &=& 0.
\end{array}
$$

--------------------------------------------------------------------------------

When $x(0) = (0, \dots, 0, 1)$, 

  - $\dot{x}_n=0$ yields $x_n(t) = 1$, then

  - $\dot{x}_{n-1}=x_n$ yields $x_{n-1}(t) = t$, 
  
  - ...

  - $\dot{x}_{k} = x_{k+1}$ yields 
    $$
    x_{k}(t) = \frac{t^{n-k}}{(n-k)!}. 
    $$

-------------------------------------------------------------------------------- 

To summarize:
$$
x(t) =
\left[
\begin{array}{c}
t^{n-1} / (n-1)! \\
\vdots \\
t^{n-1-k}/(n-1-k)! \\
\vdots \\
t \\
1
\end{array}
\right]
$$

--------------------------------------------------------------------------------

### 2. 🔓

We note that

$$
x(0)
=
x_1(0)
\left[
\begin{array}{c}
1 \\
\vdots \\
0 \\
0
\end{array}
\right]
+
\dots
+
x_{n-1}(0)
\left[
\begin{array}{c}
0 \\
\vdots \\
1 \\
0
\end{array}
\right]
+
x_n(0)
\left[
\begin{array}{c}
0 \\
\vdots \\
0 \\
1
\end{array}
\right].$$

--------------------------------------------------------------------------------

Similarly to the previous question, we find that:

$$
x(0) 
=
\left[
\begin{array}{c}
0 \\
\vdots \\
0 \\
1 \\
0
\end{array}
\right]
\; \to \;
x(t) =
\left[
\begin{array}{c}
t^{n-2} / (n-2)! \\
\vdots \\
t  \\
1 \\
0
\end{array}
\right] 
$$

--------------------------------------------------------------------------------

$$
x(0) 
=
\left[
\begin{array}{c}
0 \\
\vdots \\
1 \\
0 \\
0
\end{array}
\right]
\; \to \;
x(t) =
\left[
\begin{array}{c}
t^{n-3} / (n-3)! \\
\vdots \\
1 \\
0 \\
0
\end{array}
\right] 
$$

--------------------------------------------------------------------------------

And more generally, by linearity:

$$
x(t)
=
\left[
\begin{array}{c}
\displaystyle x_1(0) + \dots +  x_{n-1}(0) \frac{t^{n-2}}{(n-2)!} + x_n(0) \frac{t^{n-1}}{(n-1)!} \\
\vdots \\
\displaystyle x_{n-2}(0) + x_{n-1}(0) t + x_{n}(0) \frac{t^2}{2} \\
x_{n-1}(0) + x_n(0) t \\
x_n(0)
\end{array}
\right].
$$

--------------------------------------------------------------------------------

### 3. 🔓

If $\dot{x}(t) = (\lambda I + J) x(t)$ and $y(t) = x(t)e^{-\lambda t}$, then

$$
\begin{split}
\dot{y}(t) 
  &= \dot{x}(t) e^{-\lambda t} + x(t) (-\lambda e^{-\lambda t}) \\
  &= (\lambda I + J)x(t)  e^{-\lambda t} - \lambda I x(t)  e^{-\lambda t} \\
  &= J  x(t) e^{-\lambda t} \\
  &= J y(t).
\end{split}
$$

--------------------------------------------------------------------------------

Since $y(0) = x(0) e^{-\lambda 0} = x(0)$ we get

$$
x(t)
=
\left[
\begin{array}{c}
\displaystyle x_1(0) + \dots  + x_n(0) \frac{t^{n-1}}{(n-1)!} \\
\vdots \\
x_{n-1}(0) + x_n(0) t \\
x_n(0)
\end{array}
\right] e^{\lambda t}.
$$

--------------------------------------------------------------------------------

### 4. 🔓

The structure of $x(t)$ shows that

  - If $\Re \lambda < 0$, then the system is asymptotically stable.

  - If $\Re \lambda \geq 0$, then the system is not.

    For example when $x(0)= (1, 0, \dots, 0)$, we have
    $$
    x(t) = (1, 0, \dots, 0).
    $$

--------------------------------------------------------------------------------

### 5. 🔓

Every square complex matrix $A$, **even if it is not diagonalizable**,
can be decomposed into a block-diagonal matrix
where each block has the structure $\lambda I + J$.

Thus, the result of the previous question allows to prove the 
[💎 Stability Criteria] in the general case.


🧭 I/O Behavior
================================================================================

🧭 Context
--------------------------------------------------------------------------------

  - Assume that the system is **initially at rest**:

    $$
    x(0) = 0
    $$

  - Forget about the state $x(t)$ (may be unknown).

  - Study the input/output (I/O) relationship:

    $$
    u \to y
    $$

--------------------------------------------------------------------------------

In this context, we have:

  $$
  y(t) = \int_0^{t} C e^{A(t-\tau)} B u(\tau) \, d\tau + D u(t).
  $$

Causal Signals
--------------------------------------------------------------------------------

   - extend $u(t)$ and $y(t)$ by $0$ when $t<0$ (as **causal signals**).

   - introduce the **Heaviside function** defined by

     $$
     e(t) = \left|
     \begin{array}{c}
     1 & \mbox{if } \; t\geq 0, \\
     0 & \mbox{if } \; t < 0.
     \end{array}
     \right.
     $$

Impulse Response
--------------------------------------------------------------------------------

The system **impulse response** is defined by:

$$
H(t) = (C e^{At} B) \times e(t) + D \delta(t) \in \mathbb{R}^{p \times m}
$$

📝 works for general or **MIMO** systems.  
MIMO = multiple-input & multiple-output systems.

📝 $\delta(t)$ is the **unit impulse**, 
we'll get back to it (in the meantime, you may assume that $D=0$).

SISO Systems
--------------------------------------------------------------------------------

When 

$$
p = m = 1
$$ 

(single-input & single-output or **SISO** systems),

the $1 \times 1$ matrix $H(t)$ is identified with a scalar $h(t)$:

$$
H(t) = [h(t)]
$$


--------------------------------------------------------------------------------

Then, we have:

$$
y(t) = \int_{-\infty}^{+\infty} H(t - \tau) u(\tau) \, d\tau
$$

and denote $\ast$ this operation
between $H$ and $u$:

$$
y(t) = (H \ast u) (t)
$$

It's called a **convolution**.


🔍 Impulse Response
--------------------------------------------------------------------------------

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


🧩 Integrator
--------------------------------------------------------------------------------

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
  

🧩 Double Integrator
--------------------------------------------------------------------------------

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
  

🧩 Gain
--------------------------------------------------------------------------------

Let 

$$
y = K u
$$

where $u \in \mathbb{R}^m$, $y \in \mathbb{R}^p$ and 
$K \in \mathbb{R}^{p \times m}$.

--------------------------------------------------------------------------------

### 1. 🧮 

Compute the impulse response of the system.
  
  
🧩 MIMO System
--------------------------------------------------------------------------------

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

Same question but with a matrix $A$ of a different size?


🏷️ Laplace Transform
--------------------------------------------------------------------------------

Associate to a scalar signal $x(t) \in \mathbb{R}$, 
$t\in \mathbb{R}$,
the function of a complex argument $s \in \mathbb{C}$:

$$
x(s) = \int_{-\infty}^{+\infty} x(t) e^{-st} \, dt.
$$

defined when $\Re \, (s) > \sigma$ if $\|x(t)\| \leq K e^{\sigma t}$.


⚠️ Notation
--------------------------------------------------------------------------------

We use the same symbol (here "$x$") to denote: 

  - a signal $x(t)$ and

  - its Laplace transform $x(s)$
 
They are two equivalent representations of the same "object", 
but different mathematical "functions". 

If you fear some ambiguity, use named variables, e.g.:

  $$
  x(t=1) \, \mbox{ or } \, x(s=1) \, \mbox{ instead of } \, x(1).
  $$

Vector/Matrix-Valued Signals
--------------------------------------------------------------------------------

The Laplace transform 

  - of a vector-valued signal $x(t) \in \mathbb{R}^n$ or

  - of a matrix-valued signals $X(t) \in \mathbb{R}^{m \times n}$ 
  
are computed elementwise.

--------------------------------------------------------------------------------

$$
x_{i}(s) := \int_{-\infty}^{+\infty} x_{i}(t) e^{-st} \, dt.
$$

$$
X_{ij}(s) := \int_{-\infty}^{+\infty} X_{ij}(t) e^{-st} \, dt.
$$


🏷️ Rational & Causal Signals
--------------------------------------------------------------------------------

We will only deal with **rational & causal** signals:

  $$
  x(t) = \left(\sum_{\lambda \in \Lambda} p_{\lambda}(t) e^{\lambda t} \right) e(t)
  $$

where: 

  - $\Lambda$ is a finite subset of $\mathbb{C}$,

  - for every $\lambda \in \Lambda$, $p_{\lambda}(t)$ is a polynomial in $t$.


📝
--------------------------------------------------------------------------------

Such signals are **causal** since $x(t) = 0$ when $t < 0$. 

Causality: 

$$
\Leftrightarrow \deg n(s) \leq \deg d(s).
$$

They are **rational** since

  $$
  x(s) = \frac{n(s)}{d(s)}
  $$

where $n(s)$ and $d(s)$ are polynomials.


🔍 Exponential
--------------------------------------------------------------------------------

Set $x(t) = e(t) e^{a t}$.

$$
\begin{split}
x(s) &= \int_0^{+\infty} e^{at} e^{-s t} \, dt = \int_0^{+\infty} e^{(a-s) t} \, dt \\
&= \left[\frac{e^{(a-s) t}}{a-s} \right]^{+\infty}_0 = \frac{1}{s-a}
\end{split}
$$

(If $\Re (s) \geq  \Re \, (a) +\varepsilon$, then
$|e^{(a-s)t}| \leq e^{-\varepsilon t}$)


Symbolic Computations
--------------------------------------------------------------------------------

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

🧩 Laplace Transform / Ramp
--------------------------------------------------------------------------------

Compute the Laplace Transform of

$$
x(t) = t e(t)
$$



Convolution & Laplace 
--------------------------------------------------------------------------------

Let $H(t)$ be the impulse response of a system.

Its Laplace transform $H(s)$ is called the system **transfer function**.

For LTI systems in standard form, we have

$$
H(s) = C [sI - A]^{-1} B + D
$$

Operational Calculus
--------------------------------------------------------------------------------

The Laplace transform turns convolution into products:

$$
y(t) = (H \ast u)(t)
\; \Longleftrightarrow \;
y(s) = H(s) \times u(s)
$$


Graphical Language
--------------------------------------------------------------------------------

Control engineers used **block diagrams** to describe (combinations of) 
dynamical systems, with

  - "boxes" to determine the relation between input signals and output signals and

  - "wires" to route output signals to inputs signals.


🔍 Block-Diagram / Feedback
--------------------------------------------------------------------------------

![](images/static/feedback-alt.svg)  

--------------------------------------------------------------------------------

  - **Triangles** denote **gains** (scalar or matrix multipliers),

  - **Adders** sum (or substract) signals.

--------------------------------------------------------------------------------

  - **LTI systems** can be specified with:

      - (differential) equations,

      - the impulse response,

      - the transfer function,

Equivalent Systems
--------------------------------------------------------------------------------

![](images/static/equivalent-systems.svg)  


🧩 Block-Diagram / Feedback
--------------------------------------------------------------------------------

Compute the transfer function $H(s)$ of the system depicted 
in the feedback block-diagram example.



Impulse Response
--------------------------------------------------------------------------------

Why refer to $h(t)$ as the system "impulse response"?

By the way, what's an impulse?


🔍 Impulses Approximations
--------------------------------------------------------------------------------

Pick a time constant $\varepsilon > 0$ and define

$$
\delta_{\varepsilon}(t) = \frac{1}{\varepsilon} e^{-t/\varepsilon} e(t)
$$


--------------------------------------------------------------------------------

```python
def delta(t, eps=1.0):
    return exp(-t / eps) / eps * (t >= 0)
```


📈
--------------------------------------------------------------------------------

```python
figure()
t = linspace(-1,4,1000)
plot(t, delta(t, eps=1.0), "k:", label=r"$\varepsilon=1.0$")
plot(t, delta(t, eps=0.5), "k--", label=r"$\varepsilon=0.5$")
plot(t, delta(t, eps=0.25), "k", label=r"$\varepsilon=0.25$")
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

--------------------------------------------------------------------------------

![](images/impulses.svg)

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

Impulses in the Laplace Domain
--------------------------------------------------------------------------------

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
    is not defined *as a function* (issue for $t=0$) but as a *generalized
    function* $\delta(t)$, the **unit impulse**. 

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


I/O Stability
--------------------------------------------------------------------------------

A system is **I/O-stable** if there is a $K \geq 0$ such that

$$
\mbox{for any } t\geq, \|y(t)\| \leq K M
$$

whenever

$$
\mbox{for any } t\geq, \|u(t)\| \leq M
$$

There is a bound on the amplification of the input signal that the system
can provide.

📝
Also called **BIBO-stability** (for "bounded input, bounded output")


Transfer Function Poles
--------------------------------------------------------------------------------

A **pole** of the transfer function $H(s)$ is a $s \in \mathbb{C}$ such that
for at least one element $H_{ij}(s)$,

$$
|H_{ij}(s)| = +\infty.
$$

I/O-Stability Criteria
--------------------------------------------------------------------------------

A system is I/O-stable if and only if all its poles are in the open left-plane,
i.e. such that

$$
\mbox{Re}(s) < 0.
$$

Internal Stability vs I/O-Stability
--------------------------------------------------------------------------------

If the system $\dot{x} = A x$ is asymptotically stable,
then for any matrices $B$, $C$, $D$ of appropriate sizes,

$$
\begin{split}
\dot{x} &= A x + B u \\
y &= C x + Du
\end{split}
$$

is I/O-stable.

Fully Actuated & Measured System
--------------------------------------------------------------------------------

If $B=I$, $C=I$ and $D=0$, that is

  $$
  \dot{x} = A x +u, \; y = x
  $$

then $H(s) = [sI-A]^{-1}$. 

--------------------------------------------------------------------------------

Therefore, $s$ is a pole of $H$ iff it's an eigenvalue of $A$.

Thus, in this case, asymptotic stability and I/O-stability are equivalent.

This equivalence holds under much weaker conditions.

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


</style>

<link href="https://fonts.googleapis.com/css?family=Inconsolata:400,700" rel="stylesheet">

<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.css" rel="stylesheet">

