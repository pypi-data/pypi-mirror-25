## logging_kernel
===========

``logging_kernel`` is an extension of a Jupyter kernel. 

## Jupyter Version
```
jupyter --version
4.3.0
```

## Installation
------------
To install ``logging_kernel`` from PyPI::
```
    pip install logging_kernel
    python -m logging_kernel.install
```

## Using the Logging kernel
---------------------
**Notebook**: The *New* menu in the notebook should show an option for an Logging notebook.

## Installing and Enabling the logging_ext extension

### Change your folder to jupyter_extension
```
cd jupyter_extension
```

### Install and Enable
```
rm ~/.jupyter/nbconfig/notebook.json; jupyter nbextension install . --user; jupyter nbextension enable logging_ext; 
```
### You should see the below text if everything goes well
```
Enabling notebook extension logging_ext...
      - Validating: OK

```

## Remove the original python kernel options from the jupyter notebook
### Check the kernels with below command
```
jupyter kernelspec list
```
### Remove the kernel.json file from the python folder
```
rm ~/<>/jupyter/kernels/python/kernel.json
```



# Creating pip package

## Create setup.py file

```
from setuptools import setup
 
setup(
     name='my-awesome-helloworld-script',    # This is the name of your PyPI-package.
     version='0.1',                          # Update the version number for new releases
     scripts=['helloworld']                  # The name of your scipt, and also the command you'll be using for calling it
)
```

## Set up PyPi account
```
python setup.py register
```

## Create ~/.pypirc file
```
[distutils]
 index-servers =
     pypi

 [pypi]
 repository: https://upload.pypi.org/legacy/
 username:
 password:

```

## Upload your package
```
python setup.py sdist upload
```
