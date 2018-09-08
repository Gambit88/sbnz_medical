from business_rules.variables import numeric_rule_variable

from .resoner import DiseaseVariables

class CustomDiseaseVariables(DiseaseVariables):
	@numeric_rule_variable(label='Patient had high temperature multiple times in last 10 days')
	def customRuleHTC10(self):
		return self.hadTemperature(10)
	@numeric_rule_variable(label='Patient had Fever diagnosed multiple times in last 6 days')
	def customRuleHDCFever6(self):
		return self.hadDisease('Fever',6)
	@numeric_rule_variable(label='Patient had DISEASE diagnosed multiple times in last 1000 days')
	def customRuleHDCDISEASE1000(self):
		return self.hadDisease('DISEASE',1000)
	@numeric_rule_variable(label='Patient had SYNDROME syndrome multiple times in last 1000 days')
	def customRuleHSCSYNDROME1000(self):
		return self.hadSyndrome('SYNDROME',1000)
	@numeric_rule_variable(label='Patient had high temperature multiple times in last 1000 days')
	def customRuleHTC1000(self):
		return self.hadTemperature(1000)
	@numeric_rule_variable(label='Patient had temperature above 1000 multiple times in last 1000 days')
	def customRuleTAC10001000(self):
		return self.hadTemperatureAbove(1000,1000)
	@numeric_rule_variable(label='Patient had medicine that is MEDTYPE prescribed multiple times in last 1000 days')
	def customRuleHMCMEDTYPE1000(self):
		return self.hadMedicineType('MEDTYPE',1000)
