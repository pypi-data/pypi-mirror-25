## logging_kernel
===========

``logging_kernel`` is an extension of a Jupyter kernel. 

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
```
rm ~/.jupyter/nbconfig/notebook.json; jupyter nbextension install . --user; jupyter nbextension enable logging_ext; jupyter nbextension enable logging_ext;
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
