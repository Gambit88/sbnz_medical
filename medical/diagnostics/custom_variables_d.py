from business_rules.variables import numeric_rule_variable

from .resoner import DiseaseVariables

class CustomDiseaseVariables(DiseaseVariables):
	@numeric_rule_variable(label='Patient had high temperature multiple times in last 10 days')
	def customRuleHTC10(self):
		return self.hadTemperature(10)
	@numeric_rule_variable(label='Patient had Fever diagnosed multiple times in last 6 days')
	def customRuleHDCFever6(self):
		return self.hadDisease('Fever',6)
