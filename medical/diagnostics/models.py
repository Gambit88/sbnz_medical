from django.db import models
from django.contrib.auth.models import User

# Create your models here

class Syndrome(models.Model):
    name = models.CharField(max_length=150)

class Disease(models.Model):
    name = models.CharField(max_length=150)
    strongsympt = models.ManyToManyField(Syndrome,related_name="strong_syndrome")
    regularsympt = models.ManyToManyField(Syndrome,related_name="regular_syndrome")

class Ingredient(models.Model):
    name = models.CharField(max_length= 150)

class Medicine(models.Model):
    name = models.CharField(max_length= 150)
    ingredient = models.ManyToManyField(Ingredient)
    analgesic='0'
    antibiotic='1'
    other='2'
    Type_CHOICES = (
		(analgesic, 'Analgesic'),
		(antibiotic, 'Antibiotic'),
		(other, 'Other'),
		)
    medtype = models.CharField(max_length=1,choices = Type_CHOICES)

class Rule(models.Model):
    title = models.CharField(max_length= 500)
    content = models.CharField(max_length = 10000)
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
    ruletype = models.CharField(max_length=1,choices = Type_CHOICES)

class MonitoringInfo(models.Model):
    heartratebeat = models.SmallIntegerField()
    oxygenlevel = models.SmallIntegerField()
    liquidlevel = models.SmallIntegerField()
    time = models.DateTimeField(auto_now=True)

class Patient(models.Model):
    name = models.CharField(max_length= 50)
    surname = models.CharField(max_length = 50)
    alergymed = models.ManyToManyField(Medicine)
    alergying = models.ManyToManyField(Ingredient)
    monitoring = models.ManyToManyField(MonitoringInfo)

class Diagnosis(models.Model):
    medicine = models.ManyToManyField(Medicine)
    highTemp = models.BooleanField()
    temp = models.SmallIntegerField()
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    chance = models.SmallIntegerField()
    time = models.DateTimeField(auto_now=True)





