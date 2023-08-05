"""This module provides basic functionality to construct an efficient frontier

classes: RiskMeasure, SimpleEF
"""
from __future__ import print_function

import numpy as np
from pymcef import ppslp

__all__ = ['SimpleEF', 'RiskMeasure']

def _get_portfolio(port):
    prt = {}
    prt['weight'] = port.Weights().asdict()
    prt['risk'] = port.Risk()
    prt['reward'] = port.Reward()
    prt['Omega'] = port.Omega()
    prt['sd'] = port.Sd()
    prt['Sharpe'] = port.Sharpe()
    prt['lambda_l'] = port.Lambda_lower()
    prt['lambda_u'] = port.Lambda_upper()
    return prt

def _check_kwargs(kwargs, supported):
    for arg_name in kwargs.keys():
        if arg_name not in supported:
            raise TypeError(arg_name+" is a invalid keyword argument for this function")

class RiskMeasure:
    """Risk measures for efficient frontier construction

    The user specify one of the two supported risk measures to construct efficient frontier:
    RiskMeasure.AbsoluteSemiDeviation or RiskMeasure.FixTargetUnderPerformance
    This is an optional input for constructor of SimpleEF or SimpleEFp.
    """
    AbsoluteSemiDeviation, FixTargetUnderPerformance = range(2)

class SimpleEF:
    """Simple efficient frontier without matplotlib dependency

    Construct an efficient frontier at once with Monte Carlo simulated returns.
    Simple means: there is no support for intermediate result saving and restarting from
    partially constructed efficient frontier.
    Suitable for small scale problem, with the product of number of assets(positions)
    and number of simulated realizations less than 10 million, in which case
    full efficient frontier can be constructed in minutes.

    Data obtained by this class:
    SimpleEF.frontier_in_sample: all the portfolios efficient with respect to the training set
    SimpleEF.frontier_validation: statistics of the portfolios in frontier_in_sample calculated
                                  using validation set.
    All the above two class attributes are a list of dictionaries for each portfolio.

    dictionaries of SimpleEF.frontier_in_sample has the following fields:
    'weight': a dictionary with assert index as key, and the fraction as value, summing to 1.0
    'lambda_l': the lower bound of the risk factor to make this portfolio efficient with respect
                to the training set.
    'lambda_u': the upper bound of the risk factor to make this portfolio efficient with respect
                to the training set.

    The two fields 'lambda_l' and 'lambda_u' can fully specify the linear programming problem to
    obtain the efficient portfolio. The user can use them to validate the result using third party
    linear programming software: the same weights should be produced.

    With the field 'weight', the user of this class can obtain the following fields by
    themselves. Possibly with different numbers, using their own definitions.
    'risk': the risk, either using risk measure RiskMeasure.AbsoluteSemiDeviation or
            RiskMeasure.FixTargetUnderPerformance.
    'reward': the mean return of the portfolio in the training set.
    'Omega': the mean return above the target over the mean return below the target, the target
             depends on the risk measure.
    'sd': the standard deviation of the returns in the training set.
    'Sharpe': in sample Sharpe ratio, return divided by standard deviation. Notice, the riskless
              return is not subtracted from the return.

    dictionaries of SimpleEF.frontier_validation compute the following fields using the same
    formula but different data, the validation set: 'returns', 'reward', 'sd', 'Sharpe'.
    """
    def __init__(self, **kwargs):
        """Construct an efficient frontier with return realizations.
        Input arguments(all keyword argument):
        training_set(numpy 2D array): required, realizations of returns for EF construction,
                                      relative/percentage
        validation_set(numpy 2D array): optional, realizations of returns for validation, used
                                        to calculate out-of-sample Sharpe Ratio, Conditional
                                        VAR etc.
        ************************************ IMPORTANT ************************************
        The data of the above two numpy 2D arrays must be in correct dimension order:
        Each row corresponds with all the realized returns of one asset/position
        If you are using a dataframe, most likely each asset corresponds with one column
        In this case, please use numpy.transpose before using this class.
        In the C++ library where the optimization is actually implemented, the data is
        stores contiguously in this way, all returns of asset 1, and then 2, etc.
        This is the best choice for this specific linear programming program.
        ************************************ IMPORTANT ************************************
        risk_measure: optional, one of the two risk measures:
                      RiskMeasure.AbsoluteSemiDeviation or RiskMeasure.FixTargetUnderPerformance.
                      If not provided, RiskMeasure.AbsoluteSemiDeviation will be used.
                      In order to use this parameter, import it first:
                      from pymcef.simple import RiskMeasure
        target_return: optional, if RiskMeasure.FixTargetUnderPerformance is the risk measure
                       use this to specify the fixed target return, usually riskless return.
                       If not given, 0.0 is used.
        asset_names: optional, the string names of all the assets(positions), if not given
                     array index will be used as labels.
        """
        kws = ['training_set', 'validation_set', 'risk_measure', 'target_return', 'asset_names']
        _check_kwargs(kwargs, kws)
        if 'training_set' not in kwargs:
            raise TypeError("required keyword argument training_set missing")
        self.training_set = kwargs['training_set']
        if 'asset_names' in kwargs:
            self.asset_names = kwargs['asset_names']
        else:
            self.asset_names = ['asset '+str(i) for i in range(self.training_set.shape[0])]
        if len(self.asset_names) != self.training_set.shape[0]:
            raise ValueError("Dimension of input arguments mismatch")
        self.risk_measure = kwargs.get('risk_measure', RiskMeasure.AbsoluteSemiDeviation)
        self.ef_lbd_lower = 1.0 if self.risk_measure == RiskMeasure.AbsoluteSemiDeviation else 0.0
        self.target = kwargs.get('target_return', 0.0)
        if self.risk_measure == RiskMeasure.AbsoluteSemiDeviation:
            self.dic = ppslp.dictionary(self.training_set)
        elif self.risk_measure == RiskMeasure.FixTargetUnderPerformance:
            self.dic = ppslp.dictionary(self.training_set, self.target)
        else:
            raise ValueError("Unsupported Risk Measure enum value:" + str(self.risk_measure))
        self.dic.find_lambdalower_encol_entype()
        self.frontier_in_sample = []
        self.frontier_in_sample.append(_get_portfolio(self.dic.Current_portfolio()))
        while not self.dic.isentire():
            self.dic.find_lecol_then_pivot()
            self.dic.find_lambdalower_encol_entype()
            self.frontier_in_sample.append(_get_portfolio(self.dic.Current_portfolio()))
        if self.frontier_in_sample[-1]['lambda_l'] < self.ef_lbd_lower:
            self.frontier_in_sample[-1]['lambda_l'] = self.ef_lbd_lower
        max_sharpe_port_index = self.dic.Max_sharpe_index()
        max_omega_port_index = self.dic.Max_omega_index()
        max_sharpe_port = _get_portfolio(self.dic.Max_sharpe_portfolio())
        max_omega_port = _get_portfolio(self.dic.Max_omega_portfolio())
        self.critical_port_in_sample = {}
        self.critical_port_in_sample['Max Sharpe'] = {'Index' : max_sharpe_port_index,
                                                      'Portfolio' : max_sharpe_port}
        self.critical_port_in_sample['Max Omega'] = {'Index' : max_omega_port_index,
                                                     'Portfolio' : max_omega_port}
        #print("Sample efficient frontier contains " + \
        #      str(len(self.frontier_in_sample)) + " portfolios")
        #print("Max Sharpe portfolio is the " + str(max_sharpe_port_index) + "th")
        #print("Max Omega portfolio is the " + str(max_sharpe_omega_index) + "th")
        if 'validation_set' in kwargs:
            self.validation_set = kwargs['validation_set']
            if self.validation_set.shape[0] != self.training_set.shape[0]:
                raise ValueError("training set and validation set have different number of assets")
            self.frontier_validation = []
            max_sharpe_index, max_sharpe = 0, 0.0
            counter = 0
            for port in self.frontier_in_sample:
                rewards = np.zeros(self.validation_set.shape[1])
                port_validation = {}
                for index, weight in port['weight'].items():
                    rewards += weight * self.validation_set[index]
                reward = np.mean(rewards)
                port_validation['returns'] = rewards
                port_validation['reward'] = reward
                port_validation['sd'] = np.std(rewards)
                port_validation['Sharpe'] = port_validation['reward'] / port_validation['sd']
                if port_validation['Sharpe'] > max_sharpe:
                    max_sharpe = port_validation['Sharpe']
                    max_sharpe_index = counter
                # out of sample absolute semi-deviation as risk
                port_validation['risk'] = np.sum(rewards[rewards > reward] - reward) / len(rewards)
                self.frontier_validation.append(port_validation)
                counter += 1
            self.critical_port_validation = {}
            self.critical_port_validation['Max Sharpe'] = \
              {'Index' : max_sharpe_index, 'Portfolio' : self.frontier_validation[max_sharpe_index]}
        else:
            self.validation_set = None
            self.frontier_validation = None
            self.critical_port_validation = None
