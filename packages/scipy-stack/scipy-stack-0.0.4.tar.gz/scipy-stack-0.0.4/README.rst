SciPy Stack download helper
===========================

This package simply has the packages that are part of the SciPy stack as dependencies, defined
here: https://www.scipy.org/stackspec.html . It is unofficial and contains no code. Run 'pip install 
scipy-stack' to install all official scipy-stack packages, if your system is able to compile them. Note that 
this will install the non-MKL version of numpy. 

Windows users may have trouble installing
SciPy using this package due to the absense of an official wheel; the rest of the stack should
install correctly. Workaround: Download and install Numpy+MKL and SciPy wheels (The former is a prereq
for the latter.) from Chris Gohlke's site: http://www.lfd.uci.edu/~gohlke/pythonlibs/, then install scipy-stack.