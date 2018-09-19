from business_rules.variables import BaseVariables,select_multiple_rule_variable,select_rule_variable,string_rule_variable,numeric_rule_variable,boolean_rule_variable
from business_rules.actions import BaseActions,rule_action
from business_rules.fields import FIELD_SELECT_MULTIPLE,FIELD_NUMERIC,FIELD_TEXT
from django.core import serializers

from .models import Medicine,Ingredient,Symptom,Disease

from datetime import datetime, timedelta

#mora izmena
#for alergy detection rules, run for all medicines in diagnosis
def getNamesList(objects):
    l = []
    for obj in objects:
        l.append(obj.name)
    return l
class AlergyVariables(BaseVariables):
    def __init__(self, patient, medicine):
        self.patient = patient
        self.medicine = medicine
    @select_multiple_rule_variable(label="Prescribed medicine ingredients",options=getNamesList(Ingredient.objects.all()))
    def getMedicineIngredients(self):
        return getNamesList(self.medicine.ingredient.all())
    @select_rule_variable(label="Prescribed medicine", options=getNamesList(Medicine.objects.all()))
    def getMedicine(self):
        return self.medicine.name
    @select_multiple_rule_variable(label="Medicines that patient is allergic to ", options=getNamesList(Medicine.objects.all()))
    def getAlergyMedicines(self):
        return getNamesList(self.patient.alergymed.all())
    @select_multiple_rule_variable(label="Ingredients that patient is allergic to",options=getNamesList(Ingredient.objects.all()))
    def getAlergyIngredients(self):
        return getNamesList(self.patient.alergying.all())
    @string_rule_variable(label="Prescribed medicine type")
    def getMedicineType(self):
        return self.medicine.medtype
    @string_rule_variable(label="Prescribed medicine name")
    def getMedicineName(self):
        return self.medicine.name
    @boolean_rule_variable(label="Prescribed medicine is in patients allergic medicines list")
    def getIngredientMatched(self):
        if self.medicine in self.patient.alergymed.all():
            return True
        return False
    @boolean_rule_variable(label="Prescribed medicine has an ingredient that can be found in patients allergic ingredients list")
    def getMedicineMatched(self):
        for ing in self.medicine.ingredient.all():
            if ing in self.patient.alergying.all():
                return True
        return False

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
    @select_multiple_rule_variable(label="Inputed symptoms",options=getNamesList(Symptom.objects.all()))
    def getInputSyndromes(self):
        return getNamesList(self.diagnosis.symptoms)
    @select_multiple_rule_variable(label="Specific disease symptoms",options=getNamesList(Symptom.objects.all()))
    def getSDiseaseSyndromes(self):
        return getNamesList(self.disease.strongsympt.all())
    @select_multiple_rule_variable(label="General disease symptoms",options=getNamesList(Symptom.objects.all()))
    def getRDiseaseSyndromes(self):
        return getNamesList(self.disease.regularsympt.all())
    @string_rule_variable(label = "Disease name")
    def getDiseaseName(self):
        return self.disease.name
    @numeric_rule_variable(label = "General disease symptoms count")
    def getRegSynCount(self):
        return len(self.disease.regularsympt.all())
    @numeric_rule_variable(label = "Specific disease symptoms count")
    def getSpecSynCount(self):
        return len(self.disease.strongsympt.all())
    @numeric_rule_variable(label = "Inputed symptoms count")
    def getSynCount(self):
        return len(self.diagnosis.symptoms)
    @numeric_rule_variable(label="Matched specific symptoms count")
    def getMssCount(self):
        count=0
        for symptom in self.disease.strongsympt.all():
            if symptom in self.diagnosis.symptoms:
                count = count + 1

        #print("MSS:"+str(count))
        return count
    @numeric_rule_variable(label="Matched general symptoms count")
    def getMgsCount(self):
        count=0
        for symptom in self.disease.regularsympt.all():
            if symptom in self.diagnosis.symptoms:
                count = count + 1

        #print("GSS:"+str(count))
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
        self.correctSyndromes = int(amount)

#for finding disease syndroms rules
class SyndromeVariables(BaseVariables):
    def __init__(self,disease,symptom):
        self.disease = disease
        self.symptom = symptom
    @select_multiple_rule_variable(label="Inputed disease name", options=getNamesList(Disease.objects.all()))
    def getInputDiseaseName(self):
        return self.disease.name
    @select_multiple_rule_variable(label="Specific disease symptoms", options=getNamesList(Symptom.objects.all()))
    def getSDiseaseSyndromes(self):
        return getNamesList(self.disease.strongsympt.all())
    @select_multiple_rule_variable(label="General disease symptoms", options=getNamesList(Symptom.objects.all()))
    def getRDiseaseSyndromes(self):
        return getNamesList(self.disease.regularsympt.all())
    @string_rule_variable(label = "Symptom name")
    def getSyndName(self):
        return self.symptom.name
    @boolean_rule_variable(label = "Symptom is contained in list of specific disease symptoms")
    def getRegSynCount(self):
        if self.symptom in self.disease.strongsympt.all():
            return True
        else:
            return False
    @boolean_rule_variable(label = "Symptom is contained in list of general disease symptoms")
    def getStrSynCount(self):
        if self.symptom in self.disease.regularsympt.all():
            return True
        else:
            return False

class SyndromeActions(BaseActions):
    def __init__(self):
        self.show = False
        self.top = False
    @rule_action(label='Add symptom to show list')
    def show1Disease(self):
        self.show = True
        self.top = False
    @rule_action(label='Add symptom to top of show list')
    def show2Disease(self):
        self.show = True
        self.top = True

#for finding which disease might be a problem rules
class DiseaseVariables(BaseVariables):
    def __init__(self,diagnosis,disease,helper):
        self.diagnosis = diagnosis
        self.disease = disease
        self.helper = helper
    @select_multiple_rule_variable(label="List of inputed symptom names",options=getNamesList(Symptom.objects.filter(technical=False)))
    def getSyndromesNames(self):
        result = []
        for symptom in self.diagnosis.symptoms.all():
            result.append(symptom.name)
        return result
    @numeric_rule_variable(label="Temperature in *C")
    def getTemperature(self):
        return self.diagnosis.temp
    @select_multiple_rule_variable(label="Name of current disease",options=getNamesList(Disease.objects.all()))
    def getDiseaseName(self):
        return self.disease.name
    @boolean_rule_variable(label="Patient has temperature")
    def hasTemperature(self):
        return self.diagnosis.highTemp
    #OVO PRAVILO@numeric_rule_variable(label='')
    def hadDisease(self,diseaseName,days):
        results = []
        timeFrame = datetime.now() - timedelta(days = days)
        for diagnostics in self.diagnosis.patient.diagnosis_set.filter(time__gt=timeFrame):
            if diagnostics.disease is not None and diagnostics.disease.name == diseaseName:
                results.append(diagnostics.disease.id)
        return len(results)
    #OVO PRAVILO
    def hadSyndrome(self,symptomName,days):
        results = []
        timeFrame = datetime.now() - timedelta(days = days)
        for diagnostics in self.diagnosis.patient.diagnosis_set.filter(time__gt=timeFrame):
            for symptom in diagnostics.symptoms:
                if symptom.name == symptomName:
                    results.append(diagnostics.id)
                    break
        return len(results)
    #OVO PRAVILO
    def hadTemperature(self,days):
        results = []
        timeFrame = datetime.now() - timedelta(days = days)
        for diagnostics in self.diagnosis.patient.diagnosis_set.filter(time__gt=timeFrame):
            if diagnostics.highTemp:
                results.append(diagnostics.id)
        return len(results)
    #OVO PRAVILO
    def hadTemperatureAbove(self,amount,days):
        results = []
        timeFrame = datetime.now() - timedelta(days = days)
        for diagnostics in self.diagnosis.patient.diagnosis_set.filter(time__gt=timeFrame):
            if diagnostics.temp > amount:
                results.append(diagnostics.id)
        return len(results)
    #OVO PRAVILO
    def hadMedicineType(self,typeOfMedicine,days):
        results = []
        timeFrame = datetime.now() - timedelta(days = days)
        for diagnostics in self.diagnosis.patient.diagnosis_set.filter(time__gt=timeFrame):
            for medicine in diagnostics.medicine.all():
                if medicine is not None and medicine.medtype == typeOfMedicine:
                    results.append(diagnostics.id)
                    break
        return len(results)
    @numeric_rule_variable(label="Number of symptoms connected to current disease")
    def getSyndCount(self):
        res = 0
        for symptom in self.diagnosis.symptoms.all():
            for dsynd in self.disease.strongsympt.filter(technical=False):
                if symptom.name == dsynd.name:
                    res = res + 1
        for symptom in self.diagnosis.symptoms.all():
            for dsynd in self.disease.regularsympt.filter(technical=False):
                if symptom.name == dsynd.name:
                    res = res + 1
        return res
    @numeric_rule_variable(label="Number of symptoms connected to most likely diagnosed disease")
    def getBestSyndCount(self):
        return self.helper.bestRegSyndCount + self.helper.bestStrSyndCount
    @numeric_rule_variable(label="Probability connected to diagnosing current disease")
    def getPercent(self):
        return ((self.getSyndCount()/(len(self.disease.regularsympt.all())+len(self.disease.strongsympt.all())))*100)
    @numeric_rule_variable(label="Probability connected to diagnosing most likely diagnosed disease")
    def getBestPercent(self):
        return self.helper.bestPercent
    @numeric_rule_variable(label="Number of strong symptoms connected to current disease")
    def getSpecSyndCount(self):
        res = 0
        for symptom in self.diagnosis.symptoms.all():
            for dsynd in self.disease.strongsympt.filter(technical=False):
                if symptom.name == dsynd.name:
                    res = res + 1
        return res
    @numeric_rule_variable(label="Number of strong symptoms connected to most likely diagnosed disease")
    def getBestSpecSyndCount(self):
        return self.helper.bestStrSyndCount
    @numeric_rule_variable(label="Number of regular symptoms connected to current disease")
    def getRegSyndCount(self):
        res = 0
        for symptom in self.diagnosis.symptoms.all():
            for dsynd in self.disease.regularsympt.filter(technical=False):
                if symptom.name == dsynd.name:
                    res = res + 1
        return res
    @numeric_rule_variable(label="Number of regular symptoms connected to most likely diagnosed disease")
    def getBestRegSyndCount(self):
        return self.helper.bestRegSyndCount
    @numeric_rule_variable(label="Name of most likely diagnosed disease")
    def getBestDiseaseName(self):
        return int(self.helper.diseaseName)


class DiseaseActions(BaseActions):
    def __init__(self,helper,variables):
        self.helper = helper
        self.variables = variables
    @rule_action(label="Set current disease as most likely diagnosed disease")
    def setDiseaseName(self):
        self.helper.diseaseName = self.variables.disease.name
        self.helper.bestStrSyndCount = self.variables.getSpecSyndCount()
        self.helper.bestRegSyndCount = self.variables.getRegSyndCount()
        self.helper.bestPercent = self.variables.getPercent()
    @rule_action(label="Set current disease as most likely diagnosed disease if percentage of likeliness is higher than current best")
    def setBestSsyn(self):
        if self.variables.getPercent()>self.helper.bestPercent:
            self.setDiseaseName()
    @rule_action(label="Set current disease as most likely diagnosed disease if strong symptom count is higher than current best")
    def setBestRsyn(self):
        if self.variables.getSpecSyndCount()>self.helper.bestStrSyndCount:
            self.setDiseaseName()
    @rule_action(label="Set current disease as most likely diagnosed disease if regular symptom count is higher than current best")
    def setBestPerc(self):
        if self.variables.getRegSyndCount()>self.helper.bestRegSyndCount:
            self.setDiseaseName()
    @rule_action(label="Set current disease as most likely diagnosed disease if percentage(calculated after addition of completed complex parameters) of likeliness is higher than current best",params={'completed':FIELD_NUMERIC})
    def setBestcomplex(self,completed):
        if ((self.variables.getSyndCount()+completed)/((len(self.variables.disease.strongsympt.all())+len(self.variables.disease.regularsympt.all()))*100))>self.helper.bestPercent:
            self.helper.diseaseName = self.variables.disease.name
            self.helper.bestStrSyndCount = self.variables.getSpecSyndCount()
            self.helper.bestRegSyndCount = self.variables.getRegSyndCount()
            self.helper.bestPercent = ((self.variables.getSyndCount()+completed)/((len(self.variables.disease.strongsympt.all())+len(self.variables.disease.regularsympt.all()))*100))

#for finding patient data rules
class PatientVariables(BaseVariables):
    def __init__(self,patient):
        self.patient = patient
    #OVO PRAVILO
    def getRepetedDisNames(self,repeted,days):
        nameRepeatDict = {}
        results = []
        timeFrame = datetime.now() - timedelta(days = days)
        for diagnostics in self.patient.diagnosis_set.filter(time__gt=timeFrame):
            if diagnostics.disease is not None:
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
    #OVO PRAVILO
    def getNumberofMedicinesByType(self,medicineType,days):
        results = 0
        timeFrame = datetime.now() - timedelta(days = days)
        for diagnostics in self.patient.diagnosis_set.filter(time__gt=timeFrame):
            for medicine in diagnostics.medicine.all():
                if medicine.medtype == Medicine.Type_DICT[medicineType]:
                    results = results + 1 
                    break
        return results
    #OVO PRAVILO
    def getDoctorPrescribingMedByTypeCount(self,medicineType,days):
        results = []
        timeFrame = datetime.now() - timedelta(days = days)
        for diagnostics in self.patient.diagnosis_set.filter(time__gt=timeFrame):
            for medicine in diagnostics.medicine.all():
                if medicine.medtype == Medicine.Type_DICT[medicineType]:
                    if diagnostics.doctor.id in results:
                        pass
                    else:
                        results.append(diagnostics.doctor.id)
        return len(results)
    #OVO PRAVILO
    def getDiseaseNumByMedType(self,medicineType,days):
        results = []
        timeFrame = datetime.now() - timedelta(days = days)
        for diagnostics in self.patient.diagnosis_set.filter(time__gt=timeFrame):
            for medicine in diagnostics.medicine.all():
                if medicine.medtype == Medicine.Type_DICT[medicineType]:
                    if diagnostics.disease.id in results:
                        pass
                    else:
                        results.append(diagnostics.disease.id)
        return len(results)
    #OVO PRAVILO
    def getDiseaseNumByMedTypeNot(self,medicineType,days):
        results = []
        timeFrame = datetime.now() - timedelta(days = days)
        for diagnostics in self.patient.diagnosis_set.filter(time__gt=timeFrame):
            tmp = True
            for medicine in diagnostics.medicine.all():
                if medicine.medtype == Medicine.Type_DICT[medicineType]:
                    tmp = False
            if tmp:
                if diagnostics.disease is None or diagnostics.disease.id in results:
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