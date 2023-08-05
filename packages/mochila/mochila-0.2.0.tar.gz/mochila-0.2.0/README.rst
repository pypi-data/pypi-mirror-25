Mochila
=======

.. image:: https://circleci.com/bb/arcanefoam/mochila/tree/master.svg?style=shield
     :target: https://circleci.com/bb/arcanefoam/mochila/tree/master

.. image:: https://coveralls.io/repos/bitbucket/arcanefoam/mochila/badge.svg
     :target: https://coveralls.io/bitbucket/arcanefoam/mochila

.. image:: https://readthedocs.org/projects/mochila/badge/?version=latest
     :target: http://mochila.readthedocs.io/en/latest/?badge=latest
     :alt: Documentation Status

Collections are vital for implementing algorithms: they are the bread an butter of data aggregation and processing.
For example, a collection can be used to represent the list of ingredients of a recipe.
Then, you might want your algorithm to scale the ingredients to accommodate a different number of portions than the
original recipe.
The Mochila package provides a powerful API to process data in collections in a declarative way.

QuickStart
----------

Installation
~~~~~~~~~~~~

You can download and install the latest version of this software from the Python package index (PyPI) as follows::

    pip install --upgrade mochila

Usage
~~~~~

Import the module and all or any of the collections you want to use::

    from mochila import Sequence

    s = Sequence([1,2,3])


The complete reference is hosted in `Read the Docs <http://mochila.readthedocs.io/en/latest/>`_.

Development
-----------

Development of this happens on `Bitbucket <https://bitbucket.org/arcanefoam/mochila>`_, and issues are tracked in
`Youtrack <https://mofongo.myjetbrains.com/youtrack/issues/MCH>`_.

Bug reports, patches (including tests), and documentation are very welcome!

`Contributing <CONTRIB.rst>`_ contains information on contributing to the project.