import unittest

from decimal import Decimal

from bpmn_dmn.dmn import DMNDecisionRunner

class LongOrDoubleDecisionTestClass(unittest.TestCase):
    """
    Doc: https://docs.camunda.org/manual/7.7/user-guide/dmn-engine/
    """

    @classmethod
    def setUpClass(cls):
        cls.runner = DMNDecisionRunner('long_or_double_decision_comparison.dmn', debug='DEBUG')

    def test_long_or_double_decision_string_output1(self):
        res = self.runner.decide(Decimal('30.5'))
        self.assertEqual(res.description, '30.5 Row Annotation')

    def test_long_or_double_decision_string_output2(self):
        res = self.runner.decide(Decimal('25.3'))
        self.assertEqual(res.description, 'L Row Annotation')

    def test_long_or_double_decision_string_output3(self):
        res = self.runner.decide(Decimal('25.4'))
        self.assertEqual(res.description, 'H Row Annotation')
