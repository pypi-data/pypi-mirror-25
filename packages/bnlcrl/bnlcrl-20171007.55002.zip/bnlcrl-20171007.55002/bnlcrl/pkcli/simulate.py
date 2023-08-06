# -*- coding: utf-8 -*-
u"""Utilities for X-Ray beamlines.

The module to perform the following operations:

- simulate Compound Refractive Lenses (``CRL``) in the approximation of thick lens;
- get the Index of Refraction (``Delta``) value;
- calculate ideal focal distance.
"""
import argh

from bnlcrl.crl_simulator import CRLSimulator, DEFAULTS_FILE as DEFAULTS_FILE_CRL
from bnlcrl.delta_finder import DeltaFinder, DEFAULTS_FILE as DEFAULTS_FILE_DELTA

from bnlcrl.utils import get_cli_functions, read_json

# CRL:
config_crl = read_json(DEFAULTS_FILE_CRL)
functions_list = get_cli_functions(config_crl)
for content in functions_list:
    exec(content)

# Delta and focus:
config_delta = read_json(DEFAULTS_FILE_DELTA)
functions_list = get_cli_functions(config_delta)
for content in functions_list:
    exec(content)
