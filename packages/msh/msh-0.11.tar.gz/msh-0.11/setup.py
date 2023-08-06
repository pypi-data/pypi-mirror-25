from setuptools import setup, find_packages

# files = ["src/*"]


setup(
      name="msh",
      version="0.11",
      keywords='mac ssh',
      description="mac ssh client(linux can also use)",
      author="wls",
      author_email="wanglongshengdf@126.com",
      url="",
      license="GNU",
      python_requires='==2.7.*',
      install_requires=['pexpect','ipaddress'],
      packages=find_packages(),
      scripts=["scripts/msh"],
      )
