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
    def __str__(self):
        return self.title

class MonitoringInfo(models.Model):
    heartratebeat = models.SmallIntegerField(verbose_name="Heartbeat rate")
    oxygenlevel = models.SmallIntegerField(verbose_name="Level of oxygen in blood")
    liquidlevel = models.SmallIntegerField(verbose_name="Amount of urine produced")
    time = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.time)

class Patient(models.Model):
    name = models.CharField(max_length= 50,verbose_name="Name")
    surname = models.CharField(max_length = 50,verbose_name="Surname")
    alergymed = models.ManyToManyField(Medicine,verbose_name="Allergic to medicines", blank=True)
    alergying = models.ManyToManyField(Ingredient,verbose_name="Allergic to ingredients", blank=True)
    monitoring = models.ManyToManyField(MonitoringInfo,verbose_name="Monitoring data records", blank=True)
    def __str__(self):
        return self.name + " " + self.surname + " Id:" + str(self.id)

class Diagnosis(models.Model):
    medicine = models.ManyToManyField(Medicine,verbose_name="Prescribed medicines")
    highTemp = models.BooleanField(verbose_name="User had high temperature")
    temp = models.SmallIntegerField(verbose_name="Temperature", blank=True)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE,verbose_name="Diagnosed disease")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Doctor responsable for diagnosis")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE, verbose_name="Patient")
    chance = models.SmallIntegerField(blank=True, verbose_name="Certainty that patient has a disease")
    time = models.DateTimeField(auto_now=True)
    def str(self):
        return self.disease.name





