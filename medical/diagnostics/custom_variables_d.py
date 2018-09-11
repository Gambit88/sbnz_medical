from business_rules.variables import numeric_rule_variable

from .resoner import DiseaseVariables

class CustomDiseaseVariables(DiseaseVariables):
	@numeric_rule_variable(label='Patient had Prehlada diagnosed multiple times in last 60 days')
	def customRuleHDCPrehlada60(self):
		return self.hadDisease('Prehlada',60)
	@numeric_rule_variable(label='Patient had Groznica diagnosed multiple times in last 60 days')
	def customRuleHDCGroznica60(self):
		return self.hadDisease('Groznica',60)
	@numeric_rule_variable(label='Patient had Visok pritisak syndrome multiple times in last 180 days')
	def customRuleHSCVisokpritisak180(self):
		return self.hadSyndrome('Visok pritisak',180)
	@numeric_rule_variable(label='Patient had Hipertenzija diagnosed multiple times in last 180 days')
	def customRuleHDCHipertenzija180(self):
		return self.hadDisease('Hipertenzija',180)
	@numeric_rule_variable(label='Patient had Hipertenzija diagnosed multiple times in last 36500 days')
	def customRuleHDCHipertenzija36500(self):
		return self.hadDisease('Hipertenzija',36500)
	@numeric_rule_variable(label='Patient had Dijabetes diagnosed multiple times in last 36500 days')
	def customRuleHDCDijabetes36500(self):
		return self.hadDisease('Dijabetes',36500)
	@numeric_rule_variable(label='Patient had temperature above 37 multiple times in last 14 days')
	def customRuleTAC3714(self):
		return self.hadTemperatureAbove(37,14)
	@numeric_rule_variable(label='Patient had high temperature multiple times in last 14 days')
	def customRuleHTC14(self):
		return self.hadTemperature(14)
	@numeric_rule_variable(label='Patient had medicine that is Antibiotic prescribed multiple times in last 21 days')
	def customRuleHMCAntibiotic21(self):
		return self.hadMedicineType('Antibiotic',21)
