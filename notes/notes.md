% Notes

Globally Asymptotically Stable imples Stable
--------------------------------------------------------------------------------

(given my exotic definition of G.A.S).

The aim: to show that for any $\epsilon > 0$, there is a $r >0$ such that
$|x(0)| < r$ yields $|x(t)| < \epsilon$ for any $t \geq 0$.

Denote $X(t, x_0)$ the solution $x(t)$ to $\dot{x} = f(x)$ such that
$x(t) =x_0$ (we assume that $0$ is the equilibrium, that the system is
autonomous and well-posed)

Now, assume that the system is G.A.S. Pick the open unit ball $B =  B(0,1)$ 
as the set of initial conditions. Since it is bounded, by definition of
G.A.S., there is a $\tau > 0$ such that
if $x(0) \in B$ and $t \geq \tau$ then $|x(t)| < \epsilon$, in other words,
for any $t \geq \tau$, $X(t, B) \subset B(0, \epsilon)$. Let $V = X(t,B)$;
if $x(0) \in V$, then for any $t\geq 0$, $|x(t)| < \epsilon$ (invariance
by translation in time). Now, since $0$ is an equilibrium and $0 \in B$,
$0 \in V$; since the reverse system (that goes back in time) is well-posed, 
if $|x(\tau)|$ is small enough, $<$ some $r$, then $|x(0)|$ 
is smaller than $1$ and thus $x(0) \in B$; 
thus, if $|x(0)| < r$, $x(t) \in V$ and that gives
us that $|x(t)| < \epsilon$ for any $t\geq 0$. 

Local Attractive equivalent to Globally Asymptotically Stable
--------------------------------------------------------------------------------

For $\dot{x} = A x$, $x \in \mathbb{R}^n$

Local attractive equivalent to globally attractive: use the homogeneity of
the solution $x(t)$ wrt to the initial value $x(0)$.

Globally attractive: to show that for any $\epsilon$ and any ball of radius $r$, 
there is a $\tau > 0$ such that if $x(0)$ is in the ball and $t\geq \tau$ then
$|x(t)| < \epsilon$, decompose $x(0)$ as $\sum_i \lambda_i e_i$ and use the
linearity of the flow and the fact that the system is attractive for each
of the solutions associated to $x(0) = e_i$.