from business_rules.variables import numeric_rule_variable,select_multiple_rule_variable

from .models import Disease
from .resoner import PatientVariables,getNamesList

class CustomPatientVariables(PatientVariables):
	@select_multiple_rule_variable(label='Names of diseases that had repeated 5 times in last 730 days',options=getNamesList(Disease.objects.all()))
	def customRuleRDN5730(self):
		return self.getRepetedDisNames(5,730)
	@numeric_rule_variable(label='Number of medicines of Analgesic type prescribed in last 180 days')
	def customRuleCMTAnalgesic180(self):
		return self.getNumberofMedicinesByType('Analgesic',180)
	@numeric_rule_variable(label='Number of different doctors prescribing medicine of Analgesic type in last 180 days')
	def customRuleDPCAnalgesic180(self):
		return self.getDoctorPrescribingMedByTypeCount('Analgesic',180)
	@numeric_rule_variable(label='Number of diseases that had medicine of Analgesic type prescribed in last 360 days')
	def customRuleDMCAnalgesic360(self):
		return self.getDiseaseNumByMedType('Analgesic',360)
	@numeric_rule_variable(label='Number of diseases that had medicine of Antibiotic type prescribed in last 360 days')
	def customRuleDMCAntibiotic360(self):
		return self.getDiseaseNumByMedType('Antibiotic',360)
	@numeric_rule_variable(label='Number of diseases that had medicine of Other type prescribed in last 360 days')
	def customRuleDMCOther360(self):
		return self.getDiseaseNumByMedType('Other',360)
	@numeric_rule_variable(label='Number of medicines of Antibiotic type prescribed in last 360 days')
	def customRuleCMTAntibiotic360(self):
		return self.getNumberofMedicinesByType('Antibiotic',360)
	@numeric_rule_variable(label='Number of diseases that did not have medicine of Antibiotic type prescribed in last 360 days')
	def customRuleMCNAntibiotic360(self):
		return self.getDiseaseNumByMedTypeNot('Antibiotic',360)
