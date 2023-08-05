SciPy Stack download helper
===========================

This package simply has the packages that are part of the scipy stack as dependencies, defined
here: https://www.scipy.org/stackspec.html

This package is unofficial and contains no code. running 'pip install scipy-stack' will
install all official scipy-stack packages, if your system is able to compile them. Note that 
this will install the non-MKL version of numpy. 

Windows users may have trouble installing
Scipy using this package; the rest of the stack should
install correctly. Workaround: Download and install Numpy+MKL and Scipy wheels from
Chris Gohlke's site: http://www.lfd.uci.edu/~gohlke/pythonlibs/, then install scipy-stack.

