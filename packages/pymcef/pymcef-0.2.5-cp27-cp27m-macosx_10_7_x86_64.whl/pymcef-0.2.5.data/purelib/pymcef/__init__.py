"""This package support the construction of efficient frontier from MC simulated returns

classes: RiskMeasure, SimpleEF, SimpleEFp
    SimpleEF: efficient frontier construction, depends on numpy
    SimpleEFp: efficient frontier construction with visualization, depends on numpy and matplotlib
"""
from pymcef.simple import SimpleEF, RiskMeasure
from pymcef.simple_plot import SimpleEFp
