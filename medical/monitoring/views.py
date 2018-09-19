import json
from pathlib import Path
from importlib import import_module
from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from business_rules import run_all

from diagnostics.models import Alarm,Patient,Rule,MonitoringInfo
from .resoner import MonitoringActions,MonitoringVariables
# Create your views here.
#Alarm checker area

@login_required(login_url="/diagnostics/loginPage/")
@permission_required('diagnostics.run_rules')
def getPage(request):
    template = loader.get_template("monitoringPage.html")
    alarms = Alarm.objects.filter(solved=False)
    return HttpResponse(template.render({'user':request.user,'alarms':alarms}))


@login_required(login_url="/diagnostics/loginPage/")
@permission_required('diagnostics.run_rules')
def solve(request,alarm_id):
    alarm = Alarm.objects.get(id=alarm_id)
    alarm.solved = True
    alarm.save()
    return redirect('/monitoring/alarms/')

@csrf_exempt
def info(request,patient_id):
    hb = request.POST.get('heartratebeat')
    ol = request.POST.get('oxygenlevel')
    ll = request.POST.get('liquidlevel')
    patient = Patient.objects.get(id=int(patient_id))
    try:
        monitoring = MonitoringInfo.objects.create(heartratebeat=int(hb),oxygenlevel=int(ol),liquidlevel=int(ll),patient=patient)
        monitoring.save()
    except:
        return HttpResponse(status=400)
    rules = Rule.objects.filter(ruletype=Rule.monitoringRule).order_by('-priority')
    engRules = []
    for rule in rules:
        engRules.append(json.loads(rule.content))

    my_file = Path("./monitoring/custom_variables_m.py")
    if my_file.is_file():
        module = import_module('.custom_variables_m',package="monitoring")
        for rule in engRules:
            l = []
            l.append(rule)
            monitoringActions = MonitoringActions()
            run_all(rule_list=l,
                defined_variables=module.CustomMonitoringVariables(monitoring,patient),
                defined_actions=monitoringActions,
                stop_on_first_trigger=False
            )
            if monitoringActions.alarm:
                if Alarm.objects.filter(alarm=monitoringActions.name,patientId=patient.id,solved=False).first() is None:
                    alarm  = Alarm.objects.create(alarm=monitoringActions.name,patientId=patient.id,patient=patient.name+" "+patient.surname,solved=False)
                    alarm.save()
            
    else:
        for rule in engRules:
            l = []
            l.append(rule)
            monitoringActions = MonitoringActions()
            run_all(rule_list=l,
                defined_variables=MonitoringVariables(monitoring,patient),
                defined_actions=monitoringActions,
                stop_on_first_trigger=False
            )
            if monitoringActions.alarm:
                if Alarm.objects.filter(alarm=monitoringActions.name,patientId=patient.id,solved=False).first() is None:
                    alarm  = Alarm.objects.create(alarm=monitoringActions.name,patientId=patient.id,patient=patient.name+" "+patient.surname,solved=False)
                    alarm.save()
    
    return HttpResponse(status=200)

