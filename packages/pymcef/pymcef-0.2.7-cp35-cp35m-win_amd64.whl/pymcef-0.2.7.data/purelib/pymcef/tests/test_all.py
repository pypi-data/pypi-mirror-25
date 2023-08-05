import unittest

def suite():
    from pymcef.tests import test_ppslp
    from pymcef.tests import test_pymcef
    this_suite = unittest.TestSuite()
    this_suite.addTest(test_ppslp.suite())
    this_suite.addTest(test_pymcef.suite())
    return this_suite

def run():
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())

if __name__ == '__main__':
    run()
