import doctest
import unittest

from osc_plugin_clone import main

suite = unittest.TestSuite()
suite.addTest(doctest.DocTestSuite(main))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
