import unittest
import sys

def suite():
    from pymcef.tests import test_ppslp
    from pymcef.tests import test_pymcef
    this_suite = unittest.TestSuite()
    this_suite.addTest(test_ppslp.suite())
    this_suite.addTest(test_pymcef.suite())
    return this_suite

def run():
    runner = unittest.TextTestRunner(verbosity=2)
    return not runner.run(suite()).wasSuccessful()

if __name__ == '__main__':
    ret = run()
    sys.exit(ret)
