#!/usr/bin/env python
# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# @Author: oesteban - code@oscaresteban.es
# @Date:   2014-06-03 11:49:42
# @Last Modified by:   oesteban
# @Last Modified time: 2017-10-13 14:55:28
"""Complementary data necessary in workflows

.. module:: regseg.data
   :synopsis: data required by :py:mod:`regseg`

.. moduleauthor:: Oscar Esteban <code@oscaresteban>

"""
from __future__ import print_function, division, absolute_import, unicode_literals

import os.path as op

data_path = op.abspath(op.dirname(op.realpath(__file__)))

p_paths = dict()
folders = dict()

for key in ['x', 'y', 'z']:
    p_paths[key] = op.join(data_path, 't2b_elastix_%s.txt' % key)

folders['t2b_params'] = p_paths
folders['regseg_hcp'] = op.join(data_path, 'regseg_hcp.json')
folders['regseg_default'] = op.join(data_path, 'regseg_default.json')
folders['model_labels'] = op.join(data_path, 'model_labels.json')


def get(value):
    if value not in folders:
        raise RuntimeError('Requested data resource does not exist')
    else:
        return folders[value]
