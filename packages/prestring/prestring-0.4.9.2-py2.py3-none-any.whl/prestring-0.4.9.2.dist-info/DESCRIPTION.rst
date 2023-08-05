prestring
========================================

.. image:: https://travis-ci.org/podhmo/prestring.svg?branch=master
    :target: https://travis-ci.org/podhmo/prestring


this is heavily inspired by `srcgen <https://github.com/tomerfiliba/srcgen>`_ .

(todo: gentle introduction)

features
----------------------------------------

- generating code with with-syntax
- string injection after writing string

generating code with with-syntax
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

  from prestring.python import PythonModule

  m = PythonModule()

  with m.class_("Point", metaclass="InterfaceMeta"):
      with m.def_("__init__", "self", "value"):
          m.stmt("self.value = value")

      with m.def_("__str__", "self"):
          m.return_("self.value")

output is.

.. code-block:: python

  class Point(object, metaclass=InterfaceMeta)
      def __init__(self, value):
          self.value = value

      def __str__(self):
          return self.value

string injection after writing string
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

  from prestring.python import PythonModule

  m = PythonModule()

  with m.def_("setup", "config"):
      import_area = m.submodule()
      m.sep()
      for k in ["a", "b", "c", "d", "e"]:
          import_area.stmt("from .plugins import {k}_plugin", k=k)
          m.stmt("config.activate({}_plugin)", k)

  print(m)


.. code-block:: python

  def setup(config):
      from .plugins import(
          a_plugin,
          b_plugin,
          c_plugin,
          d_plugin,
          e_plugin
      )

      config.activate(a_plugin)
      config.activate(b_plugin)
      config.activate(c_plugin)
      config.activate(d_plugin)
      config.activate(e_plugin)


0.4.7

- add prestring.output.SeparatedOutput
- LazyKeywords is sorted

0.4.3

- clear if empty (e.g. go-module's  import_group)

0.4.2

- bug fix LazyArgumentsAndKeywords

0.4

- more lazy (python module)
- lazy object is cached

0.3.3

- goname function

0.3.1

- more lazy (go module)

0.3.0

- go code output support


