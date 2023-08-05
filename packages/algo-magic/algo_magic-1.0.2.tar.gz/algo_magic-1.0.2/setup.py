from setuptools import setup, find_packages
from codecs import open
import algo_magic

long_description = """\
This set of IPython magic extensions is provided to the first year students enrolled in the algorithmics course at ISFATES (University of Lorraine).

Installation
------------

The recommended way to install the algo_magic extension is to use pip:

::

    pip install algo_magic

If this fails, ensure first you have a working Python 3 installation.


Usage
-----

Load the magic extensions:

::

    %load_ext algo_magic


More info
---------

`Source code on GitHub
<https://github.com/laowantong/algo_magic/>`_
"""

with open("README.rst", "w", "utf8") as f:
    f.write(long_description)

setup(
    name="algo_magic",
    version=algo_magic.__version__,
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Topic :: Database',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Framework :: IPython'
    ],
    keywords='algorithmics tools',
    zip_safe=False,
    description=("Set of IPython magic extensions used in the first year algorithmics course at ISFATES (University of Lorraine)."),
    url='https://github.com/laowantong/algo_magic',
    author='Aristide Grange',
    author_email='name.surname@univ-lorraine.fr',
    packages=find_packages(exclude=[]),
    install_requires=["ipython", "yapf"],
    long_description=long_description
)
