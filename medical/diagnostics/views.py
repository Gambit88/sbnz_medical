from django.shortcuts import render
from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from django.template.defaulttags import register
from django.db import IntegrityError
from django.http import HttpResponse
from business_rules.engine import run_all
from business_rules.utils import export_rule_data
from pathlib import Path
from importlib import import_module
import json

from .models import Patient,Ingredient,Medicine,Disease,Syndrome,FileRule,Rule,Diagnosis,DiagnosedSyndromes
from monitoring.rule_writer import customMonitoringVariablesWriter
from .rule_writer import customDiagnosisVariablesWriter
from .resoner import AlergyActions,AlergyVariables,DiseaseActions,DiseaseVariables,DiseasesActions,DiseasesVariables,PatientActions,PatientVariables,SyndromeActions,SyndromeVariables
from monitoring.resoner import MonitoringActions,MonitoringVariables
# Create your views here.

def something(request):
    pass

#Doctor pages/resoner runners
#SYNDROME DETECTION
def diseasesyndpage(request):
    template = loader.get_template("pickDiseasePage.html")
    diseases = Disease.objects.all()
    return HttpResponse(template.render({'diseases':diseases,'user':request.user}))

def diseaseSyndList(request,disease_name):
    template = loader.get_template("syndromeListPage.html")
    syndromes = []
    disease = Disease.objects.get(name=disease_name)
    rules = Rule.objects.filter(ruletype=Rule.findDiseaseSymptomsRule).order_by('-priority')
    engRules = []
    for rule in rules:
        engRules.append(json.loads(rule.content))
    for syndrome in Syndrome.objects.all():
        syndromeActions = SyndromeActions()
        run_all(rule_list=engRules,
            defined_variables=SyndromeVariables(disease,syndrome),
            defined_actions=syndromeActions,
            stop_on_first_trigger=True
           )
        if syndromeActions.show:
            if syndromeActions.top:
                syndromes.insert(0,syndrome)
            else:
                syndromes.append(syndrome)
    
    return HttpResponse(template.render({'syndromes':syndromes,'user':request.user}))
#REPORTING
def reportpage(request):
    template = loader.get_template("reportingPickPage.html")
    rules = Rule.objects.filter(ruletype=Rule.patientInfoRule)
    return HttpResponse(template.render({'rules':rules,'user':request.user}))

def patientreportList(request):
    template = loader.get_template("patientListPage.html")
    patients = []
    rulesId = request.GET.get('rules').split(',')
    rules = Rule.objects.filter(ruletype=Rule.findDiseaseSymptomsRule).order_by('-priority')
    engRules = []
    for rule in rules:
        if str(rule.id) in rulesId:
            engRules.append(json.loads(rule.content))

    my_file = Path("./diagnostics/custom_variables_p.py")
    if my_file.is_file():
        module = import_module('.custom_variables_p',package="diagnostics")
        for patient in Patient.objects.all():
            patientActions = PatientActions()
            run_all(rule_list=engRules,
                defined_variables=module.CustomPatientVariables(patient),
                defined_actions=patientActions,
                stop_on_first_trigger=True
            )
            if patientActions.show:
                patients.append(patient)
    else:
        for patient in Patient.objects.all():
            patientActions = PatientActions()
            run_all(rule_list=engRules,
                defined_variables=PatientVariables(patient),
                defined_actions=patientActions,
                stop_on_first_trigger=True
            )
            if patientActions.show:
                patients.append(patient)
        
    return HttpResponse(template.render({'patients':patients,'user':request.user}))
#DISEASE SYNDROMES
def diseaselistPage(request):
    template = loader.get_template("diseaseListPage.html")
    diseasesRaw = []
    diseases = []
    diagnosis = DiagnosedSyndromes()
    syndromes = request.GET.get('syndromes').split(',')
    for synid in syndromes:
        diagnosis.syndromes.append(Syndrome.objects.get(id=int(synid)))
    rules = Rule.objects.filter(ruletype=Rule.findDiseaseRule).order_by('-priority')
    engRules = []
    for rule in rules:
        engRules.append(json.loads(rule.content))
    for disease in Disease.objects.all():
        diseaseActions = DiseasesActions()
        run_all(rule_list=engRules,
            defined_variables=DiseasesVariables(diagnosis,disease),
            defined_actions=diseaseActions,
            stop_on_first_trigger=True
           )
        if diseaseActions.show:
            diseasesRaw.append((disease,diseaseActions.correctSyndromes))
    for rawDis in sorted(diseasesRaw,key= lambda element:element[1],reverse=True):
        diseases.append(rawDis[0])
    
    return HttpResponse(template.render({'diseases':diseases,'user':request.user}))
#Patient
def patientsP(request):
    template = loader.get_template("patientsPage.html")
    patients = Patient.objects.all()
    return HttpResponse(template.render({'patients':patients,'user':request.user}))

def editPatientsP(request,id):
    template = loader.get_template("createPatientPage.html")
    ingredients = Ingredient.objects.all()
    medicines = Medicine.objects.all()
    if id=="None":
        return HttpResponse(template.render({'new':True,'user':request.user,'ingredients':ingredients,'medicines':medicines}))
    else:
        patient = Patient.objects.get(id=id)
        return HttpResponse(template.render({'new':False,'patient':patient,'user':request.user,'ingredients':ingredients,'medicines':medicines,'alergeni':patient.alergying.all(),'alergenm':patient.alergymed.all()}))

@csrf_exempt
def editPatient(request,patient_id):
    patient = Patient.objects.get(id=patient_id)
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    ingredients = request.POST.get('ingredients')
    medicines = request.POST.get('medicines')
    patient.name = name
    patient.surname = surname
    patient.alergying.clear()
    patient.alergymed.clear()
    for ingredient_id in ingredients.split(","):
        ingred = Ingredient.objects.get(id=ingredient_id)
        patient.alergying.add(ingred)
    for medicine_id in medicines.split(","):
        medicine = Medicine.objects.get(id=medicine_id)
        patient.alergymed.add(medicine)
    patient.save()
    return redirect('/diagnostics/patients/')
    
@csrf_exempt
def newPatient(request):
    patient = Patient.objects.create()
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    ingredients = request.POST.get('ingredients')
    medicines = request.POST.get('medicines')
    patient.name = name
    patient.surname = surname
    for ingredient_id in ingredients.split(","):
        ingred = Ingredient.objects.get(id=eval(ingredient_id))
        patient.alergying.add(ingred)
    for medicine_id in medicines.split(","):
        medicine = Medicine.objects.get(id=eval(medicine_id))
        patient.alergymed.add(medicine)
    patient.save()
    return redirect('/diagnostics/patients/')
#Ingredient
def ingredientsP(request):
    template = loader.get_template("ingredientsPage.html")
    ingredients = Ingredient.objects.all()
    return HttpResponse(template.render({'ingredients':ingredients,'user':request.user}))
def createIngredientPage(request):
    template = loader.get_template("createIngredientPage.html")
    return HttpResponse(template.render({'user':request.user}))
@csrf_exempt
def newIngredient(request):
    ingredient = Ingredient.objects.create()
    name = request.POST.get('name')
    ingredient.name = name
    ingredient.save()
    return redirect('/diagnostics/ingredients/')
#Medicine
def medicinesP(request):
    template = loader.get_template("medicinesPage.html")
    medicines = Medicine.objects.all()
    dt = dict(Medicine.Type_CHOICES)
    return HttpResponse(template.render({'medicines':medicines,'user':request.user, 'dict':dt}))
def editMedicineP(request,id):
    template = loader.get_template("createMedicinePage.html")
    ingredients = Ingredient.objects.all()
    dt = list(Medicine.Type_CHOICES)
    if id=="None":
        return HttpResponse(template.render({'new':True,'user':request.user,'ingredients':ingredients,'choice':dt}))
    else:
        medicine = Medicine.objects.get(id=id)
        print(medicine.medtype)
        return HttpResponse(template.render({'new':False,'medicine':medicine,'user':request.user,'ingredients':ingredients,'oldingredients':medicine.ingredient.all(),'choice':dt}))
@csrf_exempt
def editMedicine(request,medicine_id):
    medicine = Medicine.objects.get(id=medicine_id)
    name = request.POST.get('name')
    ingredients = request.POST.get('ingredients')
    medType = request.POST.get('type')
    medicine.name = name
    medicine.medtype = medType
    medicine.ingredient.clear()
    for ing_id in ingredients.split(","):
        ing = Ingredient.objects.get(id=ing_id)
        medicine.ingredient.add(ing)
    medicine.save()
    return redirect('/diagnostics/medicines/')
    
@csrf_exempt
def newMedicine(request):
    medicine = Medicine.objects.create()
    name = request.POST.get('name')
    ingredients = request.POST.get('ingredients')
    medType = request.POST.get('type')
    medicine.name = name
    medicine.medtype = medType
    for ing_id in ingredients.split(","):
        ing = Ingredient.objects.get(id=ing_id)
        medicine.ingredient.add(ing)
    medicine.save()
    return redirect('/diagnostics/medicines/')
#Syndrome
def syndromesP(request):
    template = loader.get_template("syndromesPage.html")
    syndromes = Syndrome.objects.all()
    return HttpResponse(template.render({'syndromes':syndromes,'user':request.user}))
def createSyndromePage(request):
    template = loader.get_template("createSyndromePage.html")
    return HttpResponse(template.render({'user':request.user}))
@csrf_exempt
def newSyndrome(request):
    syndrome = Syndrome.objects.create()
    name = request.POST.get('name')
    syndrome.name = name
    syndrome.save()
    return redirect('/diagnostics/syndromes/')
#Disease
def diseasesP(request):
    template = loader.get_template("diseasesPage.html")
    diseases = Disease.objects.all()
    return HttpResponse(template.render({'diseases':diseases,'user':request.user}))
def editDiseasesP(request,id):
    template = loader.get_template("createDiseasePage.html")
    syndromes = Syndrome.objects.all()
    if id=="None":
        return HttpResponse(template.render({'new':True,'user':request.user,'syndromes':syndromes}))
    else:
        disease = Disease.objects.get(id=id)
        return HttpResponse(template.render({'new':False,'disease':disease,'user':request.user,'syndromes':syndromes,'strongsynd':disease.strongsympt.all(),'regularsynd':disease.regularsympt.all()}))
@csrf_exempt
def editDisease(request,disease_id):
    disease = Disease.objects.get(id=disease_id)
    name = request.POST.get('name')
    regSyn = request.POST.get('regSynd')
    strSyn = request.POST.get('strSynd')
    disease.name = name
    disease.strongsympt.clear()
    disease.regularsympt.clear()
    for syn_id in regSyn.split(","):
        syndrome = Syndrome.objects.get(id=syn_id)
        disease.regularsympt.add(syndrome)
    for syn_id in strSyn.split(","):
        syndrome = Syndrome.objects.get(id=syn_id)
        disease.strongsympt.add(syndrome)
    disease.save()
    return redirect('/diagnostics/diseases/')
    
@csrf_exempt
def newDisease(request):
    disease = Disease.objects.create()
    name = request.POST.get('name')
    regSyn = request.POST.get('regSynd')
    strSyn = request.POST.get('strSynd')
    disease.name = name
    for syn_id in regSyn.split(","):
        syndrome = Syndrome.objects.get(id=syn_id)
        disease.regularsympt.add(syndrome)
    for syn_id in strSyn.split(","):
        syndrome = Syndrome.objects.get(id=syn_id)
        disease.strongsympt.add(syndrome)
    disease.save()
    return redirect('/diagnostics/diseases/')
#RuleExtentions
def ruleextsP(request):
    template = loader.get_template("ruleExtPage.html")
    fileRules = FileRule.objects.all()
    dt = dict(FileRule.Rule_CHOICES)
    return HttpResponse(template.render({'fileRules':fileRules,'user':request.user, 'dict':dt}))
def createRuleextPage(request):
    template = loader.get_template("createRuleExtPage.html")
    dt = list(FileRule.Rule_CHOICES)
    return HttpResponse(template.render({'user':request.user,'rule':dt}))
@csrf_exempt
def newRuleext(request):
    try:
        params = request.POST.get('params')
        rule = request.POST.get('extendRule')
        rset = None
        if rule.startswith('mv_'):
            rset = 'monv'
        elif rule.startswith('dv_'):
            rset = 'disv'
        elif rule.startswith('pv_'):
            rset = 'patv'

        ruleExt = FileRule.objects.create(extendedRule=rule,extendsRuleset=rset,params=params)
        ruleExt.save()
    except IntegrityError:
        return redirect('/diagnostics/ruleextensions/')

    monitoringRules = FileRule.objects.filter(extendsRuleset='monv')
    diseaseRules = FileRule.objects.filter(extendsRuleset='disv')
    patientRules = FileRule.objects.filter(extendsRuleset='patv')

    customMonitoringVariablesWriter(monitoringRules)
    customDiagnosisVariablesWriter(diseaseRules)
    customDiagnosisVariablesWriter(patientRules)

    return redirect('/diagnostics/ruleextensions/')
#Rules
def rulesP(request):
    template = loader.get_template("rulesPage.html")
    rules = Rule.objects.all()
    dt = dict(Rule.Type_CHOICES)
    return HttpResponse(template.render({'rules':rules,'user':request.user, 'dict':dt}))
def editRuleP(request,id):
    template = loader.get_template("createRulePage.html")
    if id=="None":
        return HttpResponse(template.render({'dict':list(Rule.Type_CHOICES),'user':request.user}))

@csrf_exempt
def newRule(request):
    title = request.POST.get('title')
    rtype = request.POST.get('type')
    content = request.POST.get('content')
    try:
        priority = int(request.POST.get('priority'))
    except:
        return redirect('/diagnostics/rules/')
    print(content)
    rule = Rule.objects.create(priority=priority)
    rule.title = title
    rule.ruletype = rtype
    rule.content = content
    rule.save()
    return redirect('/diagnostics/rules/')
@csrf_exempt
def deleteRule(request,ruleset_id):
    rule = Rule.objects.get(id=ruleset_id)
    rule.delete()
    return redirect('/diagnostics/rules/')
def ruleHelpDdmr(request):
    my_file = Path("./diagnostics/custom_variables_d.py")
    if my_file.is_file():
        module = import_module('.custom_variables_d',package="diagnostics")
        data = export_rule_data(module.CustomDiseaseVariables, DiseaseActions)
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data = export_rule_data(DiseaseVariables, DiseaseActions)
        return HttpResponse(json.dumps(data), content_type="application/json")
def ruleHelpPadr(request):
    data = export_rule_data(AlergyVariables, AlergyActions)
    return HttpResponse(json.dumps(data), content_type="application/json")
def ruleHelpFdsr(request):
    data = export_rule_data(SyndromeVariables, SyndromeActions)
    return HttpResponse(json.dumps(data), content_type="application/json")
def ruleHelpDdbosr(request):
    data = export_rule_data(DiseasesVariables, DiseasesActions)
    return HttpResponse(json.dumps(data), content_type="application/json")
def ruleHelpMar(request):
    my_file = Path("./monitoring/custom_variables_m.py")
    if my_file.is_file():
        module = import_module('.custom_variables_m',package="monitoring")
        data = export_rule_data(module.CustomMonitoringVariables, MonitoringActions)
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data = export_rule_data(MonitoringVariables, MonitoringActions)
        return HttpResponse(json.dumps(data), content_type="application/json")
def ruleHelpRfgp(request):
    my_file = Path("./diagnostics/custom_variables_p.py")
    if my_file.is_file():
        module = import_module('.custom_variables_p',package="diagnostics")
        data = export_rule_data(module.CustomPatientVariables, PatientActions)
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data = export_rule_data(PatientVariables, PatientActions)
        return HttpResponse(json.dumps(data), content_type="application/json")

#LOGIN STUFF
@csrf_exempt
def loginF(request):#TOTALY DONE
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if user.has_perm('rule.manage_rules'):
            return redirect('/diagnostics/patients/')
        return redirect('/diagnostics/diagnose/')
    else:
        return redirect('/diagnostics/loginPage/')

def logoutF(request):#TOTALY DONE
    logout(request)
    return redirect('/diagnostics/loginPage/')

def loginP(request):#TOTALY DONE
    template = loader.get_template("static/login.html")
    return HttpResponse(template.render())


#Filters:
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
@register.filter
def get_value(tuple):
    return tuple[0]
@register.filter
def get_text(tuple):
    return tuple[1]