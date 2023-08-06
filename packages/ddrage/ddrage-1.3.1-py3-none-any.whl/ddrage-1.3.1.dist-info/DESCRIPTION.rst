#############################
ddRAGE - ddRAD Data Generator
#############################


ddRAGE (ddRAD Data Generator) is a software to simulate double digest restriction site associated DNA sequencing reads.
The generated data sets can be used to test ddRAD analysis tools and validate their results.

The documentation, including a tutorial, can be found `here <https://ddrage.readthedocs.io/>`_.
The code is hosted on `bitbucket`_, `PyPI`_, and `bioconda`_.

.. _bitbucket: https://bitbucket.org/genomeinformatics/rage
.. _PyPI: https://pypi.python.org/pypi/ddrage/
.. _bioconda: https://bioconda.github.io/recipes/ddrage/README.html


*******************
System Requirements
*******************

- python >= 3.5
- numba
- numpy
- matplotlib
- pyyaml
- scipy


For the docs:

- sphinx

For parameter visualization:

- bokeh


************
Installation
************

We recommend the installation using conda:

.. code-block:: shell

   $ conda create -n ddrage -c bioconda ddrage
   $ source activate ddrage

Alternatively, you can download the source code from `bitbucket`_ and install it using the setup script:

.. code-block:: shell

   $ git clone https://bitbucket.org/genomeinformatics/rage.git ddrage
   $ cd ddrage
   /rage$ python setup.py install

In this case you have to install the requirements listed above.


*****
Usage
*****

To simulate a ddRAD data set, call ddrage from the command line:

.. code-block:: shell

   $ ddrage

you can specify parameters to change data set parameters such as number of individuals (``-n``), nr of loci (``-l``), and coverage (``--coverage``):

.. code-block:: shell

   $ ddrage -n 6 -l 10000 --coverage 30

This creates a data set with reads from 6 individuals at 10000 loci with an expected coverage of 30.

A more detailed tutorial can be found `on readthedocs <https://ddrage.readthedocs.io/en/latest/getting-started/>`_.


