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

Asymptotic Stabilization
--------------------------------------------------------------------------------

When the system 

$$
\dot{x} = A x, \; x \in \mathbb{R}^n
$$ 

is not asymptotically stable at the origin,

maybe there are some inputs $u \in \mathbb{R}^m$ such that

$$
\dot{x} = A x + Bu
$$

that we can use to stabilize asymptotically the system?


Linear Feedback
--------------------------------------------------------------------------------

We can try to compute $u$ as 

$$
u(t) = -K x(t)
$$ 

for some $K \in \mathbb{R}^{m \times n}$

📝 Note
--------------------------------------------------------------------------------

In this scheme

  - The full system state $x(t)$ must be **measured**.

  - This information is then **fed back** into the system.


Closed-Loop Diagram
--------------------------------------------------------------------------------

![](images/static/feedback.svg)

Closed-Loop Dynamics
--------------------------------------------------------------------------------

When

  $$
  \begin{array}{ccc}
  \dot{x} = Ax + B u \\
  u = - K x
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


💎 Pole Assignment
--------------------------------------------------------------------------------

Assume that:

  - The systems $\dot{x} = A x + Bu$ is controllable.

  - Let $\Lambda = \{\lambda_1, \dots, \lambda_n\} \in \mathbb{C}^n$
    be a (multi-)set of complex numbers (a value may appear several times) 
    which is symmetric:  
    
    if $\lambda \in \Lambda$,
    then $\overline{\lambda} \in \Lambda$ (with the same multiplicity)

💎 Pole Assignment
--------------------------------------------------------------------------------

Then,

  - Let $\sigma(A - BK)$ denote the (multi-)set 
    of eigenvalues of $A - B K$ (counted with their multiplicity).

  - Then there is a matrix $K$ such that

    $$
    \sigma(A - B K) = \Lambda.
    $$


🔎 Stabilization/Pole Assignment
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

    from scipy.signal import place_poles
    A = array([[0, 1], [0, 0]])
    B = array([[0], [1]])
    poles = [-1, -2]
    K = place_poles(A, B, poles).gain_matrix

--------------------------------------------------------------------------------

    assert_almost_equal(K, [[2.0, 3.0]])
    eigenvalues, _ = eig(A - B @ K)
    assert_almost_equal(eigenvalues, [-1, -2])

📊 Eigenvalue Location
--------------------------------------------------------------------------------

    figure()
    x = [real(s) for s in eigenvalues]
    y = [imag(s) for s in eigenvalues]
    plot(x, y, "kx", ms=12.0)
    xticks([-3, -2,-1, 0,1, 2,3])
    yticks([-3, -2,-1, 0,1, 2,3])
    plot([0, 0], [-3, 3], "k")
    plot([-3, 3], [0, 0], "k")   
    title("Eigenvalues")
    grid(True)

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    axis("square")
    axis([-3, 3, -3, 3])

    #tight_layout()
    save("images/poles-PA")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/poles-PA.svg" data-background-size="contain"}


::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

⚠️ Implementation detail
--------------------------------------------------------------------------------

  - The `place_poles` function will not accept eigenvalues whose multiplicity
is higher than the rank of $B$.

  - So here `poles = [-1, -1]` won't work. 

  - But `poles = [-1, -1.001]` may work.


🧩 Pole Assignment / Default
--------------------------------------------------------------------------------

Consider the system with dynamics

$$
\begin{array}{ccr}
\dot{x}_1 &=& x_1 - x_2 + u \\
\dot{x}_2 &=& - x_1 + x_2 + u
\end{array}
$$

--------------------------------------------------------------------------------

  - [🧮]
    We apply the control law 
    $$u = -k_1 x_1 - k_2 x_2;$$
    can we move the poles of the system where we want by
    a suitable choice of $k_1$ and $k_2$?
    
  - [🧠] 
    Explain this result.

--------------------------------------------------------------------------------

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
  /* max-height: 80wh; won't work, overriden */
}

/*
.reveal .slides .left {
  text-align: left;
}
*/

input {
  font-family: "Source Sans Pro", Helvetica, sans-serif;
  font-size: 42px;
  line-height: 54.6px;
}

code span.kw {
  color: inherit;
  font-weight: normal;
}

code span.cf { /* return */
  color: inherit;
  font-weight: normal;
}

code span.fl { /* floats */
  color: inherit;
}

code span.dv { /* ints */
  color: inherit;
}

code span.co { /* comments */
  font-style: normal;
  color: #adb5bd; /* gray 5 */}

code span.st { /* strings */
  color: inherit;
}

code span.op { /* +, = */
  color: inherit;
}



</style>

<link href="https://fonts.googleapis.com/css?family=Inconsolata:400,700" rel="stylesheet"> 

<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.css" rel="stylesheet">
