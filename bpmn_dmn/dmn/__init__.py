from bpmn_dmn.dmn.engine.dmn_parser import DMNParser
from bpmn_dmn.dmn.engine.dmn_engine import DMNEngine

class DMNDecisionRunner:
    def __init__(self, path, debug=None):
        self.path = path

        self.dmnParser = DMNParser(self.path)
        self.dmnParser.parse()

        decision = self.dmnParser.decision
        assert len(decision.decisionTables) == 1, 'Exactly one decision table should exist! (%s)' % (len(decision.decisionTables))

        self.dmnEngine = DMNEngine(decision.decisionTables[0], debug=debug)

    def decide(self, *inputArgs, **inputKwargs):
        return self.dmnEngine.decide(*inputArgs, **inputKwargs)
