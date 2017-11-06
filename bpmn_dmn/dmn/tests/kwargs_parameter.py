import unittest

from bpmn_dmn.dmn import DMNDecisionRunner

class StringDecisionTestClass(unittest.TestCase):
    """
    Doc: https://docs.camunda.org/manual/7.7/user-guide/dmn-engine/
    """

    @classmethod
    def setUpClass(cls):
        cls.runner = DMNDecisionRunner('kwargs_parameter.dmn', debug='DEBUG')

    def test_string_decision_string_output1(self):
        res = self.runner.decide(Gender='m')
        self.assertEqual(res.description, 'm Row Annotation')
