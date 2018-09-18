from business_rules.variables import numeric_rule_variable

from .resoner import DiseaseVariables

class CustomDiseaseVariables(DiseaseVariables):
	@numeric_rule_variable(label='Patient had Dijabetes diagnosed multiple times in last 2 days')
	def customRuleHDCDijabetes2(self):
		return self.hadDisease('Dijabetes',2)
	@numeric_rule_variable(label='Patient had Kijanje symptom multiple times in last 2 days')
	def customRuleHSCKijanje2(self):
		return self.hadSyndrome('Kijanje',2)
	@numeric_rule_variable(label='Patient had high temperature multiple times in last 1 days')
	def customRuleHTC1(self):
		return self.hadTemperature(1)
	@numeric_rule_variable(label='Patient had temperature above 39 multiple times in last 1 days')
	def customRuleTAC391(self):
		return self.hadTemperatureAbove(39,1)
	@numeric_rule_variable(label='Patient had medicine that is Analgesic prescribed multiple times in last 2 days')
	def customRuleHMCAnalgesic2(self):
		return self.hadMedicineType('Analgesic',2)
