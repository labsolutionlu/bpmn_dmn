from SpiffWorkflow.bpmn.parser.TaskParser import TaskParser
from SpiffWorkflow.bpmn.specs.BpmnSpecMixin import BpmnSpecMixin
from SpiffWorkflow.specs.Simple import Simple

from bpmn_dmn.dmn import DMNDecisionRunner
from bpmn_dmn.bpmn import BPMNXMLWorkflowRunner

class _BusinessRuleTask(Simple, BpmnSpecMixin):
    """
    Task Spec for a bpmn:businessTask (DMB Decision Reference) node.
    """

    def __init__(self, wf_spec, name, **kwargs):
        super().__init__(wf_spec, name, **kwargs)

        self.decisionRunner = None
        self.res = None
        self.resDict = None

    def _on_complete_hook(self, my_task):
        super(_BusinessRuleTask, self)._on_complete_hook(my_task)

        self.res = self.decisionRunner.decide(**my_task.data)
        self.resDict = self.res.outputAsDict()
        my_task.data.update(self.resDict)
        my_task.workflow.data.update(self.resDict)

class _BusinessRuleTaskParser(TaskParser):
    dmn_debug=None

    def __init__(self, process_parser, spec_class, node):
        super(_BusinessRuleTaskParser, self).__init__(process_parser, spec_class, node)
        self.decisionRef = None
        self.dmnParser = None

    def parse_node(self):
        task = super(_BusinessRuleTaskParser, self).parse_node()
        for attrib in self.node.attrib:
            if attrib.endswith('decisionRef'):
                self.setTaskDecision(task, self.node.attrib[attrib])
                break

        return task

    def setTaskDecision(self, task, decisionRef):
        if '.' not in decisionRef:
            decisionRef += '.dmn'

        self.decisionRef = decisionRef
        task.decisionRunner = DMNDecisionRunner(self.decisionRef, debug=_BusinessRuleTaskParser.dmn_debug)

class BPMNDMNXMLWorkflowRunner(BPMNXMLWorkflowRunner):
    def __init__(self, *args, dmn_debug=None, **kwargs):
        super(BPMNDMNXMLWorkflowRunner, self).__init__(*args, **kwargs)

        # Add business rule task support to execute decision tables
        _BusinessRuleTaskParser.dmn_debug = dmn_debug
        self.addParserSupport('businessRuleTask', _BusinessRuleTaskParser, _BusinessRuleTask)
