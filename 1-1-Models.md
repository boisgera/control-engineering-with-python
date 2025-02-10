% Models
% 👤 [Sébastien Boisgérault](mailto:Sebastien.Boisgerault@minesparis.psl.eu) 


### Control Engineering with Python

- 📖 [Course Materials](https://github.com/boisgera/control-engineering-with-python)

- ©️ [License CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

- 🏦 [ITN, Mines Paris - PSL University](https://itn.dev)



## Symbols

|     |             |     |                        |
| --- | ----------- | --- | ---------------------- |
| 🐍  | Code        | 🔍  | Worked Example         |
| 📈  | Graph       | 🧩  | Exercise               |
| 🏷️  | Definition  | 💻  | Numerical Method       |
| 💎  | Theorem     | 🧮  | Analytical Method      |
| 📝  | Remark      | 🧠  | Theory                 |
| ℹ️  | Information | 🗝️  | Hint                   |
| ⚠️  | Warning     | 🔓  | Solution               |



## 🐍 Imports

```python
from numpy import *
from numpy.linalg import *
from matplotlib.pyplot import *
```

::: notebook :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## 🔧 Notebook Configuration

```python
rcParams['figure.dpi'] = 200
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

## 🏷️ Ordinary Differential Equation (ODE)

The "simple" version:

$$
\dot{x} = f(x)
$$

where:

- **State:** $x \in \mathbb{R}^n$

- **State space:** $\mathbb{R}^n$

- **Vector field:** $f:\mathbb{R}^n \to \mathbb{R}^n$.

## 🏷️ Vector Field

- Visualize $f(x)$ as an **arrow** with origin the **point** $x$.

- Visualize $f$ as a field of such arrows.

- In the plane ($n=2$), use [quiver](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.quiver.html) from Matplotlib.

## 🐍 Helper

We define a `Q` function helper whose arguments are

- `f`: the vector field (a function) 

- `xs`, `ys`: the coordinates (two 1d arrays)

and which returns:

  - the tuple of arguments expected by `quiver`.

--------------------------------------------------------------------------------

```python
def Q(f, xs, ys):
    X, Y = meshgrid(xs, ys)
    fx = vectorize(lambda x, y: f([x, y])[0])
    fy = vectorize(lambda x, y: f([x, y])[1])
    return X, Y, fx(X, Y), fy(X, Y)
```

## 🔍 Rotation Vector Field

Consider $f(x,y) = (-y, x).$

```python
def f(xy):
    x, y = xy
    return array([-y, x])
```

---

### 📈 Vector Field

```python
figure()
x = y = linspace(-1.0, 1.0, 20)
ticks = [-1.0, 0.0, 1.0]
xticks(ticks); yticks(ticks)
gca().set_aspect(1.0)
quiver(*Q(f, x, y))
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    save("images/test_Q")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/test_Q.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## 🏷️ ODE Solution

A **solution** of $\dot{x} = f(x)$ is

- a (continuously) differentiable function $x:I \to \mathbb{R}^n,\!$

- defined on a (possibly unbounded) interval $I$ of $\mathbb{R}$,

- such that for every $t \in I,$

  $$\dot{x}(t) = dx(t)/dt = f(x(t)).$$

## 📈 Stream Plot

When $n=2$, represent a diverse set of solutions in the state space with [streamplot](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.streamplot.html) 

```python
figure()
x = y = linspace(-1.0, 1.0, 20)
gca().set_aspect(1.0)
streamplot(*Q(f, x, y), color="k")
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    save("images/test_Q2")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/test_Q2.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## 🏷️ Initial Value Problem (IVP)

Solutions $x(t)$, for $t\geq t_0$, of

$$
\dot{x} = f(x)
$$

such that

$$
x(t_0) = x_0 \in \mathbb{R}^n.
$$

## 🏷️

The **initial condition** $(t_0, x_0)$ is made of

- the **initial time** $t_0 \in \mathbb{R}$ and

- the **initial value** or **initial state** $x_0 \in \mathbb{R}^n$.

The point $x(t)$ is the **state at time** $t$.

## 🏷️ Higher-Order ODEs

(Scalar) differential equations whose structure is

$$
y^{(n)}(t) = g(y, \dot{y}, \ddot{y}, \dots, y^{(n-1)})
$$

where $n > 1$.

## 💎 Higher-Order ODEs

The previous $n$-th order ODE is equivalent to the first-order ODE

$$
\dot{x} = f(x), \, x \in \mathbb{R}^n
$$

with

$$
f(y_0, \dots, y_{n-2}, y_{n-1}) := (y_1, \dots, y_{n-1}, g(y_0, \dots, y_{n-1})).
$$

## 🗝️

The result is more obvious if we expand the first-order equation:

$$
\begin{array}{ccl}
\dot{y}_0 &=& y_1 \\
\dot{y}_1 &=& y_2 \\
\vdots &\vdots& \vdots \\
\dot{y}_n &=& g(y_0, y_1, \dots, y_{n-1})
\end{array}
$$

## 🧩 Pendulum

![](images/static/pendulum.svg){style="display: block; margin: auto;"}

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

m=1.0; b=1.0; l=1.0; g=9.81
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

---

### 1. 🧠 🧮

Establish the equations governing the pendulum dynamics.

---

### 2. 🧠 🧮

Generalize the dynamics when there is a friction torque
$c = -b \dot{\theta}$ for some $b \geq 0$.

---

We denote $\omega$ the pendulum **angular velocity**:

$$\omega := \dot{\theta}.$$

---

### 3. 🧠 🧮

Transform the dynamics into a first-order ODE with state $x = (\theta, \omega)$.

---

### 4. 📈

Draw the system stream plot when $m=1$, $\ell=1$, $g=9.81$ and $b=0$.

---

### 5. 🧠 🧮

Determine least possible angular velocity
$\omega_0 > 0$ such that when $\theta(0) = 0$ and
$\dot{\theta}(0) = \omega_0$, the pendulum reaches (or overshoots)
$\theta(t) = \pi$ for some $t>0$.


## 🔓 Pendulum

---

### 1. 🔓

The pendulum **total mechanical energy** $E$ is the sum of its
**kinetic energy** $K$ and its **potential energy** $V$:

$$
E = K + V.
$$

---

The kinetic energy depends on the mass velocity $v$:

$$
K = \frac{1}{2} m v^2 = \frac{1}{2} m \ell^2 \dot{\theta}^2
$$

The potential energy mass depends on the pendulum elevation $y$.
If we set the reference $y=0$ when the pendulum is horizontal, we have

$$
V = mg y = - mg \ell \cos \theta
$$

---

$$
\Rightarrow \; E = K+V = \frac{1}{2} m \ell^2 \dot{\theta}^2 - mg \ell \cos \theta.
$$

If the system evolves without any energy dissipation,

$$
\begin{split}
\dot{E}
&= \frac{d}{dt} \left(\frac{1}{2} m \ell^2 \dot{\theta}^2 - mg \ell \cos \theta\right) \\
&= m \ell^2 \dot{\theta}\ddot{\theta} + m g \ell (\sin \theta) \dot{\theta} \\&= 0
\end{split}
$$

$$
\Rightarrow \; m \ell^2 \ddot{\theta} + m g \ell \sin \theta = 0.
$$

---

### 2. 🔓

When there is an additional dissipative torque $c=-b\theta$, we have instead

$$
\dot{E} = c \dot{\theta} = - b\dot{\theta}^2
$$

and thus

$$
m \ell^2 \ddot{\theta} + b \dot{\theta} + m g \ell \sin \theta = 0.
$$

---

### 3. 🔓

With $\omega := \dot{\theta}$, the dynamics becomes

$$
\begin{array}{lll}
\dot{\theta} &=& \omega \\
\dot{\omega} &=& - (b/m\ell^2) \omega -(g /\ell) \sin \theta
\end{array}
$$

---

### 4. 🔓

```python
m=1.0; b=0.0; l=1.0; g=9.81
def f(theta_d_theta):
    theta, d_theta = theta_d_theta
    J = m * l * l
    d2_theta  = - b / J * d_theta
    d2_theta += - g / l * sin(theta)
    return array([d_theta, d2_theta])
```

---

### 📈

```python
figure()
theta = linspace(-1.5 * pi, 1.5 * pi, 100)
d_theta = linspace(-5.0, 5.0, 100)
labels =  [r"$-\pi$", "$0$", r"$\pi$"]
xticks([-pi, 0, pi], labels)
yticks([-5, 0, 5])
streamplot(*Q(f, theta, d_theta), color="k")
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
save("images/sstreamplot_pendulum")
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/sstreamplot_pendulum.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

---

### 5. 🔓

In the top vertical configuration, the total mechanical energy of the pendulum 
is

$$
E_{\top} = \frac{1}{2} m \ell^2 \dot{\theta}^2 - mg \ell \cos \pi = \frac{1}{2} m \ell^2 \dot{\theta}^2 + mg \ell.
$$

Hence we have at least $E_{\top} \geq mg \ell$.

---

On the other hand, in the bottom configuration,

$$
E_{\bot} = \frac{1}{2} m \ell^2 \dot{\theta}^2 - mg \ell \cos 0 = \frac{1}{2} m \ell^2 \dot{\theta}^2 - mg \ell.
$$

Hence, without any loss of energy, the initial velocity must satisfy
$E_{\bot} \geq E_{\top}$ for the mass to reach the top position.

---

That is

$$
E_{\bot} = \frac{1}{2} m \ell^2 \dot{\theta}^2 - mg \ell \geq  mg \ell = E_{\top}
$$

which leads to:

$$
|\dot{\theta}| \geq 2 \sqrt{\frac{g}{\ell}}.
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
