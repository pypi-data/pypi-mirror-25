meshio
======

|Build Status| |codecov.io| |PyPi Version| |GitHub stars|

.. figure:: https://nschloe.github.io/meshio/pp.png
   :alt: 

There are various mesh formats available for representing unstructured
meshes, e.g.,

-  `ANSYS
   msh <http://www.afs.enea.it/fluent/Public/Fluent-Doc/PDF/chp03.pdf>`__
-  `DOLFIN
   XML <http://manpages.ubuntu.com/manpages/wily/man1/dolfin-convert.1.html>`__
-  `Exodus <https://cubit.sandia.gov/public/13.2/help_manual/WebHelp/finite_element_model/exodus/block_specification.htm>`__
-  `H5M <https://press3.mcs.anl.gov/sigma/moab/h5m-file-format>`__
-  `Medit <https://people.sc.fsu.edu/~jburkardt/data/medit/medit.html>`__
-  `Gmsh <http://gmsh.info/doc/texinfo/gmsh.html#File-formats>`__
-  `OFF <http://segeval.cs.princeton.edu/public/off_format.html>`__
-  `PERMAS <http://www.intes.de>`__
-  `VTK <http://www.vtk.org/wp-content/uploads/2015/04/file-formats.pdf>`__
-  `VTU <http://www.vtk.org/Wiki/VTK_XML_Formats>`__
-  `XDMF/XDMF3 <http://www.xdmf.org/>`__

meshio can read and write all of these formats and smoothly converts
between them. Simply call

::

    meshio-convert input.msh output.vtu

with any of the supported formats.

In Python, simply call

.. code:: python

    points, cells, point_data, cell_data, field_data = \
        meshio.read(args.infile)

to read a mesh. To write, do

.. code:: python

    meshio.write(
        args.outfile,
        points,
        cells,
        point_data=point_data,
        cell_data=cell_data,
        field_data=field_data
        )

For both input and output, you can optionally specify the exact
``file_format`` (in case you would like to enforce binary over ASCII
VTK, for example).

Installation
~~~~~~~~~~~~

meshio is `available from the Python Package
Index <https://pypi.python.org/pypi/meshio/>`__, so simply type

::

    pip install -U meshio

to install or upgrade.

Usage
~~~~~

Just

::

    import meshio

and make use of all the goodies the module provides.

Testing
~~~~~~~

To run the meshio unit tests, check out this repository and type

::

    pytest

Distribution
~~~~~~~~~~~~

To create a new release

1. bump the ``__version__`` number,

2. tag and upload to PyPi:

   ::

       make publish

License
~~~~~~~

meshio is published under the `MIT
license <https://en.wikipedia.org/wiki/MIT_License>`__.

.. |Build Status| image:: https://travis-ci.org/nschloe/meshio.svg?branch=master
   :target: https://travis-ci.org/nschloe/meshio
.. |codecov.io| image:: https://codecov.io/github/nschloe/meshio/branch/master/graphs/badge.svg
   :target: https://codecov.io/github/nschloe/meshio/branch/master
.. |PyPi Version| image:: https://img.shields.io/pypi/v/meshio.svg
   :target: https://pypi.python.org/pypi/meshio
.. |GitHub stars| image:: https://img.shields.io/github/stars/nschloe/meshio.svg?style=social&label=Star&maxAge=2592000
   :target: https://github.com/nschloe/meshio


