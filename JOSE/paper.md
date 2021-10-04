---
title: 'Control Engineering with Python'
tags:
  - Python
  - Control theory
authors:
  - name: Sébastien Boisgérault
    orcid: 0000-0003-4685-8099
    affiliation: 1
affiliations:
 - name: Center for Robotics, MINES ParisTech, PSL University
   index: 1
date: 04 October 2021
bibliography: paper.bib
---

Test reference: [@Sontag98]

## Statement of Need

TODO:

  - Mix theory and numerical/visualisation methods

  - Python ecosystem (wider audience, tools more familiar, etc.)

## Learning Objectives

The course targets students with a basic knowledge of linear algebra and ordinary differential equations as well as some experience with the Python scientific tools (NumPy, Scipy, Matplotlib, Jupyter notebooks). Expertise in an application domain
of control engineering, such as mechanical engineering, electrical engineering or process engineering can be useful.

At the end of this course, students will be able to:

  - understand and apply the theoretical foundations of control systems,

  - use common numerical methods in control engineering,

  - leverage the control engineering perspective in application domains.

## Experience

TODO: convert links to bibliography?

The course material has been taught:

  - in [EMINES engineering cycle](https://www.emines-ingenieur.org/en/education/course-catalog) since 2019. In this context, the course is composed of 
  2 periods of 3 (6-hour) day. The typical student workload is in the 75--90 hour range (including the 36 hours of face-to-face teaching). The second period is
  entirely dedicated to a mobile robotics project.

  - in [MINES ParisTech master's degree in science and executive engineering](https://mines-paristech.eu/Admissions/Master-degree-in-science-and-engineering/), since 2021.
  Since the format is shorter ($3 \times 3$h plus the 1.5h exam) some subjects are dropped and the robotics project is not included.

Accordingly, the course is composed of three parts:

 1. Dynamical Systems: Models, Properties, Simulation.

 2. Controllers and Observers Design.

 3. Control Engineering for Mobile Robotics.

While parts 1 and 2 are considered standard for such an introductory course, 
part 3 is merely one possible field of application of control engineering; 
it could be replaced or complemented with alternate topics in the future.

### Course Material

A custom set of resources supports the course objectives 
with the following characteristics:

  - Digital First: all documents are available in digital form;
    they use the English language.

  - Open Knowledge: the course material is
    freely available under a permissive license.

  - Reproducible Education: the design process 
    enable and fosters reuse and modification 
    of the course material.

### Software Stack & Educational Technology

The software tools used to solve control engineering problems
belong to the [Python/SciPy ecosystem](https://www.scipy.org/). 
Mostly:

  - [NumPy](http://www.numpy.org/) for numerical arrays,

  - [Matplotlib](https://matplotlib.org/) for data visualization,

  - The [Scipy library](http://scipy.github.io/devdocs/) for
    ODEs, LTI systems, Linear Algebra, etc.

We also rely on [Jupyter notebooks](http://jupyter.org/) to define
executable documents. Notebooks can behave mostly like classic documents,
but they can also embed some editable and executable code that produces 
some dynamic content. 

### Pedagogy & Team

To provide a hands-on experience, the course contains 
at least 50% tutorials or lab sessions in small groups.
We use notebooks as a complement of classic documents, since they
foster experimentation and active learning for students.
The third and more applied part of the course should also 
contribute positively to the engagement of the less mathematically 
inclined students.

Teachers in the pedagogical team are knowledgeable 
with the mathematics of control theory, 
the software stack used in the course 
and the application domain selected in its last part. 

### Assignments & Assessment

An assignment is associated to each part of the lecture; 
it complements the tutorial and lab sessions.
The corresponding deliverable is a notebook that shall
be produced at most two weeks after the end of the part.
Up to 1/3 of the final mark will be based on the 
interactions with the teachers during the course.

# TODO

JOSE papers should:

  - [X] List all authors and affiliations.
    
  - [ ] Describe the submission, and explain its eligibility for JOSE.
    
  - [ ] Include a “Statement of Need” section, explaining how the submitted 
    artifacts contribute to computationally enabled teaching and learning, and describing how they might be adopted by others.

    -> TODO: teaching of theory & code, integrated. Not Matlab based, but 
    Python-based (scientific stack)

  - [ ] For learning modules, describe the learning objectives, content, instructional design, and experience of use in teaching and learning situations.
    
  - [ ] Tell us the “story” of the project: how did it come to be?
    
  - [ ] Cite key references, including a link to the open archive of the sofware or the learning module.

JOSE welcomes submissions with diverse educational contexts. 

  - [ ] You should write your paper for a non-specialist reader. 
  
  - [ ] Your submission should probably be around 1000 words (or around two pages).

The goal is that someone reading the JOSE paper has enough information to decide if they’d be interested in adoping the learnig module or software. Readers will want to know how the content/software has been used, and how they would adopt it. They may also want to be persuaded that the authors have put careful work on creating the material, and have experience teaching with it.