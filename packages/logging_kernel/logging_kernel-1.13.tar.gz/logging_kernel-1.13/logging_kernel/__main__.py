from ipykernel.kernelapp import IPKernelApp
from . import LoggingIPythonKernel

IPKernelApp.launch_instance(kernel_class=LoggingIPythonKernel)
