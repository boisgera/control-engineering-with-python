# Control Engineering with Python

[![Build Status](https://github.com/boisgera/control-engineering-with-python/workflows/build/badge.svg)](https://github.com/boisgera/control-engineering-with-python/actions) ![Discord](https://img.shields.io/discord/1338161489567023187?logo=discord&logoColor=white)

<!--
### Notations

| Symbol | Meaning     | Symbol | Meaning                |
| ------ | ----------- | ------ | ---------------------- |
| 🐍     | Code        | 🔍     | Worked Example         |
| 📈     | Graph       | 🧩     | Exercise               |
| 🏷️     | Definition  | 💻     | Numerical Method       |
| 💎     | Theorem     | 🧮     | Analytical Method      |
| 📝     | Remark      | 🧠     | Theory                 |
| ℹ️     | Information | 🗝️     | Hint                   |
| ⚠️     | Warning     | 🔓     | Solution               |

-->

### 📚 Lecture Slides

| Chapter                       | #   | Slide Deck (HTML)             |                                   |
| ----------------------------- | --- | ----------------------------- | --------------------------------- |
| Introduction                  | 0.1 | ![HTML] [Introduction]        | [![PDF]][Introduction PDF]        |
| Dynamical Systems             | 1.1 | ![HTML] [Models]              | [![PDF]][Models PDF]              |
|                               | 1.2 | ![HTML] [Simulation]          | [![PDF]][Simulation PDF]          |
|                               | 1.3 | ![HTML] [Well-Posedness]      | [![PDF]][Well-Posedness PDF]      |
|                               | 1.4 | ![HTML] [Asymptotic Behavior] | [![PDF]][Asymptotic Behavior PDF] |
| Linear Time-Invariant Systems | 2.1 | ![HTML] [LTI Models]          | [![PDF]][LTI Models PDF]          |
|                               | 2.2 | ![HTML] [Internal Dynamics]   | [![PDF]][Internal Dynamics PDF]   |
|                               | 2.3 | ![HTML] [I/O Behavior]        | [![PDF]][I/O Behavior PDF]        |
| Controller Design             | 3.1 | ![HTML] [Controllability]     | [![PDF]][Controllability PDF]     |
|                               | 3.2 | ![HTML] [Stabilization]       | [![PDF]][Stabilization PDF]       |
|                               | 3.3 | ![HTML] [Optimal Control]     | [![PDF]][Optimal Control PDF]     |
| Observers                     | 4.1 | ![HTML] [Observers]           | [![PDF]][Observers PDF]           |

[HTML]: https://api.iconify.design/logos/html-5.svg
[PDF]: https://api.iconify.design/bi/file-pdf.svg

[Introduction]: https://boisgera.github.io/control-engineering-with-python/0-1-Introduction.html
[Models]: https://boisgera.github.io/control-engineering-with-python/1-1-Models.html
[Simulation]: https://boisgera.github.io/control-engineering-with-python/1-2-Simulation.html
[Well-Posedness]: https://boisgera.github.io/control-engineering-with-python/1-3-Well-Posedness.html
[Asymptotic Behavior]: https://boisgera.github.io/control-engineering-with-python/1-4-Asymptotic-Behavior.html
[LTI Models]: https://boisgera.github.io/control-engineering-with-python/2-1-LTI-Models.html
[Internal Dynamics]: https://boisgera.github.io/control-engineering-with-python/2-2-Internal-Dynamics.html
[I/O Behavior]: https://boisgera.github.io/control-engineering-with-python/2-3-IO-Behavior.html
[Controllability]: https://boisgera.github.io/control-engineering-with-python/3-1-Controllability.html
[Stabilization]: https://boisgera.github.io/control-engineering-with-python/3-2-Stabilization.html
[Optimal Control]: https://boisgera.github.io/control-engineering-with-python/3-3-Optimal-Control.html
[Observers]: https://boisgera.github.io/control-engineering-with-python/4-1-Observers.html

[Introduction PDF]: https://boisgera.github.io/control-engineering-with-python/0-1-Introduction.pdf
[Models PDF]: https://boisgera.github.io/control-engineering-with-python/1-1-Models.pdf
[Simulation PDF]: https://boisgera.github.io/control-engineering-with-python/1-2-Simulation.pdf
[Well-Posedness PDF]: https://boisgera.github.io/control-engineering-with-python/1-3-Well-Posedness.pdf
[Asymptotic Behavior PDF]: https://boisgera.github.io/control-engineering-with-python/1-4-Asymptotic-Behavior.pdf
[LTI Models PDF]: https://boisgera.github.io/control-engineering-with-python/2-1-LTI-Models.pdf
[Internal Dynamics PDF]: https://boisgera.github.io/control-engineering-with-python/2-2-Internal-Dynamics.pdf
[I/O Behavior PDF]: https://boisgera.github.io/control-engineering-with-python/2-3-IO-Behavior.pdf
[Controllability PDF]: https://boisgera.github.io/control-engineering-with-python/3-1-Controllability.pdf
[Stabilization PDF]: https://boisgera.github.io/control-engineering-with-python/3-2-Stabilization.pdf
[Optimal Control PDF]: https://boisgera.github.io/control-engineering-with-python/3-3-Optimal-Control.pdf
[Observers PDF]: https://boisgera.github.io/control-engineering-with-python/4-1-Observers.pdf

### ![Jupyter] Jupyter Notebooks

[Jupyter]: https://api.iconify.design/logos/jupyter.svg

The course materials are also available as Jupyter notebooks. To execute and edit them:

 0. [Install the pixi package manager.](https://pixi.sh/latest/)

 1. Download and extract this [zip archive](https://github.com/boisgera/control-engineering-with-python/archive/refs/heads/gh-pages.zip).[^1] 

 2. To browse the notebooks, inside the project directory, type the terminal command:

    ```console
    $ pixi run start
    ```
[^1]: or alternatively, if you are a git user, `git clone` the `gh-pages` branch of the current repository.
   

Alternatively, if want to use the conda package manager instead of pixi, skip step 0.,
perform step 1. as usual, and then inside the project directory, type `conda env create -f environment.yml` to create the conda project environment (once and dfor all). Then whenever you want to browse 
the notebooks, type:
```console
$ conda activate control-engineering-with-python
$ jupyter lab
```

      
### 🚀 Project

🚧 *Coming soon!* 🚧

### 📚 Open Resources

<!--
#### :computer: Animation of dynamical systems

Example notebook: double pendulum

- [view in GitHub](https://github.com/boisgera/control-engineering-with-python/blob/master/examples/animation.ipynb),

- [open in binder](https://mybinder.org/v2/gh/boisgera/control-engineering-with-python/gh-pages?filepath=examples/animation.ipynb).

--> 

- :book: [Nicolas Rougier – Scientific Visualization: Python + Matplotlib](https://hal.inria.fr/hal-03427242/document)
- :book: [Eduardo Sontag – Mathematical Control Theory](http://www.sontaglab.org/FTPDIR/sontag_mathematical_control_theory_springer98.pdf)

- :book: [Vladimír Kučera – Riccati Equations and their Solution](http://library.utia.cas.cz/separaty/2011/TR/kucera-0436431.pdf)

- :book: [The Zodiac – Theory of Robot Control](http://www.gipsa-lab.grenoble-inp.fr/~carlos.canudas-de-wit/publications/Theory_of_robot_control.pdf)

---

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
