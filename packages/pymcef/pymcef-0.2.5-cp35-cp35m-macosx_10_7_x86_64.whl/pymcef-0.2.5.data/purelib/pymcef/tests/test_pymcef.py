import os
import unittest
from numpy.random import multivariate_normal as mn
from numpy import transpose
from pymcef import RiskMeasure, SimpleEFp

class pymcef_tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')
        means = [5, 2, 4]
        covs = [[10, -3, -1],
                [-3, 2, 1],
                [-1, 1, 4]]
        cls.returns = transpose(mn(means, covs, 5000))
        cls.returns_validation = transpose(mn(means, covs, 1000))
        return

    @classmethod
    def tearDownClass(cls):
        return

    def test_simple_abs_semi_dev(self):
        clss = pymcef_tests
        output_dir = os.path.join(clss.out_dir, 'abs_semi_dev')
        simple_ef = SimpleEFp(target_return=2.0, training_set=clss.returns,\
                              validation_set=clss.returns_validation,\
                              risk_measure=RiskMeasure.AbsoluteSemiDeviation)
        fig1 = simple_ef.plot_ef(CVar_t=2.0)
        fig2 = simple_ef.plot_performance(CVar_t=2.0)
        fig3 = simple_ef.plot_weights()
        try:
            fig1.savefig(os.path.join(output_dir, 'efficient frontier.pdf'))
            fig2.savefig(os.path.join(output_dir, 'Sharpe ratio.pdf'))
            fig3.savefig(os.path.join(output_dir, 'weights.pdf'))
        except: # pylint: disable=W0702
            pass
        return

    def test_simple_fixed_targ_und(self):
        clss = pymcef_tests
        output_dir = os.path.join(clss.out_dir, 'fixed_targ_und')
        simple_ef = SimpleEFp(target_return=2.0, training_set=clss.returns,\
                              validation_set=clss.returns_validation,
                              risk_measure=RiskMeasure.FixTargetUnderPerformance)
        fig1 = simple_ef.plot_ef(CVar_t=2.0)
        fig2 = simple_ef.plot_performance(CVar_t=2.0)
        fig3 = simple_ef.plot_weights()
        try:
            fig1.savefig(os.path.join(output_dir, 'efficient frontier.pdf'))
            fig2.savefig(os.path.join(output_dir, 'Sharpe ratio.pdf'))
            fig3.savefig(os.path.join(output_dir, 'weights.pdf'))
        except: # pylint: disable=W0702
            pass
        return

def suite():
    this_suite = unittest.TestSuite()
    this_suite.addTest(unittest.makeSuite(pymcef_tests))
    return this_suite

def run():
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())

if __name__ == '__main__':
    run()
