# BPMN DMN (bpmn_dmn)

A library to execute BPMN Workflows and DMN Decision Tables

## Introduction

This package uses SpiffWorkflow to execute the DBPM workflow. I wrote my own DMN engine to execute DMN Decision Tables.
I used the Camunda Modeleler to create all my files.

The bpmn_dmn package contains 3 main modules:

- bpmn to execute BPMN Workflow Charts by using an xml file on the disc
![Alt text](bpmn.jpg?raw=true "BPMN")

- dmn to execute DMN Decision Tables by using an xml file on the disc
![Alt text](dmn.jpg?raw=true "DMN")

- bpmn_dmn to execute BPMN Workflow Charts that includes DMN Decision Tables as business tasks
![Alt text](bpmn_dmn.jpg?raw=true "BPMN_DMN")

## Doc and Modeler

* [Camunda BPMN Doc](https://docs.camunda.org/manual/7.7/)
* [Camunda DMN Doc](https://docs.camunda.org/manual/7.5/reference/dmn11/decision-table/)
* [Camunda Modeler](https://camunda.org/download/modeler/)

## Usage

### Execute bpmn Workflow Charts (See bpmn/tests):

Use the BPMNXMLWorkflowRunner class to execute xml files

```path, workflowProcessID=None, debugLog='INFO', debug=False, **kwargs```

#### Basic Example:

```
from bpmn_dmn.bpmn import BPMNXMLWorkflowRunner

class Lorder:
    def __init__(self, status, printedfl):
        self.status = status
        self.printedfl = printedfl

runner = BPMNXMLWorkflowRunner('exclusive_gateway_two_if_else.bpmn', debugLog='DEBUG', debug=True)
runner.start(lorder=Lorder(2, True))
res = runner.getEndEventName()
print(res)
```

### Execute bpmn Workflow Charts that includes DMN Decision Tables (See bpmn_dmn/tests):

Use the BPMNDMNXMLWorkflowRunner class to execute xml files

```path, workflowProcessID=None, debugLog='INFO', debug=False, **kwargs```

#### Basic Example:

```
from bpmn_dmn.bpmn_dmn import BPMNDMNXMLWorkflowRunner

runner = BPMNDMNXMLWorkflowRunner('ExclusiveGatewayIfElseAndDecision.bpmn', debugLog='DEBUG', debug=True)
runner.start(x=3)

res = runner.getEndEventName()
print(res)
```

#### Use my own script engine:

```
from bpmn_dmn.bpmn import BPMNXMLWorkflowRunner

from SpiffWorkflow.bpmn.BpmnScriptEngine import BpmnScriptEngine

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

class Lorder:
    def __init__(self, status, printedfl):
        self.status = status
        self.printedfl = printedfl

runner = LXS_BPMNXMLWorkflowRunner('exclusive_gateway_two_if_else.bpmn', debugLog='DEBUG', debug=True)
runner.start(lorder=Lorder(2, True))
res = runner.getEndEventName()
print(res)
```

### Execute dmn Decision Tables (See dmn/tests):

Use the DMNDecisionRunner class to execute xml files

```path, debug='INFO'```

#### Basic Example:

```
from bpmn_dmn.dmn import DMNDecisionRunner

runner = DMNDecisionRunner('string_integer_decision.dmn', debug='DEBUG')
res = self.runner.decide('m', 30)
print(res)
```

## Authors

* **Denny Weinberg** - *Initial work* - [DennyWeinberg](https://github.com/DennyWeinberg)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## TODOs

* Log improvements
* Test other unit tests from SpiffWorkflow [Source](https://github.com/knipknap/SpiffWorkflow/tree/master/tests/SpiffWorkflow/bpmn)
