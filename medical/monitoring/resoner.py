from business_rules.variables import BaseVariables,numeric_rule_variable,boolean_rule_variable
from business_rules.actions import BaseActions,rule_action
from business_rules.fields import FIELD_NUMERIC

from datetime import datetime, timedelta

#for monitoring rules
class PatientVariables(BaseVariables):
    def __init__(self,monitoring,patient):
        self.monitoring = monitoring
        self.patient = patient
    @numeric_rule_variable(label="Oxygen level in blood")
    def getOxygenLevel(self):
        return self.monitoring.oxygenlevel
    @numeric_rule_variable(label="Amount of urin relieved")
    def getLiquidLevel(self):
        return self.monitoring.liquidlevel
    @numeric_rule_variable(label="Amount of urin relieved in last n hours")
    def getTimedLiquidLevel(self,hours):
        summary = 0
        lastHours = datetime.now() - timedelta(hours = hours)
        for monitorings in self.patient.monitoring_set.filter(time__gt=lastHours):
            summary = summary + monitorings.liquidlevel
        return summary
    @numeric_rule_variable(label="Number of hearthbeats in last n secounds")
    def getHearthRate(self,secounds):
        return (self.monitoring.heartratebeat/60)*secounds
    @boolean_rule_variable(label="x disease is in patients records history")
    def checkDiseaseInHistory(self,disease):
        for diagnosis in self.patient.diagnostics_set.all():
            if disease == diagnosis.disease.name:
                return True
        return  False
    @boolean_rule_variable(label="Oxygen level went up in last x minutes")
    def oxygenWentUp(self,minutes):
        timeFrame = datetime.now() - timedelta(minutes = minutes)
        tmpLevel = None
        for monitorings in self.patient.monitoring_set.filter(time__gt=timeFrame).order_by('time'):
            if tmpLevel!=None:
                if tmpLevel<monitorings.oxygenlevel:
                    return True
            else:
                tmpLevel = monitorings.oxygenlevel
        return False
    @boolean_rule_variable(label="Oxygen level went down in last x minutes")    
    def oxygenWentDown(self,minutes):
        timeFrame = datetime.now() - timedelta(minutes = minutes)
        tmpLevel = None
        for monitorings in self.patient.monitoring_set.filter(time__gt=timeFrame).order_by('time'):
            if tmpLevel!=None:
                if tmpLevel>monitorings.oxygenlevel:
                    return True
            else:
                tmpLevel = monitorings.oxygenlevel
        return False

class PatientActions(BaseActions):
    def __init__(self):
        self.alarm = False
    @rule_action(label='Activate alarm')
    def activateAlarm(self):
        self.alarm = True
    @rule_action(label='Deactivate alarm')
    def deactivateAlarm(self):
        self.alarm = False