from business_rules.variables import numeric_rule_variable,select_multiple_rule_variable

from .models import Disease
from .resoner import PatientVariables,getNamesList

class CustomPatientVariables(PatientVariables):
	@numeric_rule_variable(label='Number of diseases that had medicine of other type prescribed in last 6 days')
	def customRuleDMCother6(self):
		return self.getDiseaseNumByMedType('other',6)
	@select_multiple_rule_variable(label='Names of diseases that had repeated 5 times in last 731 days',options=getNamesList(Disease.objects.all()))
	def customRuleRDN5731(self):
		return self.getRepetedDisNames(5,731)
	@numeric_rule_variable(label='Number of diseases that had medicine of anelgetics type prescribed in last 180 days')
	def customRuleDMCanelgetics180(self):
		return self.getDiseaseNumByMedType('anelgetics',180)
	@numeric_rule_variable(label='Number of diseases that had medicine of Analgesic type prescribed in last 180 days')
	def customRuleDMCAnalgesic180(self):
		return self.getDiseaseNumByMedType('Analgesic',180)
	@numeric_rule_variable(label='Number of different doctors prescribing medicine of Analgesic type in last 180 days')
	def customRuleDPCAnalgesic180(self):
		return self.getDoctorPrescribingMedByTypeCount('Analgesic',180)
	@numeric_rule_variable(label='Number of diseases that had medicine of Antibiotic type prescribed in last 360 days')
	def customRuleDMCAntibiotic360(self):
		return self.getDiseaseNumByMedType('Antibiotic',360)
	@select_multiple_rule_variable(label='Names of diseases that had repeated 2 times in last 10 days',options=getNamesList(Disease.objects.all()))
	def customRuleRDN210(self):
		return self.getRepetedDisNames(2,10)
