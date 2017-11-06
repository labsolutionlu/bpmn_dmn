import unittest

from bpmn_dmn.dmn import DMNDecisionRunner

class StringDecisionTestClass(unittest.TestCase):
    """
    Doc: https://docs.camunda.org/manual/7.7/user-guide/dmn-engine/
    """

    @classmethod
    def setUpClass(cls):
        cls.runner = DMNDecisionRunner('string_decision.dmn', debug='DEBUG')

    def test_string_decision_string_output1(self):
        res = self.runner.decide('m')
        self.assertEqual(res.description, 'm Row Annotation')

    def test_string_decision_string_output2(self):
        res = self.runner.decide('f')
        self.assertEqual(res.description, 'f Row Annotation')

    def test_string_decision_string_output3(self):
        res = self.runner.decide('y')
        self.assertEqual(res.description, 'NOT x Row Annotation')

    def test_string_decision_string_output4(self):
        res = self.runner.decide('x')
        self.assertEqual(res.description, 'ELSE Row Annotation')
