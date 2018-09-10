from django.db import models
from django.contrib.auth.models import User

# Create your models here

class Syndrome(models.Model):
    name = models.CharField(max_length=150,verbose_name="Name")
    def __str__(self):
        return self.name

class Disease(models.Model):
    name = models.CharField(max_length=150,verbose_name="Name")
    strongsympt = models.ManyToManyField(Syndrome,related_name="strong_syndrome",verbose_name="Specific syndromes",blank=True)
    regularsympt = models.ManyToManyField(Syndrome,related_name="regular_syndrome",verbose_name="General syndromes")
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length= 150,verbose_name="Name")
    def __str__(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length= 150,verbose_name="Name")
    ingredient = models.ManyToManyField(Ingredient,verbose_name="Ingredients")
    analgesic='0'
    antibiotic='1'
    other='2'
    Type_CHOICES = (
		(analgesic, 'Analgesic'),
		(antibiotic, 'Antibiotic'),
		(other, 'Other'),
		)
    medtype = models.CharField(max_length=1,choices = Type_CHOICES,verbose_name="Medicine type")
    def __str__(self):
        return self.name

class Rule(models.Model):
    title = models.CharField(max_length= 500,verbose_name="Rule title")
    content = models.CharField(max_length = 10000,verbose_name="Rule")
    diseaseRule='0'
    alergyRule='1'
    findDiseaseSymptomsRule='2'
    findDiseaseRule='3'
    monitoringRule='4'
    patientInfoRule='5'
    Type_CHOICES = (
		(diseaseRule, 'Disease decision making rule'),
		(alergyRule, 'Patient alergy detection rule'),
		(findDiseaseSymptomsRule, 'Find disease symptoms rule'),
		(findDiseaseRule, 'Detect disease based on symptoms rule'),
		(monitoringRule, 'Monitoring alarm rule'),
		(patientInfoRule, 'Rule for grouping patients'),
		)
    ruletype = models.CharField(max_length=1,choices = Type_CHOICES,verbose_name="Rule type")
    priority = models.IntegerField(verbose_name="Rule priority")
    def __str__(self):
        return self.title
    class Meta:
        permissions = (("run_rules","Can run decision making process"),("manage_rules","Can make/change/delete rules"),)

class Patient(models.Model):
    name = models.CharField(max_length= 50,verbose_name="Name")
    surname = models.CharField(max_length = 50,verbose_name="Surname")
    alergymed = models.ManyToManyField(Medicine,verbose_name="Allergic to medicines", blank=True)
    alergying = models.ManyToManyField(Ingredient,verbose_name="Allergic to ingredients", blank=True)
    def __str__(self):
        return self.name + " " + self.surname + " Id:" + str(self.id)

class MonitoringInfo(models.Model):
    heartratebeat = models.SmallIntegerField(verbose_name="Heartbeat rate")
    oxygenlevel = models.SmallIntegerField(verbose_name="Level of oxygen in blood")
    liquidlevel = models.SmallIntegerField(verbose_name="Amount of urine produced")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.time)

class Diagnosis(models.Model):
    medicine = models.ManyToManyField(Medicine,verbose_name="Prescribed medicines")
    highTemp = models.BooleanField(verbose_name="User had high temperature")
    temp = models.SmallIntegerField(verbose_name="Temperature", blank=True)
    syndromes = models.ManyToManyField(Syndrome,verbose_name="Patient syndromes")
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE,verbose_name="Diagnosed disease")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Doctor responsable for diagnosis")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE, verbose_name="Patient")
    time = models.DateTimeField(auto_now=True)
    def str(self):
        return self.disease.name

class RezonerHelper():
    def __init__(self):
        self.bestPercent = 0
        self.bestRegSyndCount = 0
        self.bestStrSyndCount = 0
        self.diseaseName = ""

class FileRule(models.Model):
    params = models.CharField(max_length = 1000)
    monitoringVariable='monv'
    patientVariable='patv'
    diseaseVariable='disv'
    ruleTLL = 'mv_tll'
    ruleHR = 'mv_htr'
    ruleDIH = 'mv_dih'
    ruleOWU = 'mv_owu'
    ruleOWD = 'mv_owd'
    ruleHDC = 'dv_hdc'
    ruleHSC = 'dv_hsc'
    ruleHTC = 'dv_htc'
    ruleHTAC = 'dv_tac'
    ruleHMTC = 'dv_hmc'
    ruleRDN = 'pv_rdn'
    ruleNMT = 'pv_cmt'
    ruleDPMT = 'pv_dpc'
    ruleDNMT = 'pv_dmc'

    Rule_CHOICES = (
		(ruleTLL, '(Monitoring ruleset) Amount of urin relieved in last (n) hours. (Params: time_in_hours)'),
		(ruleHR, '(Monitoring ruleset) Number of hearthbeats in last (n) secounds. (Params: time_in_secounds)'),
		(ruleDIH, '(Monitoring ruleset) (x) disease is in patients records history. (Params: disease_name)'),
		(ruleOWU, '(Monitoring ruleset) Oxygen level went up in last (n) minutes. (Params: time_in_minutes)'),
		(ruleOWD, '(Monitoring ruleset) Oxygen level went down in last (n) minutes. (Params: time_in_minutes)'),
		(ruleHDC, '(Disease detection ruleset) Patient had (x) diagnosed multiple times in last (n) days. (Params: disease_name,number_of_days)'),
		(ruleHSC, '(Disease detection ruleset) Patient had (x) syndrome multiple times in last (n) days. (Params: syndrome_name,number_of_days)'),
		(ruleHTC, '(Disease detection ruleset) Patient had high temperature multiple times in last (n) days. (Params: number_of_days)'),
		(ruleHTAC, '(Disease detection ruleset) Patient had temperature above (x) multiple times in last (n) days. (Params: temperature,number_of_days)'),
		(ruleHMTC, '(Disease detection ruleset) Patient had medicine that is (x) prescribed multiple times in last (n) days. (Params: medicine_type,number_of_days)'),
		(ruleRDN, '(Patient data finding ruleset) Names of diseases that had repeated (x) times in last (n) days. (Params: number_of_repeats,number_of_days)'),
		(ruleNMT, '(Patient data finding ruleset) Number of medicines of (x) type prescribed in last (n) days. (Params: medicine_type,number_of_days)'),
		(ruleDPMT, '(Patient data finding ruleset) Number of different doctors prescribing medicine of (x) type in last (n) days (Params: medicine_type,number_of_days)'),
		(ruleDNMT, '(Patient data finding ruleset) Number of diseases that had medicine of (x) type prescribed in last (n) days (Params: medicine_type,number_of_days)'),
		)
    Ruleset_CHOICES = (
        (monitoringVariable,"Extends monitoring ruleset"),
        (patientVariable,"Extends patient data finding ruleset"),
        (diseaseVariable,"Extends disease detection ruleset"),
    )
    extendedRule = models.CharField(max_length=6,choices = Rule_CHOICES,verbose_name="Extended rule")
    extendsRuleset = models.CharField(max_length=4,choices = Ruleset_CHOICES,verbose_name="Extended ruleset")
    class Meta:
        unique_together = ('extendedRule','params')

class DiagnosedSyndromes():
    def __init__(self):
        self.syndromes = []
