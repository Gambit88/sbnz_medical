from business_rules.variables import numeric_rule_variable,boolean_rule_variable

from .resoner import MonitoringVariables

class CustomMonitoringVariables(MonitoringVariables):
	@numeric_rule_variable(label='Amount of urin relieved in last 1 hours')
	def customRuleTLL1(self):
		return self.getTimedLiquidLevel(1)
	@numeric_rule_variable(label='Number of hearthbeats in last 20 secounds')
	def customRuleHTR20(self):
		return self.getHearthRate(20)
	@boolean_rule_variable(label='Dijabetes is in patients disease records history')
	def customRuleDIHDijabetes(self):
		return self.checkDiseaseInHistory('Dijabetes')
	@boolean_rule_variable(label='Oxygen level went up in last 1 minutes')
	def customRuleOWU1(self):
		return self.oxygenWentUp(1)
	@boolean_rule_variable(label='Oxygen level went down in last 1 minutes')
	def customRuleOWD1(self):
		return self.oxygenWentDown(1)
