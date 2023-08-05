# -*- coding: utf-8 -*-
# -*- mode: python -*-
""" Generates equations.txt and parameters.txt for makecode (not implemented)"""
# python 3 compatibility
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import logging
from spyks.core import n_params, n_state, n_forcing
from spyks.codegen import simplify_equations

log = logging.getLogger('spyks')   # root logger


def discretize(model):
    pass
