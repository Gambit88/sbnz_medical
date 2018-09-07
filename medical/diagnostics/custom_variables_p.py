from business_rules.variables import numeric_rule_variable,select_multiple_rule_variable

from .resoner import PatientVariables

class CustomPatientVariables(PatientVariables):
	@numeric_rule_variable(label='Number of diseases that had medicine of other type prescribed in last 6 days')
	def customRuleDMCother6(self):
		return self.getDiseaseNumByMedType('other',6)
