# -*- coding: utf-8 -*-

from trytond.pool import Pool
from .memo import PimMemo
from .category import Category


def register():
    Pool.register(
        Category,
        PimMemo,
        module='pim_memos', type_='model')
