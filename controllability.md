% Controllability
% 👤 [Sébastien Boisgérault](mailto:Sebastien.Boisgerault@mines-paristech.fr), 
  🏦 MINES ParisTech, PSL University
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
| 💎  | Theorem     | 🧮  | Computation (Human)    |
| 📝  | Remark      | 🧠  | Theory                 |
| ℹ️  | Information | 🗝️  | Hint                   |
| ⚠️  | Warning     | 🔓  | Solution               |

🐍 Imports
--------------------------------------------------------------------------------

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
from numpy import *
from numpy.linalg import *
from numpy.testing import *
from scipy.integrate import *
from scipy.linalg import *
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


::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


🏷️ Controllability
--------------------------------------------------------------------------------

The system $\dot{x} = f(x,u)$ is **controllable** if 

  - for any $t_0 \in \mathbb{R}$, $x_0 \in \mathbb{R}^n$ and $x_f \in \mathbb{R}^n$, 

  - there are $t_f > t_0$ and $u: [t_0, t_f] \to \mathbb{R}^m$ such that

  - the solution $x(t)$ such that $x(t_0)=x_0$ satisfies

    $$
    x(t_f) = x_f.
    $$

--------------------------------------------------------------------------------

![](images/static/controllability.svg)


🏷️ Admissible Trajectory
--------------------------------------------------------------------------------

Let $x_r$ be a reference trajectory of the system state:
 $$
 x_r(t), \,  t\in[t_0, t_f].
 $$ 

 It is **admissible** if there is a function $u_r(t)$, $t \in [t_0, t_f]$ 
 such that the solution $x$ of the IVP
   $$
   \dot{x} = f(x, u_r), \; x(t_0) = x_r(t_0)
   $$
is the function $x_r$.


🔍 Car
--------------------------------------------------------------------------------

The position $d$ (in meters) of a car of mass $m$ (in kg) on a straight road
is governed by

$$
m \ddot{d} = u
$$

where $u$ the force (in Newtons) generated by its motor.

--------------------------------------------------------------------------------

The car is initially at the origin of a road and motionless.

We would like to cross the end of the road (location $d_f > 0$) 
at time $t_f > 0$ and speed $v_f$.

**Numerical values:** 
  
  - $m=1500 \, \mbox{kg}$, 

  - $t_f=10 \, \mbox{s}$, $d_f=100 \, \mbox{m}$ and $v_f=100 \, \mbox{km/h}$.

--------------------------------------------------------------------------------

### Step 1 -- Trajectory Planning

We search for a **reference trajectory** for the state

$$x_r(t) = (d_r(t), \dot{d}_r(t))$$

such that: 

  - $d_r(0)=0$, $\dot{d}_r(0) = 0$, 
  
  - $d_r(t_f) = x_f$, $\dot{d}_r(t_f) = v_f$.
    
--------------------------------------------------------------------------------

### Step 2 -- Admissibility

We check that this reference trajectory is **admissible**, 
i.e. that we can find a control $u_r(t)$ such that the solution
of the IVP is $x(t) = x_r(t)$ when $x(0) = x_r(t)$.

Admissible Trajectory
--------------------------------------------------------------------------------

Here, if $d_r$ is smooth and if we apply the control $u(t) = m\ddot{d}_r(t)$,

  $$
  m \frac{d^2}{dt^2} (d-d_r) = 0, 
  $$
  $$
  (d-d_r)(0) = 0, \; \frac{d}{dt} (d-d_r)(0)= 0.
  $$

Thus, $d(t) = d_r(t)$ -- and thus $\dot{d}(t) = \dot{d}_r(t)$ -- 
for every $t\geq 0$.


Reference Trajectory
--------------------------------------------------------------------------------

We can find $d_r$ as a third-order polynomial in $t$ 

$$
d_r(t) = \alpha t^3 + \beta t^2 + \gamma t + \delta
$$

with

$$
\alpha = \frac{v_f}{t_f^2}- 2\frac{d_f}{t_f^3}, \;
\beta = 3\frac{d_f}{t_f^2} - \frac{v_f}{tf},\;
\gamma=0, \; \delta=0.
$$

(equivalently, with $u(t)$ as an affine function of $t$).

🐍 Constants
--------------------------------------------------------------------------------

``` python
m = 1500.0
xf = 100.0
vf = 100.0 * 1000 / 3600 # m/s
tf = 10.0
alpha = vf/tf**2 - 2*xf/tf**3
beta = 3*xf/tf**2 - vf/tf
```

🐍 State & Input Evolution
--------------------------------------------------------------------------------

``` python
def x(t):
    return alpha * t**3 + beta * t**2
def d2_x(t):
    return 6 * alpha * t + 2 * beta
def u(t):
    return m * d2_x(t)
```

🐍 💻 Simulation
--------------------------------------------------------------------------------

```
y0 = [0.0, 0.0]
def fun(t, y):
    x, d_x = y
    d2_x = u(t) / m
    return [d_x, d2_x]
result = solve_ivp(
  fun, [0.0, tf], y0, dense_output=True
)
```

📊 Graph of the Distance
--------------------------------------------------------------------------------

``` python
figure()
t = linspace(0, tf, 1000)
xt = result["sol"](t)[0]
plot(t, xt)
grid(True); xlabel("$t$"); title("$d(t)$")
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/car")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/car.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


📊 Graph of the velocity
--------------------------------------------------------------------------------

``` python
figure()
vt = result["sol"](t)[1]
plot(t, 3.6 * vt)
grid(True); xlabel("$t$")
title(r"$\dot{d}(t)$ km/h")
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/car-speed")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


## {.section data-background="images/car-speed.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

🧩 Non-admissible trajectory
--------------------------------------------------------------------------------

Let $\dot{x} = A x + B u$ with $x\in \mathbb{R}^2$, $u \in \mathbb{R}$,
$$
A = \left[
\begin{array}{cc}
0 & 1 \\
0 & 0
\end{array}
\right], \; 
B = \left[
\begin{array}{cc}
0 \\
1
\end{array}
\right].
$$

--------------------------------------------------------------------------------

### 1. 🧠 

Find a smooth reference trajectory $x_r(t)$, $t\in[0, 1]$ which is not admissible.


🧩 Pendulum
--------------------------------------------------------------------------------

Consider the pendulum with dynamics:

  $$
  m \ell^2 \ddot{\theta} + b \dot{\theta} + mg \ell \sin \theta = u
  $$

--------------------------------------------------------------------------------

### 1. 🧠 🧮

Find a smooth reference trajectory that leads the
pendulum from $\theta(0)=0$ and $\dot{\theta}(0) = 0$ to
$\theta(t_f) = \pi$ and $\dot{\theta}(t_f) = 0$.

--------------------------------------------------------------------------------

### 2. 🧠 🧮 

Show that the reference trajectory is admissible and compute the
corresponding input $u(t)$ as a function of $t$ and $\theta(t)$.

--------------------------------------------------------------------------------


### 3. 💻 🧠

Simulate the result and visualize the solution.
    
What should theoretically happen after $t=t_f$ if $u(t)=0$ is applied 
when $t \geq t_f$? What does happen in reality ? Why ? How can we 
mitigate this issue?

**Numerical Values:**

$$
m = 1.0, \, l = 1.0, \, b = 0.1,\, g = 9.81, \, t_f = 10.
$$

💎 Controllability of LTI systems
--------------------------------------------------------------------------------

A system $\dot{x} = Ax + Bu$ is controllable
iff 

  - from the origin $x_0 = 0$ at $t_0=0$,

  - we can reach any state $x_f \in \mathbb{R}^n$.

🏷️ 💎 Kalman Criterion
--------------------------------------------------------------------------------

The system $\dot{x} = Ax+Bu$ ($x\in \mathbb{R}^n$) is controllable iff:

  $$
  \mathrm{rank} \, \left[B, AB, \dots, A^{n-1} B\right] = n
  $$

$[B, \dots, A^{n-1}B]$ is the **controllability matrix**.


🔍 Controllability Matrix
--------------------------------------------------------------------------------

$$
A = 
\left[ 
\begin{array}{ccc}
0 & 1 & 0 \\
0 & 0 & 1 \\
0 & 0 & 0
\end{array}
\right], \;
B = 
\left[ 
\begin{array}{c}
0 \\
0 \\
1 
\end{array}
\right]
$$

🐍 Computation
--------------------------------------------------------------------------------

``` python
def KCM(A, B):
    n = shape(A)[0]
    mp = matrix_power
    cs = column_stack
    return cs([mp(A, k) @ B for k in range(n)])
```
🐍 LTI System
--------------------------------------------------------------------------------

``` python
n = 3 
A = zeros((n, n))
for i in range(0, n-1):
    A[i,i+1] = 1.0

B = zeros((n, 1))
B[n-1, 0] = 1.0
```

🐍 Rank Condition
--------------------------------------------------------------------------------

``` python
C = KCM(A, B)

C_expected = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
assert_almost_equal(C, C_expected)

assert matrix_rank(C) == n
```

⚠️ Warnings
--------------------------------------------------------------------------------

  - This implementation of `KCM` is not optimized: fewer computations are achievable
    using the identity:

    $$
    A^n B = A \times (A^{n-1}B).
    $$

  - Rank computations are subject to (catastrophic) numerical errors;
    sensitivity analysis or symbolic computations may alleviate the problem.

🧩 Fully Actuated System
--------------------------------------------------------------------------------

Consider $\dot{x} = A x + Bu$ with 

  - $x \in \mathbb{R}^n$, 
 
  - $u \in\mathbb{R}^m$ and,

  - $\mathrm{rank} \, B = n$.

--------------------------------------------------------------------------------

### 1. 🧠 

Show that $m \geq n$.

--------------------------------------------------------------------------------

### 2. 🧮 

Is the system controllable ?

--------------------------------------------------------------------------------

### 3. 🧠 🧮

Given $x_0$, $x_f$ and $t_f > 0$, show that any smooth trajectory 
that leads from $x_0$ at time $t_0$ to $x_f$ at time $t_f$ is admissible.


🧩 Integrator Chain
--------------------------------------------------------------------------------

![](images/static/integrator-chain.svg)

$$\dot{x}_n = u, \, \dot{x}_{n-1} = x_n, \, \cdots \,, \dot{x}_1 = x_2.$$

--------------------------------------------------------------------------------

### 1. 🧠 🧮 

Show that the system is controllable

🧩 Heat Equation
--------------------------------------------------------------------------------


![](images/static/heat-simple.svg)

--------------------------------------------------------------------------------

  - $d T_1/dt = u + (T_2 - T_1)$

  - $d T_2/dt = (T_1 - T_2) + (T_3 - T_2)$

  - $d T_3/dt = (T_2 - T_3) + (T_4 - T_3)$

  - $d T_4/dt = (T_3 - T_4)$


--------------------------------------------------------------------------------

### 1. 🧠 🧮
     
Show that the system is controllable.

--------------------------------------------------------------------------------

### 2. 🧠 🧮 

Assume now that the four cells are organized as a square.

  - Is the system still controllable?

  - Why? 

  - How could you solve this problem?


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