from ipykernel.kernelapp import IPKernelApp
from .kernel import LuaKernel
IPKernelApp.launch_instance(kernel_class=LuaKernel)
