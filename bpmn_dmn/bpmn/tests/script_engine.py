import unittest

from SpiffWorkflow.bpmn.BpmnScriptEngine import BpmnScriptEngine

from bpmn_dmn.bpmn import BPMNXMLWorkflowRunner

class LXScriptEngine(BpmnScriptEngine):
    @staticmethod
    def lxs(arg):
        print('lxs', arg)
        return arg == 'y'

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

    @classmethod
    def setUpClass(cls):
        cls.runner = LXS_BPMNXMLWorkflowRunner('script_engine.bpmn', debug=True)

    def test_script_engine(self):
        self.runner.start(x='y')
        res = self.runner.getEndEventName()
        self.assertEqual(res, 'EndEvent_0tq881i')

    def test_script_engine_else(self):
        self.runner.start(x='z')
        res = self.runner.getEndEventName()
        self.assertEqual(res, 'EndEvent_1kj5qm0')
