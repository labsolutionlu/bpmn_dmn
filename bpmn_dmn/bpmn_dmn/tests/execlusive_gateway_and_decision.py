import unittest

from bpmn_dmn.bpmn_dmn import BPMNDMNXMLWorkflowRunner

class ExclusiveGatewayTestClass(unittest.TestCase):
    """
    Doc: https://docs.camunda.org/manual/7.4/reference/bpmn20/gateways/exclusive-gateway/ + https://docs.camunda.org/manual/7.7/user-guide/dmn-engine/
    """

    def test_exclusive_gateway_two_if_else_and_decision(self):
        runner = BPMNDMNXMLWorkflowRunner('ExclusiveGatewayIfElseAndDecision.bpmn', debug=True, dmn_debug='INFO')
        runner.start(x=3)

        res = runner.getEndEventName()
        self.assertEqual(res, 'EndEvent_0n32cxd')

        data = runner.getData()
        self.assertDictEqual(data, {'x': 3, 'y': 'A'})
