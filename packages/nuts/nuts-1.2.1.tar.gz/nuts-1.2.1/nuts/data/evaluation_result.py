from __future__ import absolute_import
from __future__ import unicode_literals


class EvaluationResult(object):
    def __init__(self, minion, actual_result, passed):
        self.minion = minion
        self.actual_result = actual_result
        self.passed = passed
