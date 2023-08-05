try:
    from math import inf
except ImportError:
    inf = float('inf')
import unittest
import numpy as np

from pymcef.ppslp import dictionary
'''
this test is based on the following returns
10 1 5
1 -2 0 -1
2 -3 1 -3
'''
class dictionary_tests(unittest.TestCase):
    def test_simple_dictionary_operation_fixed_target(self):
        benchmark_weights = [{0: 1.0}, {0: 0.25, 1: 0.75}, {1: 1.0}]
        benchmark_risks = [1.66666666666667, 0.166666666666667, 0.0]
        benchmark_rewards = [1.66666666666667, 0.916666666666667, 0.666666666666667]
        benchmark_omegas = [2.0, 6.5, inf]
        benchmark_sds = [7.23417813807024, 2.03613195381177, 0.577350269189626]
        benchmark_sharpes = [0.230387838792046, 0.450200029988532, 1.15470053837925]
        benchmark_lbd_l = [2, 0.666666666666667, -1]
        benchmark_lbd_u = [inf, 2, 0.666666666666667]

        # initialize a dictionary from realizations, three assets, three realizations,
        # each row corresponds with one asset
        dense = np.array([[10.0, -2.0, -3.0], [1.0, 0.0, 1.0], [5.0, -1.0, -3.0]], order='C')
        dic = dictionary(dense, 0.0)
        dic.find_lambdalower_encol_entype()
        port = dic.Current_portfolio()
        weights = [port.Weights()]
        risks = [port.Risk()]
        rewards = [port.Reward()]
        omegas = [port.Omega()]
        sds = [port.Sd()]
        sharpes = [port.Sharpe()]
        lambda_l = [port.Lambda_lower()]
        lambda_u = [port.Lambda_upper()]
        while not dic.isentire():
            dic.find_lecol_then_pivot()
            dic.find_lambdalower_encol_entype()
            port = dic.Current_portfolio()
            weights.append(port.Weights())
            risks.append(port.Risk())
            rewards.append(port.Reward())
            omegas.append(port.Omega())
            sds.append(port.Sd())
            sharpes.append(port.Sharpe())
            lambda_l.append(port.Lambda_lower())
            lambda_u.append(port.Lambda_upper())

        for i in [0, 1, 2]:
            w1 = benchmark_weights[i]
            w2 = weights[i]
            self.assertEqual(len(w1), w2.size())
            for k, v in w1.items():
                self.assertAlmostEqual(w2[k], v, delta=1e-10)
            self.assertAlmostEqual(benchmark_risks[i], risks[i], delta=1e-10)
            self.assertAlmostEqual(benchmark_rewards[i], rewards[i], delta=1e-10)
            self.assertAlmostEqual(benchmark_omegas[i], omegas[i], delta=1e-10)
            self.assertAlmostEqual(benchmark_sds[i], sds[i], delta=1e-10)
            self.assertAlmostEqual(benchmark_sharpes[i], sharpes[i], delta=1e-10)
            self.assertAlmostEqual(benchmark_lbd_l[i], lambda_l[i], delta=1e-10)
            self.assertAlmostEqual(benchmark_lbd_u[i], lambda_u[i], delta=1e-10)
        return

    def test_simple_dictionary_operation_absolute_semi_deviation(self):
        benchmark_weights = [{0: 1.0}, {0: 0.0666666666666665, 1: 0.933333333333333}, {1: 1.0}]
        benchmark_risks = [2.77777777777778, 0.28888888888889, 0.22222222222222]
        benchmark_rewards = [1.66666666666667, 0.73333333333333, 0.66666666666667]
        benchmark_omegas = [1.6, 3.53846153846154, 4]
        benchmark_sds = [7.23417813807024, 0.866666666666666, 0.577350269189626]
        benchmark_sharpes = [0.230387838792046, 0.846153846153847, 1.15470053837925]
        benchmark_lbd_l = [2.66666666666667, 1, -0.666666666666667]
        benchmark_lbd_u = [inf, 2.66666666666667, 1]

        # initialize a dictionary from realizations, three assets, three realizations,
        # each row corresponds with one asset
        dense = np.array([[10.0, -2.0, -3.0], [1.0, 0.0, 1.0], [5.0, -1.0, -3.0]], order='C')
        dic = dictionary(dense)
        dic.find_lambdalower_encol_entype()
        port = dic.Current_portfolio()
        weights = [port.Weights()]
        risks = [port.Risk()]
        rewards = [port.Reward()]
        omegas = [port.Omega()]
        sds = [port.Sd()]
        sharpes = [port.Sharpe()]
        lambda_l = [port.Lambda_lower()]
        lambda_u = [port.Lambda_upper()]
        while not dic.isentire():
            dic.find_lecol_then_pivot()
            dic.find_lambdalower_encol_entype()
            port = dic.Current_portfolio()
            weights.append(port.Weights())
            risks.append(port.Risk())
            rewards.append(port.Reward())
            omegas.append(port.Omega())
            sds.append(port.Sd())
            sharpes.append(port.Sharpe())
            lambda_l.append(port.Lambda_lower())
            lambda_u.append(port.Lambda_upper())

        for i in [0, 1, 2]:
            w1 = benchmark_weights[i]
            w2 = weights[i]
            self.assertEqual(len(w1), w2.size())
            for k, v in w1.items():
                self.assertAlmostEqual(w2[k], v, delta=1e-10)
            self.assertAlmostEqual(benchmark_risks[i], risks[i], delta=1e-10)
            self.assertAlmostEqual(benchmark_rewards[i], rewards[i], delta=1e-10)
            self.assertAlmostEqual(benchmark_omegas[i], omegas[i], delta=1e-10)
            self.assertAlmostEqual(benchmark_sds[i], sds[i], delta=1e-10)
            self.assertAlmostEqual(benchmark_sharpes[i], sharpes[i], delta=1e-10)
            self.assertAlmostEqual(benchmark_lbd_l[i], lambda_l[i], delta=1e-10)
            self.assertAlmostEqual(benchmark_lbd_u[i], lambda_u[i], delta=1e-10)
        return

def suite():
    this_suite = unittest.TestSuite()
    this_suite.addTest(unittest.makeSuite(dictionary_tests))
    return this_suite

def run():
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())

if __name__ == '__main__':
    run()
