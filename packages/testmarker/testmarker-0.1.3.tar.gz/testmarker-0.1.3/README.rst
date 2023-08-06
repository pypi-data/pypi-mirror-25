testmarker
========================================

Marker library for unittest.


install
----------------------------------------

.. code-block::

  pip install testmarker

run tests with marker
----------------------------------------

Running tests like a `python -m unittest discover`.

.. code-block:: shell

  make[1]: Entering directory '$HOME/my/testmarker/examples'
  python -m testmarker discover foo --verbose
  test_it (foo.tests.test_it.Test0) ... ok
  test_it (foo.tests.test_it.Test1) ... ok
  test_it (foo.tests.test_it.Test2) ... ok
  test_it (foo.tests.test_it.Test3) ... ok
  test_it (foo.tests.test_it.Test4) ... ok
  test_it (foo.tests.test_it.Test5) ... skipped 'f is default skipped'
  test_it (foo.tests.test_it.Test6) ... ok
  
  ----------------------------------------------------------------------
  Ran 7 tests in 0.000s
  
  OK (skipped=1)
  python -m testmarker discover foo --ignore a,b --ignore c --verbose
  test_it (foo.tests.test_it.Test0) ... skipped 'a'
  test_it (foo.tests.test_it.Test1) ... skipped 'b'
  test_it (foo.tests.test_it.Test2) ... skipped 'c'
  test_it (foo.tests.test_it.Test3) ... ok
  test_it (foo.tests.test_it.Test4) ... ok
  test_it (foo.tests.test_it.Test5) ... skipped 'f is default skipped'
  test_it (foo.tests.test_it.Test6) ... ok
  
  ----------------------------------------------------------------------
  Ran 7 tests in 0.000s
  
  OK (skipped=4)
  python -m testmarker discover foo --only a,b --verbose
  test_it (foo.tests.test_it.Test0) ... ok
  test_it (foo.tests.test_it.Test1) ... ok
  test_it (foo.tests.test_it.Test2) ... skipped 'c'
  test_it (foo.tests.test_it.Test3) ... skipped 'd'
  test_it (foo.tests.test_it.Test4) ... skipped 'e'
  test_it (foo.tests.test_it.Test5) ... skipped 'f is default skipped'
  skipped 'Test6 is skipped by --only option'
  
  ----------------------------------------------------------------------
  Ran 6 tests in 0.000s
  
  OK (skipped=5)
  make[1]: Leaving directory '$HOME/my/testmarker/examples'

marker setting
----------------------------------------

examples/foo/foo/tests/test_it.py

.. code-block:: python

  import unittest
  from testmarker import mark
  
  
  @mark.a
  class Test0(unittest.TestCase):
      def test_it(self):
          pass
  
  
  @mark.b
  class Test1(unittest.TestCase):
      def test_it(self):
          pass
  
  
  @mark.c
  class Test2(unittest.TestCase):
      def test_it(self):
          pass
  
  
  @mark.d
  class Test3(unittest.TestCase):
      def test_it(self):
          pass
  
  
  @mark.e
  class Test4(unittest.TestCase):
      def test_it(self):
          pass
  
  
  @mark("f", description="f is default skipped", skip=True)
  class Test5(unittest.TestCase):
      def test_it(self):
          pass
  
  
  class Test6(unittest.TestCase):
      def test_it(self):
          pass