"""This module provides basic functionality to construct an efficient frontier and visualize it

classes: SimpleEFp
"""
from copy import deepcopy
from operator import itemgetter
try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import cm

from pymcef.simple import SimpleEF, RiskMeasure, _check_kwargs

__all__ = ['SimpleEFp']
plot_font = 'Arial'

def _compute_cvar(port, cvar_q, cvar_target):
    returns = port['returns']
    quantile = np.percentile(returns, cvar_q*100)
    cvar = np.mean(cvar_target - returns[returns < quantile])
    return cvar

class SimpleEFp(SimpleEF):
    """Simple efficient frontier and plot, with matplotlib dependency

    Construct an efficient frontier at once with Monte Carlo simulated returns.
    Simple means: there is no support for intermediate result saving and restarting from
    partially constructed efficient frontier.
    Suitable for small scale problem, with the product of number of assets(positions)
    and number of simulated realizations less than 10 million, in which case
    full efficient frontier can be constructed in minutes.

    The only difference between this class and its parent SimpleEF is that this class has
    a few additional methods to visualize the efficient frontier obtained.
    You will need to correctly set up the matplotlib backend to use this class, usually the
    default setting is good enough. However on linux, please modify your matplotlibrc to
    use TkAgg backend.

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
        SimpleEF.__init__(self, **kwargs)

    def _get_axis_label_for_risk(self):
        if self.risk_measure == RiskMeasure.AbsoluteSemiDeviation:
            xlabel = 'In Sample Risk (absolute semi-deviation)'
        elif self.risk_measure == RiskMeasure.FixTargetUnderPerformance:
            xlabel = 'In Sample Risk (expected under-performance to target '+str(self.target)+')'
        else:
            raise ValueError("Unsupported Risk Measure enum value:" + str(self.risk_measure))
        return xlabel

    def plot_ef(self, **kwargs):
        """Plot the constructed efficient frontier

        Input arguments(all keyword argument):
        CVar_q: optional, default 0.05. The lower quantile for Conditional Var
        CVar_t: optional, default 0.0. The target of CVar, for instance the expected return
        conditional on being less than 0.05 quantile is -0.03, and the target is 0.0, then the
        CVar is 0.0 - (-0.03) = 0.03.
        """
        tag = '-'
        n = len(self.frontier_in_sample)
        xs = [self.frontier_in_sample[i]['risk'] for i in range(n)]
        ys = [self.frontier_in_sample[i]['reward'] for i in range(n)]
        port = self.critical_port_in_sample['Max Sharpe']['Portfolio']
        x = port['risk']
        y = port['reward']
        num_subplots = 1 if self.frontier_validation is None else 2
        fig = plt.figure(figsize=(6 * num_subplots, 4.5))
        ax = fig.add_subplot(1, num_subplots, 1)
        ax.plot(xs, ys, tag)
        ax.plot(x, y, 'r.')
        ax.text(x * 1.05, y, 'Max Sharpe ratio portfolio', fontsize=8)
        xlabel = self._get_axis_label_for_risk()
        ax.set_xlabel(xlabel, fontname=plot_font)
        ax.set_ylabel('Reward(Mean return)', fontname=plot_font)
        ax.set_title('In sample efficient frontier', fontname=plot_font)
        if num_subplots == 2:
            _check_kwargs(kwargs, ['CVar_q', 'CVar_t'])
            cvar_q = kwargs.get('CVar_q', 0.05)
            cvar_t = kwargs.get('CVar_t', 0.0)
            xs = []
            for port in self.frontier_validation:
                xs.append(_compute_cvar(port, cvar_q, cvar_t))
            ys = [self.frontier_validation[i]['reward'] for i in range(n)]
            port = self.critical_port_validation['Max Sharpe']['Portfolio']
            x = _compute_cvar(port, cvar_q, self.target)
            y = port['reward']
            ax = fig.add_subplot(1, num_subplots, 2)
            ax.plot(xs, ys, tag)
            ax.plot(x, y, 'r.')
            ax.text(x * 1.05, y, 'Max Sharpe ratio portfolio', fontsize=8)
            ax.set_xlabel('CVar('+str(cvar_q)+')', fontname=plot_font)
            ax.set_ylabel('Reward(Mean return)', fontname=plot_font)
            ax.set_title('Validation efficient frontier', fontname=plot_font)
        return fig

    def plot_performance(self, **kwargs):
        """Plot the performance indicators for all the efficient portfolios

        Input arguments(all keyword argument):
        CVar_q: optional, default 0.05. The lower quantile for Conditional Var
        CVar_t: optional, default 0.0. The target of CVar, for instance the expected return
        conditional on being less than 0.05 quantile is -0.03, and the target is 0.0, then the
        CVar is 0.0 - (-0.03) = 0.03.

        Performance indicators are: Sharpe Ratio, Return over CVar
        """
        tag = '-'
        n = len(self.frontier_in_sample)
        xs = [self.frontier_in_sample[i]['lambda_l'] for i in range(n)]
        ys = [self.frontier_in_sample[i]['Sharpe'] for i in range(n)]
        num_subplots = 1 if self.frontier_validation is None else 2
        fig = plt.figure(figsize=(6*num_subplots, 4.5))
        ax = fig.add_subplot(1, num_subplots, 1)
        ax.plot(xs, ys, tag, label='In sample')
        if self.frontier_validation is not None:
            ys = [self.frontier_validation[i]['Sharpe'] for i in range(n)]
            ax.plot(xs, ys, tag, label='Validation')
        ax.set_xlabel('$\\lambda$', fontname=plot_font)
        ax.set_ylabel('Sharpe Ratio', fontname=plot_font)
        ax.legend(fontsize=10, handlelength=5, frameon=False)
        if self.frontier_validation is not None:
            ax = fig.add_subplot(1, num_subplots, 2)
            _check_kwargs(kwargs, ['CVar_q', 'CVar_t'])
            cvar_q = kwargs.get('CVar_q', 0.05)
            cvar_t = kwargs.get('CVar_t', 0.0)
            ys = []
            for port in self.frontier_validation:
                ys.append(port['reward']/_compute_cvar(port, cvar_q, cvar_t))
            ax.plot(xs, ys, tag)
            ax.set_xlabel('$\\lambda$', fontname=plot_font)
            ax.set_ylabel('Reward / Validation CVar('+str(cvar_q)+')', fontname=plot_font)
            ax.set_title('Performance in validation portfolios', fontsize=10)
        return fig

    def plot_weights(self, max_num_assets=20):
        """Plot the weights of portfolio components for the entire frontier
        Positional arguments:
        max_num_assets: optional, default 20, the maximum number of assets/positions to plot
        """
        tag = '-'
        max_labels = 5
        cmap = cm.get_cmap('jet')
        fig = plt.figure(figsize=(6, 4.5))
        ax = fig.add_subplot(1, 1, 1)
        num_assets = 0
        weights_risk = Q.Queue(maxsize=len(self.frontier_in_sample))
        xs1 = []
        ys1 = []
        for port in self.frontier_in_sample:
            weights_risk.put((deepcopy(port['weight']), port['risk']))
            xs1.append(port['risk'])
            ys1.append(port['lambda_l'])
        while num_assets < max_num_assets and (not weights_risk.empty()):
            weights, risk = weights_risk.get()
            for k, v in sorted(weights.items(), key=itemgetter(1), reverse=True):
                ws = [v]
                rs = [risk]
                m = weights_risk.qsize() # single thread here, qsize is exact size
                for i in range(m): # pylint: disable=W0612
                    w, r = weights_risk.get()
                    rs.append(r)
                    if k in w:
                        ws.append(w[k])
                        del w[k]
                    else:
                        ws.append(0.0)
                    if len(w) > 0:
                        weights_risk.put((w, r))
                color = cmap(num_assets*1.0/max_num_assets)
                num_assets += 1
                ax.plot(rs, ws, tag, c=color)
                if num_assets <= max_labels:
                    ax.text(rs[0]*0.95, ws[0]+0.02, self.asset_names[k],\
                            fontsize=6, horizontalalignment='right', color=color)
        port = self.critical_port_in_sample['Max Sharpe']['Portfolio']
        ax.axvline(x=port['risk'], ls='dotted', c='black')
        ax.text(port['risk'], 1.02, 'Max Sharpe ratio portfolio', fontsize=6)
        #ys = list(port['weight'].values())
        #xs = [port['risk']] * len(ys)
        #ax.plot(xs, ys, '.k')
        xlabel = self._get_axis_label_for_risk()
        ax.set_xlabel(xlabel, fontname=plot_font)
        ax.set_ylabel('Weights', fontname=plot_font)
        ax1 = ax.twinx()
        ax1.plot(xs1, ys1, '--k', label='$\\lambda$', dashes=(12, 3))
        ax1.set_ylabel('$\\lambda$', fontname=plot_font)
        ax1.set_xlim(right=max(xs1))
        ax1.legend(loc='upper center', fontsize=10, handlelength=5, frameon=False)
        return fig

