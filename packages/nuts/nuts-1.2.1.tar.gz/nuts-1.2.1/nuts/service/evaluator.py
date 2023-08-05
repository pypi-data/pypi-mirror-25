from __future__ import absolute_import
from __future__ import unicode_literals

import logging

from colorama import Fore
from past.builtins import basestring

from nuts.data.evaluation import Evaluation
from nuts.data.evaluation_result import EvaluationResult


class Evaluator(object):
    def __init__(self, test_suite):
        self.test_suite = test_suite
        self.application_logger = logging.getLogger('nuts-application')
        self.test_report_logger = logging.getLogger('nuts-test-report')

    @staticmethod
    def _compare_type(expected, result):
        if isinstance(expected, basestring) and isinstance(result, basestring):
            return True

        if isinstance(expected, bool) and isinstance(result, bool):
            return True
        # bool is instance of int. return False if one type is a boolean
        elif isinstance(expected, bool) != isinstance(result, bool):
            return False

        if isinstance(expected, (int, float)) and isinstance(result, (int, float)):
            return True

        if isinstance(expected, list) and isinstance(result, list):
            return True

        if isinstance(expected, dict) and isinstance(result, dict):
            return True

        if isinstance(expected, tuple) and isinstance(result, type):
            return True

        return False

    def compare(self, test_case):
        evaluation = Evaluation(test_case.expected_result, test_case.operator)
        for minion in test_case.minions:
            evaluation.evaluation_results.append(self.compare_minion(test_case, minion))
        return evaluation

    def compare_minion(self, test_case, minion):
        actual_result = test_case.extract_actual_result()
        if minion in actual_result:
            if self._compare_type(test_case.expected_result, actual_result[minion]):
                if test_case.operator == '=':
                    compare = self.comp(test_case.expected_result, actual_result[minion])
                elif test_case.operator == '<':
                    compare = test_case.expected_result < actual_result[minion]
                elif test_case.operator == '>':
                    compare = test_case.expected_result > actual_result[minion]
                elif test_case.operator == 'not':
                    compare = test_case.expected_result != actual_result[minion]
            else:
                self.test_report_logger.warning('%s%s: Result type mismatch ---------%s', Fore.RED, test_case.name,
                                                Fore.RESET)
                compare = False
            result = actual_result[minion]
        else:
            compare = False
            result = None
        return EvaluationResult(minion, result, compare)

    def comp(self, list1, list2):
        if isinstance(list1, list) and isinstance(list1, list):
            return self.comp(set(list1), set(list2))
        else:
            return list1 == list2

    @staticmethod
    def format_result(result):
        if isinstance(result, basestring):
            return result.encode('utf-8')
        if isinstance(result, list):
            return [x.encode('utf-8') for x in result]
        if isinstance(result, dict):
            return {x.encode('utf-8'): y.encode('utf-8') for x, y in result.items()}
        return str(result)

    def _test_case_failed(self, test_case):
        # TODO Change because actual_result handling changed
        if not len(test_case.minions):
            self.test_report_logger.debug('%s%s: No devices responding --------%s', Fore.RED, test_case.name,
                                          Fore.RESET)
            return True
        return test_case.extract_actual_result() == 'ERROR'

    def validate_result(self, test_case):
        if self._test_case_failed(test_case):
            self.test_report_logger.warning('%s%s: Test error -------------------%s', Fore.RED, test_case.name,
                                            Fore.RESET)
            self.test_report_logger.warning('An error occurred while executing the test!')
            self.test_suite.mark_test_case_failed(test_case)
            return

        evaluation = self.compare(test_case)
        if evaluation.result():
            self.test_report_logger.info('%s%s: Test passed -------------------------\n%s', Fore.GREEN, test_case.name,
                                         Fore.RESET)
            self.test_report_logger.debug('Expected: %s %s Actual: %s', str(test_case.expected_result),
                                          test_case.operator,
                                          str(test_case.extract_actual_result()))
            self.test_suite.mark_test_case_passed(test_case)
        else:
            self.test_report_logger.warning('%s%s: Test failed -------------------\n%s', Fore.RED, test_case.name,
                                            Fore.RESET)
            self.test_report_logger.warning('Expected: %s\nOperator:%s\nActual:', str(evaluation.expected_result),
                                            evaluation.operator)
            for eval_result in evaluation.evaluation_results:
                color = Fore.GREEN if eval_result.passed else Fore.RED
                self.test_report_logger.warning(color + '%s: %s', eval_result.minion, eval_result.actual_result)
            self.test_report_logger.debug('Test: %s Expected: %s Operator: %s\nActual: %s', test_case.name,
                                          str(test_case.expected_result), test_case.operator,
                                          test_case.extract_actual_result())
            self.test_suite.mark_test_case_failed(test_case)

    def validate_all_results(self):
        for test in self.test_suite.test_cases_async + self.test_suite.test_cases_sync:
            self.validate_result(test)
        self.test_suite.print_statistics()
