from business_rules.variables import numeric_rule_variable,boolean_rule_variable

from .resoner import MonitoringVariables

class CustomMonitoringVariables(MonitoringVariables):
	@numeric_rule_variable(label='Amount of urin relieved in last 4 hours')
	def customRuleTLL4(self):
		return self.getTimedLiquidLevel(4)
