import unittest

from SpiffWorkflow.bpmn.BpmnScriptEngine import BpmnScriptEngine

from bpmn_dmn.bpmn import BPMNXMLWorkflowRunner

class Lorder:
    def __init__(self, rptgrpcode, status, printedfl, testList, patientOrder):
        self.rptgrpcode = rptgrpcode
        self.status = status
        self.printedfl = printedfl
        self.testList = testList
        self.patientOrder = patientOrder

class LXScriptEngine(BpmnScriptEngine):
    @staticmethod
    def lxs(fctName, lorder):
        print('lxs', fctName, lorder)

        if fctName == 'checkPatientOrder':
            return lorder.patientOrder
        else:
            raise NotImplementedError(fctName)

    def _eval(self, task, expression, **kwargs):
        locals().update(kwargs)
        locals().update({'lxs': LXScriptEngine.lxs})
        return eval(expression)

class LXS_BPMNXMLWorkflowRunner(BPMNXMLWorkflowRunner):
    def __init__(self, *args, **kwargs):
        super(LXS_BPMNXMLWorkflowRunner, self).__init__(*args, **kwargs, script_engine=LXScriptEngine())

class ExclusiveGatewayTestClass(unittest.TestCase):
    """
    Doc: https://docs.camunda.org/manual/7.4/reference/bpmn20/gateways/exclusive-gateway/
    """

    def test_exclusive_gateway_if_else(self):
        runner = BPMNXMLWorkflowRunner('exclusive_gateway_if_else.bpmn', debugLog='DEBUG', debug=True)
        runner.start(x=1)
        res = runner.getEndEventName()
        self.assertEqual(res, 'EndEvent_0ofyivj')

    def test_exclusive_gateway_two_if_else(self):
        class Lorder:
            def __init__(self, status, printedfl):
                self.status = status
                self.printedfl = printedfl

        runner = BPMNXMLWorkflowRunner('exclusive_gateway_two_if_else.bpmn', debugLog='DEBUG', debug=True)
        runner.start(lorder=Lorder(2, True))
        res = runner.getEndEventName()
        self.assertEqual(res, 'EndEvent_01jecqa')

    def test_exclusive_gateway_complex(self):
        runner = LXS_BPMNXMLWorkflowRunner('exclusive_gateway_complex.bpmn', debugLog='DEBUG', debug=True)

        runner.start(lorder=Lorder('A', 2, True, ['NA', 'BTN'], False))
        res = runner.getEndEventName()
        self.assertEqual(res, 'EndEvent_14qisp7')

        runner.start(lorder=Lorder('A', 2, True, ['NA', 'BS'], True))
        res = runner.getEndEventName()
        self.assertEqual(res, 'EndEvent_0tq881i')

        runner.start(lorder=Lorder('A', 2, True, ['NA', 'BS'], False))
        res = runner.getEndEventName()
        self.assertEqual(res, 'EndEvent_1kj5qm0')
