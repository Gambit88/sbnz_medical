from business_rules.variables import BaseVariables,select_multiple_rule_variable,select_rule_variable,string_rule_variable,numeric_rule_variable
from business_rules.actions import BaseActions,rule_action
from business_rules.fields import FIELD_SELECT_MULTIPLE,FIELD_NUMERIC

from datetime import datetime, timedelta

#for alergy detection rules, run for all medicines in diagnosis
class AlergyVariables(BaseVariables):
    def __init__(self, patient, medicine):
        self.patient = patient
        self.medicine = medicine
    @select_multiple_rule_variable(label="Prescribed medicine ingredients")
    def getMedicineIngredients(self):
        return self.medicine.ingredient
    @select_rule_variable(label="Prescribed medicine")
    def getMedicine(self):
        return self.medicine
    @select_multiple_rule_variable(label="Medicines that patient is allergic to ")
    def getAlergyMedicines(self):
        return self.patient.alergymed
    @select_multiple_rule_variable(label="Ingredients that patient is allergic to")
    def getAlergyIngredients(self):
        return self.patient.alergying
    @string_rule_variable(label="Prescribed medicine type")
    def getMedicineType(self):
        return self.medicine.medtype
    @string_rule_variable(label="Prescribed medicine name")
    def getMedicineName(self):
        return self.medicine.name

class AlergyActions(BaseActions):
    def __init__(self):
        self.alarm = False
    @rule_action(label='Activate allergy alarm')
    def activateAlarm(self):
        self.alarm = True
    @rule_action(label="Deactivate allergy alarm")
    def deactivateAlarm(self):
        self.alarm = False


#for finding all disease with one of syndroms rules
class DiseasesVariables(BaseVariables):
    def __init__(self,diagnosis,disease):
        self.diagnosis = diagnosis
        self.disease = disease
    @select_multiple_rule_variable(label="Inputed syndromes")
    def getInputSyndromes(self):
        return self.diagnosis.syndroms
    @select_multiple_rule_variable(label="Specific disease syndromes")
    def getSDiseaseSyndromes(self):
        return self.disease.strongsympt
    @select_multiple_rule_variable(label="General disease syndromes")
    def getRDiseaseSyndromes(self):
        return self.disease.regularsympt
    @string_rule_variable(label = "Disease name")
    def getDiseaseName(self):
        return self.disease.name
    @numeric_rule_variable(label = "General disease syndromes count")
    def getRegSynCount(self):
        return len(self.disease.regularsympt)
    @numeric_rule_variable(label = "Specific disease syndromes count")
    def getSpecSynCount(self):
        return len(self.disease.strongsympt)
    @numeric_rule_variable(label = "Inputed syndromes count")
    def getSynCount(self):
        return len(self.diagnosis.syndromes)
    @numeric_rule_variable(label="Matched specific syndromes count")
    def getMssCount(self):
        count=0
        for syndrome in self.disease.strongsympt:
            if syndrome in self.diagnosis.syndromes:
                count = count + 1
        return count
    @numeric_rule_variable(label="Matched general syndromes count")
    def getMgsCount(self):
        count=0
        for syndrome in self.disease.regularsympt:
            if syndrome in self.diagnosis.syndromes:
                count = count + 1
        return count

class DiseasesActions(BaseActions):
    def __init__(self):
        self.show = False
        self.correctSyndromes = 0
    @rule_action(label='Add disease to show list')
    def showDisease(self):
        self.show = True
    @rule_action(label="Add sorting weight to disease",params= {"amount":FIELD_NUMERIC})
    def weight(self,amount):
        self.correctSyndromes = self.correctSyndromes + amount

#for finding disease syndroms rules
class SyndromeVariables(BaseVariables):
    def __init__(self,disease,syndrome):
        self.disease = disease
        self.syndrome = syndrome
    @select_multiple_rule_variable(label="Inputed disease name")
    def getInputDiseaseName(self):
        return self.disease.name
    @select_multiple_rule_variable(label="Specific disease syndromes")
    def getSDiseaseSyndromes(self):
        return self.disease.strongsympt
    @select_multiple_rule_variable(label="General disease syndromes")
    def getRDiseaseSyndromes(self):
        return self.disease.regularsympt
    @string_rule_variable(label = "Syndrome")
    def getDiseaseName(self):
        return self.syndrome
    @numeric_rule_variable(label = "Syndrome name")
    def getRegSynCount(self):
        return self.syndrome.name

class SyndromeActions(BaseActions):
    def __init__(self):
        self.show = False
    @rule_action(label='Add syndrome to show list')
    def showDisease(self):
        self.show = True

#for finding which disease might be a problem rules
class DiseaseVariables(BaseVariables):
    def __init__(self,diagnosis,disease):
        self.diagnosis = diagnosis
        self.disease = disease

class DiseaseActions(BaseActions):
    def __init__(self):
        self.alarm = False

#for finding patient data rules
class PatientVariables(BaseVariables):
    def __init__(self,patient):
        self.patient = patient
    def getRepetedDisNames(self,days,repeted):
        nameRepeatDict = {}
        results = []
        timeFrame = datetime.now() - timedelta(days = days)
        for diagnostics in self.patient.diagnosis_set.filter(time__gt=timeFrame):
            if diagnostics.disease.name in nameRepeatDict.keys():
                nameRepeatDict[diagnostics.disease.name] = nameRepeatDict[diagnostics.disease.name]+1
            else:
                nameRepeatDict[diagnostics.disease.name] = 1
        sortedNames = sorted(nameRepeatDict,key=nameRepeatDict.__getitem__,reverse=True)
        for name in sortedNames:
            if nameRepeatDict[name] >= repeted:
                results.append(name)
            else:
                return results
        return results
    def getNumberofMedicinesByType(self,days,medicineType):
        results = 0
        timeFrame = datetime.now() - timedelta(days = days)
        for diagnostics in self.patient.diagnosis_set.filter(time__gt=timeFrame):
            for medicine in diagnostics.medicine.all():
                if medicine.medtype == medicineType:
                    results = results + 1 
                    break
        return results
    def getDoctorPrescribingMedByTypeCount(self,days,medicineType):
        results = []
        timeFrame = datetime.now() - timedelta(days = days)
        for diagnostics in self.patient.diagnosis_set.filter(time__gt=timeFrame):
            for medicine in diagnostics.medicine.all():
                if medicine.medtype == medicineType:
                    if diagnostics.doctor.id in results:
                        pass
                    else:
                        results.append(diagnostics.doctor.id)
        return len(results)
    def getDiseaseNumByMedType(self,days,medicineType):
        results = []
        timeFrame = datetime.now() - timedelta(days = days)
        for diagnostics in self.patient.diagnosis_set.filter(time__gt=timeFrame):
            for medicine in diagnostics.medicine.all():
                if medicine.medtype == medicineType:
                    if diagnostics.disease.id in results:
                        pass
                    else:
                        results.append(diagnostics.disease.id)
        return len(results)


class PatientActions(BaseActions):
    def __init__(self):
        self.show = False
    @rule_action(label='Add patient to show list')
    def showPatient(self):
        self.show = True