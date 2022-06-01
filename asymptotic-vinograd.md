% Vinograd System
% 👤 [Sébastien Boisgérault](mailto:Sebastien.Boisgerault@minesparis.psl.eu), 
  🏦 Mines Paris, PSL University
% ©️ [CC-BY 4.0 International](https://creativecommons.org/licenses/by/4.0/)


🐍 Imports
--------------------------------------------------------------------------------

```python
from numpy import *
from numpy.linalg import *
from scipy.integrate import solve_ivp
from matplotlib.pyplot import *
```


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


::: notebook :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

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

Vinograd System
--------------------------------------------------------------------------------

Its behavior is ruled by

$$
\begin{array}{rcl}
\dot{x} &=& (x^2 (y-x) +y^5) / q(x,y) \\
\dot{y} &=& y^2 (y - 2x) / q(x,y)
\end{array}
$$

where 

$$
q(x, y) := x^2 + y^2 (1 + (x^2 + y^2)^2).
$$


🐍 Vector field
--------------------------------------------------------------------------------

``` python
def f(xy):
    x, y = xy
    q = x**2 + y**2 * (1 + (x**2 + y**2)**2) 
    dx = (x**2 * (y - x) + y**5) / q
    dy = y**2 * (y - 2*x) / q
    return array([dx, dy])
```

📈 Stream plot
--------------------------------------------------------------------------------

``` python
figure()
x = y = linspace(-1.0, 1.0, 1000)
streamplot(*Q(f, x, y), color="k") 
xticks([-1, 0, 1])
plot([0], [0], "k.", ms=15.0)
axis("square")
axis("off")
``` 

::: hidden :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    tight_layout()
    save("images/vinograd")

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::: slides :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

## {.section data-background="images/vinograd.svg" data-background-size="contain"}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

✍️ Question 1
--------------------------------------------------------------------------------

Show that the origin $(0, 0)$ is the only equilibrium.

::: notebook :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

If $(x, y) = (0, 0)$, we have $x^2 (y-x) +y^5 = 0$ and $y^2 (y - 2x) =0$, thus
$dx = dy = 0$. Hence, the origin is an equilibrium of the system.

Conversely, if $y^2 (y - 2x) =0$ and $x^2 (y-x) +y^5 = 0$, then either
$y=0$ or $y=2x$. If $y=0$, then $x^2 (y-x) +y^5 = -x^3 = 0$, thus $x=0$.
If $y=2x$ then $x^2 (y-x) +y^5 = x^3 +32 x^5 = x^3(1+32 x^2) = 0$, thus $x=0$.
In any case, $(\dot{x},\dot{y}) = (0,0)$ implies $(x, y)=(0,0)$ hence the origin
is the only system equilibrium.

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::




💻 Question 2
--------------------------------------------------------------------------------

Is it (experimentally) attractive ?

::: notebook :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


✍️  Question 3 (⚠️ hard!)
--------------------------------------------------------------------------------

Prove that for any equilibrium of a well-posed system:

💎 **asymptotically stable $\Rightarrow$ stable**




::: notebook :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

ℹ️ We prove directly the stronger version of A.S.

Let $X_0$ be a bounded set whose closure is included in $\mathrm{dom} \, f$.
We assume that additionally $X_0$ is closed (otherwise we substitute the closure
of $X_0$ to $X_0$).

Let $r_1 > 0$ and $B_1$ be the closed ball of radius $r_1$ centered on $x_e$.
Since the system is stable, there is a radius $r_2 > 0$ such that
for any $t \geq 0$, $x(t, B_2) \subset B_1$. Let $r_3 := r_2/2$ and 
$B_3$ be the ball of radius $r_3$ centered on $x_e$. 

Let $x_0 \in X_0$ ; since $x_e$ is attractive,
there is a $\tau \geq 0$ such that for any $t\geq \tau,$ $x(t, x_0) \in B_3$.
Since the system is well-posed, there is a radius $r_4 > 0$ such that for 
any $t \in [0, \tau],$ and any $x_1$ in the ball of radius $r_4$ centered on
$x_0$, $\|x(t, x_1) - x(t, x_0)\| \leq r_3$. Consequently,
$\|x(\tau, x_1) - x(\tau, x_0)\| \leq r_3$ and thus
$$
\begin{split}
\|x(\tau, x_1) - x(\tau, x_e)\| 
&\leq 
\|x(\tau, x_1) - x(\tau, x_0)\| +
\|x(\tau, x_0) - x(\tau, x_e)\| \\
&\leq r_3 + r_3 \\ 
&= r_2
\end{split}
$$
and thus $x(\tau, x_1) \in B_2$. 
Since $x(t, B_2) \subset B_1$ for any $t \geq \tau$, 
for any such $t$ we have 
$$
x(t, x_1) = x( t-\tau, x(\tau, x_1)) \in B_1.
$$

At this stage, we have proven that for any $r_1 > 0$ and any $x_0 \in X_0,$ there
is a $\tau(x_0) > 0$ and a $r_4(x_0)>0$ such that 
$$
\|x_1 - x_0\| \leq r_4(x_0) \; \wedge \; t\geq \tau(x_0)
\; \Rightarrow \;
\|x(t, x_1) - x_e\| \leq r_1.
$$
The collection of open balls centered on $x_0$ and of radius $r_0(x_0)$,
indexed by $x_0 \in X_0$ is an open cover of the closed set $X_0$, thus
there is a finite collection $x_0^1, \, x_0^2, \dots, \, x_0^m$ of points
of $X_0$ such that the open balls centered on $x_0^k$ with radius $r_4(x_0^k)$
cover $X_0$. Consequently, for any $x_0 \in X_0$, there is a $k \in \{1, \dots, m\}$
such that $\|x_0 - x_0^k\| \leq r_4(x_0^k)$ and thus $\|x(t, x_0) - x_e\| \leq r_1$
when $t \geq \tau(x_0^k)$. Consequently, for any $x_0 \in X_0$, if
$$
t\geq \tau := \max_{i=1,\dots,m} \tau(x_0^k),
$$
then $\|x(t, x_0) - x_e\| \leq r_1$. Thus, the equilbrium is asymptotically
stable.

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


💻 Question 4
--------------------------------------------------------------------------------

📈 Is the origin (experimentally) stable

::: notebook :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

```python
figure(figsize=(12,12))
x = y = linspace(-1.0, 1.0, 1000)
streamplot(*Q(f, x, y), color="k") 
xticks([-1, 0, 1])
plot([0], [0], "k.", ms=15.0)
axis("square")
axis("off")

def fun(t, xy):
    return f(xy)
y0 = [-0.001, 0.001]
t_span = [0.0, 10.0]
r = solve_ivp(fun=fun, y0=y0, t_span=t_span, dense_output=True)
sol = r["sol"]
t = linspace(0.0, 10.0, 1000)
x, y = sol(t)
plot(x, y, lw=5)
```

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

✍️ Question 5
--------------------------------------------------------------------------------

🧠 Is the origin asymptotically stable?

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
