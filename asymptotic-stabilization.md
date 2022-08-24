% Asymptotic Stabilization
% 👤 [Sébastien Boisgérault](mailto:Sebastien.Boisgerault@mines-paristech.fr), 
  🏦 MINES ParisTech, PSL University
% ©️ [CC-BY 4.0 International](https://creativecommons.org/licenses/by/4.0/)


🐍 Imports
--------------------------------------------------------------------------------

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

``` python
from numpy import *
from numpy.linalg import *
from numpy.testing import *
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

🧭 Asymptotic Stabilization
--------------------------------------------------------------------------------

When the system 

$$
\dot{x} = A x, \; x \in \mathbb{R}^n
$$ 

is not asymptotically stable at the origin,

maybe there are some available inputs $u \in \mathbb{R}^m$ such that

$$
\dot{x} = A x + Bu
$$

that we can use to stabilize asymptotically the system?


🏷️ Linear Feedback
--------------------------------------------------------------------------------

We search for $u$ as a **linear feedback**: 

$$
u(t) = -K x(t)
$$ 

for some $K \in \mathbb{R}^{m \times n}$.

📝 Note
--------------------------------------------------------------------------------

In this scheme

  - ⚠️ The full system state $x(t)$ **must be measured**.

  - 🏷️ This information is then **fed back** into the system.

  - 🏷️ The feedback **closes the loop**.

🏷️ Closed-Loop Diagram
--------------------------------------------------------------------------------

![](images/static/feedback.svg)

💎 Closed-Loop Dynamics
--------------------------------------------------------------------------------

When

  $$
  \begin{array}{rcl}
  \dot{x} &=& Ax + B u \\
        u &=& - K x
  \end{array}
  $$

the state $x \in \mathbb{R}^n$ evolves according to:

  $$
  \dot{x} = (A - B K) x
  $$

💎 Reminder
--------------------------------------------------------------------------------

The closed-loop system is asymptotically stable iff every eigenvalue of the
matrix

$$
A - B K
$$

is in the open left-hand plane.

🏷️ Spectrum as a Multiset
--------------------------------------------------------------------------------

Multisets remember the multiplicity of their elements.
It's convenient to describe the spectrum of matrices:

$$
A :=
  \left[
  \begin{array}{ccc}
  1 & 0 & 0 \\
  0 & 1 & 0 \\
  0 & 0 & 2
  \end{array}
  \right]
  \, \Rightarrow \,
\sigma(A)
= \{1, 1, 2\}
$$

$$
0 \not \in \sigma(A), \, 1 \in \sigma(A), \, 1 \not \in^2 \sigma(A)
$$

$$
2 \in \sigma(A), \, 2 \in^2 \sigma(A), \, 2 \not \in^3 \sigma(A)
$$

💎 Pole Assignment
--------------------------------------------------------------------------------

#### Assumptions

  - The system 
    
    $$
    \dot{x} = A x + B u, \, x \in \mathbb{R}^n, \,u\in\mathbb{R}^p
    $$

    is controllable.

  - $\Lambda$ is a symmetric multiset of $n$ complex numbers:
  
    $$
    \Lambda = \{\lambda_1, \dots, \lambda_n\} \subset \mathbb{C}
    \; \mbox{ and } \;
    \lambda \in^k \Lambda
    \, \Rightarrow \,
    \overline{\lambda} \in^k \Lambda.
    $$


💎 Pole Assignment
--------------------------------------------------------------------------------

#### Conclusion

$\Rightarrow$ There is a matrix $K \in \mathbb{R}^{n \times m}$ such that

$$
\sigma(A - B K) = \Lambda.
$$


🔍 Pole Assignment
--------------------------------------------------------------------------------

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

--------------------------------------------------------------------------------

### 🐍 💻

```python
from scipy.signal import place_poles
A = array([[0, 1], [0, 0]])
B = array([[0], [1]])
poles = [-1, -2]
K = place_poles(A, B, poles).gain_matrix
```

--------------------------------------------------------------------------------

### 🐍

```python
assert_almost_equal(K, [[2.0, 3.0]])
eigenvalues, _ = eig(A - B @ K)
assert_almost_equal(eigenvalues, [-1, -2])
```

--------------------------------------------------------------------------------

### 🐍 📊 Spectrum

```python
figure()
x = [real(s) for s in eigenvalues]
y = [imag(s) for s in eigenvalues]
plot(x, y, "kx")
xticks([-3, -2,-1, 0,1, 2,3])
yticks([-3, -2,-1, 0,1, 2,3])
plot([0, 0], [-3, 3], "k")
plot([-3, 3], [0, 0], "k")   
title("Spectrum of $A-BK$"); grid(True)
```

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    axis("square")
    axis([-3, 3, -3, 3])

    #tight_layout()
    save("images/poles-PA")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/poles-PA.svg" data-background-size="contain"}


::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

⚠️ Limitations
--------------------------------------------------------------------------------

⛔ The `place_poles` function rejects eigenvalues whose multiplicity
is higher than the rank of $B$.

In the previous example, $\mbox{rank}\, B = 1$, so

  -  ❌ `poles = [-1, -1]` won't work. 

  -  ✔️ `poles = [-1, -2]` will.


🧩 Pole Assignment
--------------------------------------------------------------------------------

Consider the system with dynamics

$$
\begin{array}{ccr}
\dot{x}_1 &=& x_1 - x_2 + u \\
\dot{x}_2 &=& - x_1 + x_2 + u
\end{array}
$$

We apply the control law 

$$
u = -k_1 x_1 - k_2 x_2.
$$

--------------------------------------------------------------------------------

### 1. 🧮

Can we assign the poles of the closed-loop system freely 
by a suitable choice of $k_1$ and $k_2$?
    
--------------------------------------------------------------------------------

### 2. 🧠
    
Explain this result.

🔓 Pole Assignment
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------

### 1. 🔓

$$
\begin{split}
A - B K 
&=
\left[
\begin{array}{rr}
1 & -1 \\
-1 & 1
\end{array}
\right] 
- 
\left[
\begin{array}{r}
1 \\
1
\end{array}
\right] 
\left[
\begin{array}{rr}
k_1 & k_2
\end{array}
\right] \\
&=
\left[
\begin{array}{rr}
1-k_1 & -1-k_2 \\
-1-k_1 & 1-k_2
\end{array}
\right]
\end{split}
$$

--------------------------------------------------------------------------------

$$
\begin{split}
\det A- BK
&=
\det \left(
  \left[
\begin{array}{rr}
s - 1+k_1 & 1+k_2 \\
1+k_1 & s-1+k_2
\end{array}
\right]
  \right)
  \\
&= (s - 1+k_1)(s-1+k_2) - (1+k_1)(1+k_2) \\
&= s^2 + (k_1+k_2) s - 2 (k_1 + k_2)
\end{split}
$$

--------------------------------------------------------------------------------

$$
\begin{split}
\sigma(A - BK) &= \{ \lambda_1, \lambda_2 \} \\
&= \{\lambda \in \mathbb{C} \, | \, s^2 + (k_1+k_2) s - 2 (k_1 + k_2)  = 0\}.
\end{split}
$$

Since the characteristic polynomial is also
$$
(s-\lambda_1)(s-\lambda_2)
$$
we get
$$
k_1 + k_2 = - \lambda_1 - \lambda_2, \;
-2 (k_1 + k_2) = \lambda_1 \lambda_2
$$

--------------------------------------------------------------------------------

Thus we have

$$
\lambda_1 \lambda_2 = 2 (\lambda_1 + \lambda_2)
\Rightarrow \lambda_2 = \frac{2\lambda_1}{\lambda_1 - 2}
$$

and both poles cannot be assigned freely;
for example if we select $\lambda_1 =1$, we end up with $\lambda_2 = -2$.

--------------------------------------------------------------------------------

### 2. 🔓

We have not checked the assumptions of [💎 Pole Assignment] yet.

The commandability matrix is
$$
\left[B, AB \right]
=
\left[
  \begin{array}{rr}
  1 & 0 \\
  1 & 0
  \end{array}
  \right]
$$
whose rank is $1 < 2$. 

Since the system is not controllable, pole assignment 
may fail and it does here.


🧩 Pendulum
--------------------------------------------------------------------------------

Consider the pendulum with dynamics:

$$
m \ell^2 \ddot{\theta} + b \dot{\theta} + mg \ell \sin \theta = u
$$

Numerical Values: 

$$
m = 1.0, \, l = 1.0, \, b = 0.1,\, g = 9.81
$$

--------------------------------------------------------------------------------

  - 🧮
    Compute the linearized dynamics of the system around the equilibrium 
    $\theta=\pi$ and $\dot{\theta} = 0$.

  - 🧮
    Design a control law
    $$
    u = -k_{1} (\theta - \pi) - k_{2} \dot{\theta}
    $$
    such that the closed-loop linear system is asymptotically stable,
    with a time constant smaller than $10$ sec.



---------------------------------------------------------------------------------


  - 💻
    Simulate this control law on the nonlinear systems when 
    $\theta(0) = 0$ and $\dot{\theta}(0) = 0$; compare with
    the open-loop strategy that we have already considered.


🧩 Double Spring System
--------------------------------------------------------------------------------

Consider the dynamics:

$$
\begin{array}{rcl}
m_1 \ddot{x}_1 & = & -k_1 x_1 - k_2 (x_1 - x_2) - b_1 \dot{x}_1 \\
m_2 \ddot{x}_2 & = & -k_2 (x_2 - x_1) - b_2 \dot{x}_2 + u
\end{array}
$$

Numerical values:
$$
m_1 = m_2 = 1, \; k_1 = 1, k_2 = 100, \; b_1 = 0, \; b_2 = 20
$$

--------------------------------------------------------------------------------

  - 💻
    Compute the poles of the system. Is it asymptotically stable?

  - 💻
    Use a linear feedback to kill the oscillatory behavior of
    the solutions and "speed up" the eigenvalues associated to
    a slow behavior.


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