from setuptools import setup, find_packages

# files = ["src/*"]


setup(
      name="msh",
      version="0.10",
      keywords='mac ssh',
      description="mac ssh client",
      author="wls",
      url="",
      license="LGPL",
      python_requires='==2.7.*',
      install_requires=['pexpect','ipaddress'],
      packages= find_packages(),
      scripts=["scripts/msh"],

      )
