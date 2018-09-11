from business_rules.variables import numeric_rule_variable,boolean_rule_variable

from .resoner import MonitoringVariables

class CustomMonitoringVariables(MonitoringVariables):
	@boolean_rule_variable(label='Oxygen level went up in last 15 minutes')
	def customRuleOWU15(self):
		return self.oxygenWentUp(15)
	@numeric_rule_variable(label='Number of hearthbeats in last 10 secounds')
	def customRuleHTR10(self):
		return self.getHearthRate(10)
	@boolean_rule_variable(label='Hronična bubrežna bolest is in patients disease records history')
	def customRuleDIHHronicnabubreznabolest(self):
		return self.checkDiseaseInHistory('Hronična bubrežna bolest')
	@numeric_rule_variable(label='Amount of urin relieved in last 12 hours')
	def customRuleTLL12(self):
		return self.getTimedLiquidLevel(12)
	@boolean_rule_variable(label='Oxygen level went down in last 15 minutes')
	def customRuleOWD15(self):
		return self.oxygenWentDown(15)
