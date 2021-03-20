# SPM-Python Batchmaker

## Overview
This module is designed to provide an interface between python and SPM.
It provides a minimal functionality to set up first-level batches in python that are fully readable by SPM. 

## Use cases
* your local university does not provide sufficient tech support to install neuroimaging data analysis tools native to python
* you want to use SPM anyway for some reason but want to stick with python as much as possible.

## How it works
A first-level batch file can be constructed and exported in a few lines of python code using the batchmaker module. It consists of several classes that hierarchically feed into each other and internally cosntruct the data structure that SPM can read.

If one wishes to use values differing from the default parameters, this is easily achieved by adding additional arguments in the class calls. Additional conditions and sessions are automatically created with increasing size of the input arrays.