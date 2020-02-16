[![Build Status](https://travis-ci.org/boisgera/control-engineering-with-python.svg?branch=master)](https://travis-ci.org/boisgera/control-engineering-with-python)

Control Engineering with Python
================================================================================

### Notebooks

Two options:

  - [![Launch Binder][binder-badge]][CEIP-binder]

  - Execute the project notebooks locally: [instructions](install.md)


[binder-badge]: https://img.shields.io/badge/Launch-Binder-blue.svg?style=flat-square
[CEIP-binder]: https://mybinder.org/v2/gh/boisgera/control-engineering-with-python/gh-pages


### Program

 0. **Introduction to Control Engineering** (30 min)
    ([HTML](https://boisgera.github.io/control-engineering-with-python/intro.html),
     [PDF](https://boisgera.github.io/control-engineering-with-python/intro.pdf))

 1. **Introduction to Dynamical Systems**
    ([HTML](https://boisgera.github.io/control-engineering-with-python/odes.html),
    [PDF](https://boisgera.github.io/control-engineering-with-python/odes.pdf),
    [notebook](https://mybinder.org/v2/gh/boisgera/control-engineering-with-python/gh-pages?filepath=odes.ipynb)).

      - ODEs: definitions, numerical schemes, vizualisation (30 min). 

      - Well-posedness of IVPs (30 min).

      - Asymptotic behavior (30 min)

 2. **Linear-Time Invariant Systems**
    ([HTML](https://boisgera.github.io/control-engineering-with-python/linear-systems.html),
     [PDF](https://boisgera.github.io/control-engineering-with-python/linear-systems.pdf),
     [notebook](https://mybinder.org/v2/gh/boisgera/control-engineering-with-python/gh-pages?filepath=linear-systems.ipynb))

      - Linearization, state-space model (30 min)

      - Solutions of LTI systems, asymptotic stability (30 min)

      - I/O Behavior, Laplace domain, I/O stability (30 min)

 3. **Controllers**
    ([HTML](https://boisgera.github.io/control-engineering-with-python/controllers.html),
     [PDF](https://boisgera.github.io/control-engineering-with-python/controllers.pdf),
     [notebook](https://mybinder.org/v2/gh/boisgera/control-engineering-with-python/gh-pages?filepath=controllers.ipynb))

      - Controllability (1h)

      - Controller design: pole assignement & optimal control (1h)

 4. **Observers**
    ([HTML](https://boisgera.github.io/control-engineering-with-python/observers.html),
     [PDF](https://boisgera.github.io/control-engineering-with-python/observers.pdf),
     [notebook](https://mybinder.org/v2/gh/boisgera/control-engineering-with-python/gh-pages?filepath=observers.ipynb))

      - Observability (1h)

      - Observer design: pole assignment & optimal filtering (1h)

 5. **Application to mobile robotics** (3h)

      - Lagrangian mechanics

      - Kinematic models of mobile robots

      - Control of mobile robots

### Project

  - Problem statement (notebook): [view in github](project/Project.ipynb) or [download](https://boisgera.github.io/control-engineering-with-python/project/Project.ipynb).

### Extra resources

#### Animation of dynamical systems

Example notebook: double pendulum
  
  - [view in GitHub](https://github.com/boisgera/control-engineering-with-python/blob/master/examples/animation.ipynb),

  - [open in binder](https://mybinder.org/v2/gh/boisgera/control-engineering-with-python/gh-pages?filepath=examples/animation.ipynb).

#### Free External Resources      
      
  - [Eduardo Sontag - Mathematical Control Theory](http://www.sontaglab.org/FTPDIR/sontag_mathematical_control_theory_springer98.pdf)
  
  - [The Zodiac - Theory of Robot Control](http://www.gipsa-lab.grenoble-inp.fr/~carlos.canudas-de-wit/publications/Theory_of_robot_control.pdf)

<!--
  - [Stackoverflow: animation in iPython (check the second option of the answer with **%matplotlib notebook**)](https://stackoverflow.com/questions/35532498/animation-in-ipython-notebook/46878531#46878531)
-->

-----

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
