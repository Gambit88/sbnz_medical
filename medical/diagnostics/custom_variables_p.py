from business_rules.variables import numeric_rule_variable,select_multiple_rule_variable

from .models import Disease
from .resoner import PatientVariables,getNamesList

class CustomPatientVariables(PatientVariables):
	@select_multiple_rule_variable(label='Names of diseases that had repeated 2 times in last 2 days',options=getNamesList(Disease.objects.all()))
	def customRuleRDN22(self):
		return self.getRepetedDisNames(2,2)
	@numeric_rule_variable(label='Number of medicines of Analgesic type prescribed in last 1 days')
	def customRuleCMTAnalgesic1(self):
		return self.getNumberofMedicinesByType('Analgesic',1)
	@numeric_rule_variable(label='Number of different doctors prescribing medicine of Analgesic type in last 1 days')
	def customRuleDPCAnalgesic1(self):
		return self.getDoctorPrescribingMedByTypeCount('Analgesic',1)
	@numeric_rule_variable(label='Number of diseases that had medicine of Analgesic type prescribed in last 1 days')
	def customRuleDMCAnalgesic1(self):
		return self.getDiseaseNumByMedType('Analgesic',1)
	@numeric_rule_variable(label='Number of diseases that did not have medicine of Analgesic type prescribed in last 1 days')
	def customRuleMCNAnalgesic1(self):
		return self.getDiseaseNumByMedTypeNot('Analgesic',1)
