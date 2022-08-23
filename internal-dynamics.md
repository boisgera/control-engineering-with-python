% Internal Dynamics
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
| 💎  | Theorem     | 🧮  | Computation (Analytic) |
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

🧭
--------------------------------------------------------------------------------

We are interested in the behavior of the solution to

$$
\dot{x} = A x, \; x(0) = x_0 \in \mathbb{R}^n
$$

First, we study some elementary systems in this class.

## Scalar Case, Real-Valued

$$
\dot{x} = a x
$$

$a \in \mathbb{R}, \; x(0) = x_0 \in \mathbb{R}.$

--------------------------------------------------------------------------------

**💎 Solution:**
$$
x(t) = e^{a t} x_0
$$

**🔓 Proof:**
$$
\frac{d}{dt} e^{at} x_0 = a e^{at} x_0 = a x(t)
$$
and
$$
x(0) = e^{a \times 0} x_0 = x_0.
$$

## 📈 Trajectory

    
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

## 📈


```python
figure()
plot(real(a), imag(a), "x", color="k")
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$"); grid(True)
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



## 📈

    
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


## 📈


```python
figure()
plot(real(a), imag(a), "x", color="k")
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$"); grid(True)
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

## 📈


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

## 📈


```python
figure()
plot(real(a), imag(a), "x", color="k")
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$"); grid(True)
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

## 📈


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

## 📈


```python
figure()
plot(real(a), imag(a), "x", color="k")
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$"); grid(True)
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


## 📈


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


## 📈


```python
figure()
plot(real(a), imag(a), "x", color="k")
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$"); grid(True)
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

## 🔬 Analysis


The origin is globally asymptotically stable when 
  
$$
a < 0.0
$$  

i.e. **$a$ is in the open left-hand plane**.

--------------------------------------------------------------------------------

Let the **time constant** $\tau$ be
  
$$
\tau := 1 / |a|.
$$

When the system is asymptotically stable,

$$
x(t) = e^{-t/\tau} x_0.
$$

Quantitative Convergence
--------------------------------------------------------------------------------

$\tau$ controls the speed of convergence to the origin:

    time $t$        distance to the origin   $|x(t)|$
------------    -------------------------------------
$0$             $|x(0)|$
$\tau$          $\simeq (1/3) |x(0)|$
$3\tau$         $\simeq (5/100) |x(0)|$
$\vdots$        $\vdots$
$+\infty$       $0$


## Vector Case, Diagonal, Real-Valued


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

**🔓 Solution:** by linearity

$$
x(t) =   e^{a_1 t} \left[\begin{array}{c} x_{10} \\ 0 \end{array}\right] 
       + e^{a_2 t} \left[\begin{array}{c} 0 \\ x_{20} \end{array}\right] 
$$


## 📈


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


## 📈


```python
figure()
plot(real(a1), imag(a1), "x", color="k")
plot(real(a2), imag(a2), "x", color="k")
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

## 📈


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

## 📈


```python
figure()
plot(real(a1), imag(a1), "x", color="k")
plot(real(a2), imag(a2), "x", color="k")
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

## 🔬 Analysis


  - 💎 The rightmost $a_i$ determines the asymptotic behavior,

  - 💎 The origin is globally asymptotically stable 
    if and only if

    **every $a_i$ is in the open left-hand plane.**

## Scalar Case, Complex-Valued

$$
\dot{x} = a x
$$

$a \in \mathbb{C}$, $x(0) = x_0 \in \mathbb{C}$.

--------------------------------------------------------------------------------

**🔓 Solution:** formally, the same old solution

$$
x(t) = e^{at} x_0
$$

But now, $x(t) \in \mathbb{C}$:

if $a = \sigma + i \omega$ and $x_0 = |x_0| e^{i \angle x_0}$

$$
|x(t)| = |x_0| e^{\sigma t} \, \mbox{ and } \, \angle x(t) = \angle x_0 + \omega t.
$$

## 📈


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

## 📈


```python
figure()
plot(real(a), imag(a), "x", color="k")
gca().set_aspect(1.0)
xlim(-3,3); ylim(-3,3); 
plot([-3,3], [0,0], "k")
plot([0, 0], [-3, 3], "k")
xticks([-2,-1,0,1,2]); yticks([-2,-1,0,1,2])
title(f"$a={a}$"); grid(True)
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


## 📈


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


## 📈


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

## 📈


```python
figure()
plot(real(a), imag(a), "x", color="k")
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


## 🔬 Analysis


  - 💎 The origin is globally asymptotically stable iff 
  
    **$a$ is in the open left-hand plane: ** $\Re (a) < 0$.

  - 💎 If $a =: \sigma + i \omega$,

      - 🏷️ $\tau = 1 /|\sigma|$ is the **time constant**.

      - 🏷️ $\omega$ the **rotational frequency** of the oscillations.

## 🏷️ Exponential Matrix


If $M \in \mathbb{C}^{n \times n}$,
its **exponential** is defined as:

$$
e^{M} = \sum_{k=0}^{+\infty} \frac{M^k}{k !} \in \mathbb{C}^{n \times n}
$$

--------------------------------------------------------------------------------


### ⚠️

The exponential of a matrix $M$ is **not** 
the matrix with elements $e^{M_{ij}}$ (the elementwise exponential).

  - 🐍 elementwise exponential: **`exp`** (`numpy` module),

  - 🐍 exponential: **`expm`** (`scipy.linalg` module).


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

