from SpiffWorkflow.bpmn.parser.ValidationException import ValidationException
from SpiffWorkflow.bpmn.parser.task_parsers import ExclusiveGatewayParser, first, xpath_eval

class CamundaExclusiveGatewayParser(ExclusiveGatewayParser):
    def connect_outgoing(self, outgoing_task, outgoing_task_node, sequence_flow_node, is_default):
        try:
            super(CamundaExclusiveGatewayParser, self).connect_outgoing(outgoing_task, outgoing_task_node, sequence_flow_node, is_default)
        except ValidationException as ex:
            if 'Non-default exclusive outgoing sequence flow without condition' not in str(ex):
                raise

            xpath = xpath_eval(sequence_flow_node)
            condition_expression_node = conditionExpression = first(
                xpath('.//bpmn:conditionExpression'))

            #if conditionExpression is not None:
            #    conditionExpression = conditionExpression.text

            for attrib in condition_expression_node.attrib:
                if attrib.endswith('resource') and condition_expression_node.attrib[attrib]:
                    conditionExpression = condition_expression_node.attrib[attrib]
                    break

            cond = self.parser.parse_condition(conditionExpression, outgoing_task, outgoing_task_node, sequence_flow_node, condition_expression_node, self)

            self.task.connect_outgoing_if(cond, outgoing_task, sequence_flow_node.get('id'), sequence_flow_node.get(
                'name', None), self.parser._parse_documentation(sequence_flow_node, task_parser=self))
