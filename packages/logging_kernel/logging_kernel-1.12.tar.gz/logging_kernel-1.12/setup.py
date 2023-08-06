from distutils.core import setup

setup(
    name='logging_kernel',
    version='1.12',
    packages=['logging_kernel'],
    description='Logging kernel for Jupyter',
    long_description=open('README.md').read(),
    author='Anant Mittal, Christopher Brooks',
    author_email='anmittal@umich.edu',
    url='https://github.com/anantmittal/logging_kernel',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ]
)
