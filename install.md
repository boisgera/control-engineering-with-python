Installation 
============

To work with the project notebooks on your computer (instead of using [binder](https://mybinder.org/) in the cloud).

 1. **Install the conda package manager.** 
 
    Recommended: install [Anaconda Python 3.x distribution](https://www.anaconda.com/distribution/).  
    Alternative: install [miniconda for Python 3.x](https://docs.conda.io/en/latest/miniconda.html).

 2. **Download and extract the [zip archive](https://github.com/boisgera/control-engineering-with-python/archive/refs/heads/gh-pages.zip)** 
    of the gh-pages branch.  
    Then, open a terminal (or an "anaconda prompt") and enter the `control-engineering-with-python-gh-pages` directory.
    
 3. **Install the project dependencies** with the command:
 
        $ conda env create -f environment.yml
        
 4. **Activate the conda environment** with:
 
        $ conda activate control-engineering-with-python
        
 5. **Launch the Jupyter notebook** with
 
        $ jupyter notebook
        
    The notebook opens in a new browser tab; select the `.ipynb` file you wish to work on.
    
    
