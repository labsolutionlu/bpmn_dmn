import unittest

from bpmn_dmn.dmn import DMNDecisionRunner

class StringIntegerDecisionTestClass(unittest.TestCase):
    """
    Doc: https://docs.camunda.org/manual/7.7/user-guide/dmn-engine/
    """

    @classmethod
    def setUpClass(cls):
        cls.runner = DMNDecisionRunner('string_integer_decision.dmn', debug='DEBUG')

    def test_string_integer_decision_string_output1(self):
        res = self.runner.decide('m', 30)
        self.assertEqual(res.description, 'm30 Row Annotation')

    def test_string_integer_decision_string_output2(self):
        res = self.runner.decide('m', 24)
        self.assertEqual(res.description, 'mL Row Annotation')

    def test_string_integer_decision_string_output3(self):
        res = self.runner.decide('m', 25)
        self.assertEqual(res.description, 'mH Row Annotation')

    def test_string_integer_decision_string_output4(self):
        res = self.runner.decide('f', -1)
        self.assertEqual(res.description, 'fL Row Annotation')

    def test_string_integer_decision_string_output5(self):
        res = self.runner.decide('x', 0)
        self.assertEqual(res.description, 'ELSE Row Annotation')
