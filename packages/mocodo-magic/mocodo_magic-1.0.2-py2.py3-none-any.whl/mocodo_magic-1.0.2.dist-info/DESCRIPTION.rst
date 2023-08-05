
IPython magic extension to use Mocodo in a Jupyter Notebook.

Mocodo is an open-source tool for designing and teaching relational databases. It takes as an input a textual description of both entities and associations of an entity-relationship diagram (ERD). It outputs a vectorial drawing in SVG and a relational schema in various formats (SQL, LaTeX, Markdown, etc.).

Installation
------------

The recommended way to install the Mocodo magic extension is to use pip:

::

    pip install mocodo_magic

If this fails, ensure first you have a working Python installation (tested under 2.7 and 3.5).

Usage
-------

Load the magic extension:

::

    %load_ext mocodo_magic

Show the argument list:

::

    %mocodo --help

More
------

`Mocodo online
<http://mocodo.net/>`_

`Documentation
<https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html>`_

`Source code on GitHub
<https://github.com/laowantong/mocodo/>`_

