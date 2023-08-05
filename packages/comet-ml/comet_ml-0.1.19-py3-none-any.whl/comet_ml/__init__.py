"""comet - An opinionated, minimal cookiecutter template for Python packages"""

import config
import sklearn_logger
from .comet import Experiment

__version__ = '0.1.0'
__author__ = 'Gideon <Gideon@semantica-labs.com>'
__all__ = ['Experiment']
