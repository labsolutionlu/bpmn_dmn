from abc import abstractmethod
from io import BytesIO
import logging
from xml.etree import ElementTree

from SpiffWorkflow import Task
from SpiffWorkflow.bpmn.parser.BpmnParser import BpmnParser, full_tag
from SpiffWorkflow.bpmn.serializer.BpmnSerializer import BpmnSerializer
from SpiffWorkflow.bpmn.serializer.Packager import Packager
from SpiffWorkflow.bpmn.specs import ExclusiveGateway
from SpiffWorkflow.bpmn.workflow import BpmnWorkflow

from bpmn_dmn.bpmn.camunda import CamundaExclusiveGatewayParser

class InMemoryPackager(Packager):
    """
    Creates spiff's wf packages on the fly.
    """

    @classmethod
    def package_in_memory(cls, workflow_name, workflow_files, editor):
        """
        Generates wf packages from workflow diagrams.
        """

        s = BytesIO()
        p = cls(s, workflow_name, meta_data=[], editor=editor)
        p.add_bpmn_files_by_glob(workflow_files)
        p.create_package()
        return s.getvalue()

class BPMNXMLWorkflowRunner:
    def __init__(self, path, workflowProcessID=None, debug=False, **kwargs):
        self.path = path
        self.debug = debug
        self.kwargs = kwargs

        ETRroot = ElementTree.parse(self.path).getroot() # definitions
        self.workflowProcessID = workflowProcessID or BPMNXMLWorkflowRunner.__getWorkflowProcessID(ETRroot)
        self.workflowEditor = BPMNXMLWorkflowRunner.__getWorkflowEditor(ETRroot)

        self.packager = InMemoryPackager
        if self.workflowEditor == 'Camunda Modeler':
            self.addParserSupport('exclusiveGateway', CamundaExclusiveGatewayParser, ExclusiveGateway.ExclusiveGateway)

        self.workflow = None

    def addParserSupport(self, full_tag_name, parserClass, taskClass):
        self.packager.PARSER_CLASS.OVERRIDE_PARSER_CLASSES[full_tag(full_tag_name)] = (parserClass, taskClass)

    @staticmethod
    def __getWorkflowProcessID(ETRroot):
        processElements = []
        for child in ETRroot:
            if child.tag.endswith('process') and child.attrib.get('isExecutable', False):
                processElements.append(child)

        if len(processElements) == 0:
            raise Exception('No executable process tag found')

        if len(processElements) > 1:
            raise Exception('Multiple executable processes tags found')

        return processElements[0].attrib['id']

    @staticmethod
    def __getWorkflowEditor(ETRroot):
        return ETRroot.attrib['exporter']

    def __do_engine_steps(self):
        assert not self.workflow.read_only
        engine_steps = list(
            [t for t in self.workflow.get_tasks(Task.READY) if self.workflow._is_engine_task(t.task_spec)])
        while engine_steps:
            for task in engine_steps:
                task.complete()

            engine_steps = list([t for t in self.workflow.get_tasks(Task.READY) if self.workflow._is_engine_task(t.task_spec)])

    def start(self, **data):
        package = self.packager.package_in_memory(self.workflowProcessID, self.path, self.workflowEditor)
        workflowSpec = BpmnSerializer().deserialize_workflow_spec(package)
        self.workflow = BpmnWorkflow(workflowSpec, **self.kwargs)
        self.workflow.debug = self.debug

        # Set input data to first ready task
        self.workflow.get_tasks(Task.READY)[0].set_data(**data)

        # self.workflow.do_engine_steps()

        self.__do_engine_steps()

    def getEndEventName(self):
        endTask = self.workflow.get_tasks()[-1]
        parent = endTask.parent

        while parent and parent.task_spec.name.endswith(('EndJoin', 'End')):
            parent = parent.parent

        if parent:
            return parent.task_spec.name

    def getData(self):
        return self.workflow.data
