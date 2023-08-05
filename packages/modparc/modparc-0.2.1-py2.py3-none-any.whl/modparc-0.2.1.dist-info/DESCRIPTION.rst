===============================
modparc
===============================


.. image:: https://img.shields.io/pypi/v/modparc.svg
        :target: https://pypi.python.org/pypi/modparc

.. image:: https://img.shields.io/travis/xie-dongping/modparc.svg
        :target: https://travis-ci.org/xie-dongping/modparc

.. image:: https://readthedocs.org/projects/modparc/badge/?version=latest
        :target: https://modparc.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/xie-dongping/modparc/shield.svg
     :target: https://pyup.io/repos/github/xie-dongping/modparc/
     :alt: Updates


modparc is a Modelica parser in Python based on parser combinator.


* Free software: GNU General Public License v3
* Source code: https://github.com/xie-dongping/modparc.
* Documentation: https://modparc.readthedocs.io.

.. contents::

Quickstart
----------

Install the package from PyPI:

.. code-block:: bash

    $ pip install modparc


To parse a Modelica source file `"your_modelica_file.mo"`:

.. code-block:: python

    import modparc
    model_definition = modparc.parse_file("your_modelica_file.mo")

To list all the equations in the `model_definition` instance:

.. code-block:: python

    all_equations = model_definition.search('Equation')
    for equation in all_equations:
        print(equation.code())  # The code of the equation as string

To get the name of the model loaded:

.. code-block:: python

    print(model_definition.name())  # get the name of the stored class
    print(model_definition.class_type())  # get the type of the class

Features
--------

* Experimentally parses Modelica Standard Library 3.2.1
* Search element of a certain class

Known Issues
------------

* Handling tokenization of Q-IDENT and comments, which comes first?
* Assertion syntax not defined in Modelica specification
* Default recursion depth is not enough for long vector literals
* Cyclic import is neccessary for the Modelica syntax definition

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

The test cases used code from the `ModelicaByExample library (MIT License by Michael Tiller)`_.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`ModelicaByExample`: https://github.com/xogeny/ModelicaBook




=======
History
=======

0.1.5 (2016-10-22)
------------------

* First release on PyPI.

0.2.0 (2016-10-22)
------------------

* Get names and types of the defintions
* Roundtripping of the defintions


