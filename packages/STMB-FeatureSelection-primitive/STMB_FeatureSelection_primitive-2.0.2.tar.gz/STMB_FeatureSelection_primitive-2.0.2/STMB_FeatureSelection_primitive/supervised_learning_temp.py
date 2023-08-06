# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import abc
from typing import *
from .base import *
__all__ = (u'SupervisedLearnerPrimitiveBase',)


class SupervisedLearnerPrimitiveBase(PrimitiveBase[(Input, Output, Params)]):
    u'\n    A base class for primitives which have to be fitted on both input and output data\n    before they can start producing (useful) outputs from inputs.\n    '

    @abc.abstractmethod
    def set_training_data(self, inputs, outputs):
        u'\n        Sets training data of this primitive.\n\n        Parameters\n        ----------\n        inputs : Sequence[Input]\n            The inputs.\n        outputs : Sequence[Output]\n            The outputs.\n        '
