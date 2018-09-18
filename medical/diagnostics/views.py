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

from .models import Patient,Ingredient,Medicine,Disease,Symptom,FileRule,Rule,Diagnosis,DiagnosedSymptomes,RezonerHelper
from monitoring.rule_writer import customMonitoringVariablesWriter
from .rule_writer import customDiagnosisVariablesWriter
from .resoner import AlergyActions,AlergyVariables,DiseaseActions,DiseaseVariables,DiseasesActions,DiseasesVariables,PatientActions,PatientVariables,SyndromeActions,SyndromeVariables
from monitoring.resoner import MonitoringActions,MonitoringVariables
# Create your views here.
#Doctor pages/resoner runners
#symptom DETECTION
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.run_rules')#diagnostics.manage_rules
def diseasesyndpage(request):
    template = loader.get_template("pickDiseasePage.html")
    diseases = Disease.objects.all()
    return HttpResponse(template.render({'diseases':diseases,'user':request.user}))

@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.run_rules')
def diseaseSyndList(request,disease_name):
    template = loader.get_template("syndromeListPage.html")
    symptoms = []
    disease = Disease.objects.get(name=disease_name)
    rules = Rule.objects.filter(ruletype=Rule.findDiseaseSymptomsRule).order_by('-priority')
    engRules = []
    for rule in rules:
        engRules.append(json.loads(rule.content))
    for symptom in Symptom.objects.all():
        syndromeActions = SyndromeActions()
        run_all(rule_list=engRules,
            defined_variables=SyndromeVariables(disease,symptom),
            defined_actions=syndromeActions,
            stop_on_first_trigger=True
           )
        if syndromeActions.show:
            if syndromeActions.top:
                symptoms.insert(0,symptom)
            else:
                symptoms.append(symptom)
    
    return HttpResponse(template.render({'symptoms':symptoms,'user':request.user}))
#REPORTING
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.run_rules')
def reportpage(request):
    template = loader.get_template("reportingPickPage.html")
    rules = Rule.objects.filter(ruletype=Rule.patientInfoRule)
    return HttpResponse(template.render({'rules':rules,'user':request.user}))

@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.run_rules')
def patientreportList(request):
    template = loader.get_template("patientListPage.html")
    patients = []
    rulesId = request.GET.get('rules').split(',')
    rules = Rule.objects.filter(ruletype=Rule.patientInfoRule).order_by('-priority')
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
#DISEASE BASED ON SYNDROMES
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.run_rules')
def diseaselistPage(request):
    template = loader.get_template("diseaseListPage.html")
    diseasesRaw = []
    diseases = []
    diagnosis = DiagnosedSymptomes()
    symptoms = request.GET.get('symptoms').split(',')
    for synid in symptoms:
        diagnosis.symptoms.append(Symptom.objects.get(id=int(synid)))
    rules = Rule.objects.filter(ruletype=Rule.findDiseaseRule).order_by('-priority')
    engRules = []
    for rule in rules:
        engRules.append(json.loads(rule.content))
    for disease in Disease.objects.all():
        diseaseActions = DiseasesActions()
        run_all(rule_list=engRules,
            defined_variables=DiseasesVariables(diagnosis,disease),
            defined_actions=diseaseActions,
            stop_on_first_trigger=False
           )
        if diseaseActions.show:
            diseasesRaw.append((disease,diseaseActions.correctSyndromes))
    for rawDis in sorted(diseasesRaw,key= lambda element:element[1],reverse=True):
        diseases.append(rawDis[0])
    
    return HttpResponse(template.render({'diseases':diseases,'user':request.user}))
#ALERGY DETECTION
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.run_rules')
def alergyDetection(request):
    meds = []
    medicines = request.GET.get('medicines').split(',')
    for medicine in medicines:
        meds.append(Medicine.objects.get(id=int(medicine)))
    patientId = int(request.GET.get('patient'))
    patient = Patient.objects.get(id=patientId)
    rules = Rule.objects.filter(ruletype=Rule.alergyRule).order_by('-priority')
    engRules = []
    result = False
    for rule in rules:
        engRules.append(json.loads(rule.content))
    for medicine in meds:
        alergyActions = AlergyActions()
        run_all(rule_list=engRules,
        defined_variables=AlergyVariables(patient,medicine),
        defined_actions=alergyActions,
        stop_on_first_trigger=True
        )
        if alergyActions.alarm:
            result = True
            break
    data = {"alarm":result}
    return HttpResponse(json.dumps(data), content_type="application/json")
#DEASES FINDINGS
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.run_rules')
def diseaseFinder(request):
    patient = Patient.objects.get(id=int(request.GET.get('patient')))
    highTmp = bool(request.GET.get("hadTemp"))
    if highTmp==False:
        tmp = 36
    else:
        tmp = request.GET.get("temp")
        if tmp == "":
            tmp = 36
        else:
            print(tmp)
            tmp = int(tmp)
    diagnosis = Diagnosis.objects.create(doctor=request.user,patient=patient,temp=tmp,highTemp=bool(highTmp))
    symptoms = request.GET.get('symptoms').split(',')
    for synid in symptoms:
        if synid !="":
            diagnosis.symptoms.add(Symptom.objects.get(id=int(synid)))
    diagnosis.save()
    helper = RezonerHelper()

    rulesId = request.GET.get('rules')
    if rulesId != None:
        rulesId = rulesId.split(',')
    else:
        return HttpResponse(json.dumps({"disease":"None","probability":'N/A'}), content_type="application/json")
    rules = Rule.objects.filter(ruletype=Rule.diseaseRule).order_by('-priority')
    engRules = []
    for rule in rules:
        if str(rule.id) in rulesId:
            engRules.append(json.loads(rule.content))
    
    my_file = Path("./diagnostics/custom_variables_d.py")
    if my_file.is_file():
        module = import_module('.custom_variables_d',package="diagnostics")
        for disease in Disease.objects.all():
            diseaseVariables = module.CustomDiseaseVariables(diagnosis,disease,helper)
            diseaseActions = DiseaseActions(helper,diseaseVariables)
            run_all(rule_list=engRules,
                defined_variables=diseaseVariables,
                defined_actions=diseaseActions,
                stop_on_first_trigger=False
            )
    else:
        for disease in Disease.objects.all():
            diseaseVariables = DiseaseVariables(diagnosis,disease,helper)
            diseaseActions = DiseaseActions(helper,diseaseVariables)
            run_all(rule_list=engRules,
                defined_variables=diseaseVariables,
                defined_actions=diseaseActions,
                stop_on_first_trigger=False
            )
    result = {}
    result['disease'] = helper.diseaseName
    result['probability'] = helper.bestPercent
    diagnosis.delete()
    return HttpResponse(json.dumps(result), content_type="application/json")

#Diagnose
@csrf_exempt
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.run_rules')
def diagnoze(request):
    patient = Patient.objects.get(id=int(request.POST.get('patient')))
    disease = Disease.objects.get(id=int(request.POST.get('disease')))
    highTmp = bool(request.POST.get("hadTemp"))
    tmp = 0
    if highTmp==False:
        tmp = 36
    else:
        tmp = request.GET.get("temp")
        if tmp == "":
            tmp = 36
        else:
            print(tmp)
            tmp = int(tmp)
    diagnosis = Diagnosis.objects.create(doctor=request.user,patient=patient,temp=tmp,highTemp=highTmp,disease=disease)
    symptoms = request.POST.get('symptoms').split(',')
    for synid in symptoms:
        if synid != "":
            diagnosis.symptoms.add(Symptom.objects.get(id=int(synid)))
    medicines = request.POST.get('medicines').split(',')
    for med in medicines:
        if med != "":
            diagnosis.medicine.add(Medicine.objects.get(id=int(med)))
    diagnosis.save()
    return redirect('/diagnostics/diagnose/')
#Diagnosis page
@login_required(login_url="/diagnostics/loginPage/")
@permission_required('diagnostics.run_rules')
def diagnosisPage(request):
    template = loader.get_template("diagnosisPage.html")
    symptoms = Symptom.objects.filter(technical=False)
    diseases = Disease.objects.all()
    medicines = Medicine.objects.all()
    patients = Patient.objects.all()
    rules = Rule.objects.filter(ruletype=Rule.diseaseRule)
    return HttpResponse(template.render({'rules':rules,'medicines':medicines,'symptoms':symptoms,'diseases':diseases,'patients':patients,'user':request.user}))
#Patient
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def patientsP(request):
    template = loader.get_template("patientsPage.html")
    patients = Patient.objects.all()
    return HttpResponse(template.render({'patients':patients,'user':request.user}))
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
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
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
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
        if ingredient_id !="":
            ingred = Ingredient.objects.get(id=ingredient_id)
            patient.alergying.add(ingred)
    for medicine_id in medicines.split(","):
        if medicine_id !="":
            medicine = Medicine.objects.get(id=medicine_id)
            patient.alergymed.add(medicine)
    patient.save()
    return redirect('/diagnostics/patients/')
    
@csrf_exempt
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def newPatient(request):
    patient = Patient.objects.create()
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    ingredients = request.POST.get('ingredients')
    medicines = request.POST.get('medicines')
    patient.name = name
    patient.surname = surname
    for ingredient_id in ingredients.split(","):
        if ingredient_id !="":
            ingred = Ingredient.objects.get(id=eval(ingredient_id))
            patient.alergying.add(ingred)
    for medicine_id in medicines.split(","):
        if medicine_id !="":
            medicine = Medicine.objects.get(id=eval(medicine_id))
            patient.alergymed.add(medicine)
    patient.save()
    return redirect('/diagnostics/patients/')

#Ingredient
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def ingredientsP(request):
    template = loader.get_template("ingredientsPage.html")
    ingredients = Ingredient.objects.all()
    return HttpResponse(template.render({'ingredients':ingredients,'user':request.user}))
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def createIngredientPage(request):
    template = loader.get_template("createIngredientPage.html")
    return HttpResponse(template.render({'user':request.user}))
@csrf_exempt
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def newIngredient(request):
    if len(Ingredient.objects.filter(name=request.POST.get('name')))==0:
        ingredient = Ingredient.objects.create()
        name = request.POST.get('name')
        ingredient.name = name
        ingredient.save()
    return redirect('/diagnostics/ingredients/')
    
#Medicine
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def medicinesP(request):
    template = loader.get_template("medicinesPage.html")
    medicines = Medicine.objects.all()
    dt = dict(Medicine.Type_CHOICES)
    return HttpResponse(template.render({'medicines':medicines,'user':request.user, 'dict':dt}))

@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def editMedicineP(request,id):
    template = loader.get_template("createMedicinePage.html")
    ingredients = Ingredient.objects.all()
    dt = list(Medicine.Type_CHOICES)
    if id=="None":
        return HttpResponse(template.render({'new':True,'user':request.user,'ingredients':ingredients,'choice':dt}))
    else:
        medicine = Medicine.objects.get(id=id)
        return HttpResponse(template.render({'new':False,'medicine':medicine,'user':request.user,'ingredients':ingredients,'oldingredients':medicine.ingredient.all(),'choice':dt}))
@csrf_exempt
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def editMedicine(request,medicine_id):
    try:
        medicine = Medicine.objects.get(id=medicine_id)
        name = request.POST.get('name')
        ingredients = request.POST.get('ingredients')
        medType = request.POST.get('type')
        medicine.name = name
        medicine.medtype = medType
        medicine.ingredient.clear()
        for ing_id in ingredients.split(","):
            if ing_id!="":
                ing = Ingredient.objects.get(id=ing_id)
                medicine.ingredient.add(ing)
        medicine.save()
        return redirect('/diagnostics/medicines/')
    except IntegrityError:
        return redirect('/diagnostics/medicines/')
    
@csrf_exempt
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def newMedicine(request):
    if len(Medicine.objects.filter(name=request.POST.get('name')))==0:
        medicine = Medicine.objects.create()
        name = request.POST.get('name')
        ingredients = request.POST.get('ingredients')
        medType = request.POST.get('type')
        medicine.name = name
        medicine.medtype = medType
        for ing_id in ingredients.split(","):
            if ing_id!="":
                ing = Ingredient.objects.get(id=ing_id)
                medicine.ingredient.add(ing)
        medicine.save()
    return redirect('/diagnostics/medicines/')
#Symptom
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def syndromesP(request):
    template = loader.get_template("syndromesPage.html")
    symptoms = Symptom.objects.all()
    return HttpResponse(template.render({'symptoms':symptoms,'user':request.user}))
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def createSyndromePage(request):
    template = loader.get_template("createSyndromePage.html")
    return HttpResponse(template.render({'user':request.user}))

@csrf_exempt
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def newSyndrome(request):
    if len(Symptom.objects.filter(name=request.POST.get('name')))==0:
        symptom = Symptom.objects.create(technical = bool(request.POST.get('technical')),name = request.POST.get('name'))
        symptom.save()
    return redirect('/diagnostics/symptoms/')
#Disease
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def diseasesP(request):
    template = loader.get_template("diseasesPage.html")
    diseases = Disease.objects.all()
    return HttpResponse(template.render({'diseases':diseases,'user':request.user}))
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def editDiseasesP(request,id):
    template = loader.get_template("createDiseasePage.html")
    symptoms = Symptom.objects.all()
    if id=="None":
        return HttpResponse(template.render({'new':True,'user':request.user,'symptoms':symptoms}))
    else:
        disease = Disease.objects.get(id=id)
        return HttpResponse(template.render({'new':False,'disease':disease,'user':request.user,'symptoms':symptoms,'strongsynd':disease.strongsympt.all(),'regularsynd':disease.regularsympt.all()}))
@csrf_exempt
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def editDisease(request,disease_id):
    try:
        disease = Disease.objects.get(id=disease_id)
        name = request.POST.get('name')
        regSyn = request.POST.get('regSynd')
        strSyn = request.POST.get('strSynd')
        disease.name = name
        disease.strongsympt.clear()
        disease.regularsympt.clear()
        for syn_id in regSyn.split(","):
            if syn_id != "":
                symptom = Symptom.objects.get(id=syn_id)
                disease.regularsympt.add(symptom)
        for syn_id in strSyn.split(","):
            if syn_id != "":
                symptom = Symptom.objects.get(id=syn_id)
                disease.strongsympt.add(symptom)
        disease.save()
        return redirect('/diagnostics/diseases/')
    except IntegrityError:
        return redirect('/diagnostics/diseases/')
    
@csrf_exempt
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def newDisease(request):
    if len(Disease.objects.filter(name = request.POST.get('name')))==0:
        disease = Disease.objects.create(name = request.POST.get('name'))
        regSyn = request.POST.get('regSynd')
        strSyn = request.POST.get('strSynd')
        for syn_id in regSyn.split(","):
            if syn_id != "":
                symptom = Symptom.objects.get(id=syn_id)
                disease.regularsympt.add(symptom)
        for syn_id in strSyn.split(","):
            if syn_id != "":
                symptom = Symptom.objects.get(id=syn_id)
                disease.strongsympt.add(symptom)
        disease.save()
    return redirect('/diagnostics/diseases/')
#RuleExtentions
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def ruleextsP(request):
    template = loader.get_template("ruleExtPage.html")
    fileRules = FileRule.objects.all()
    dt = dict(FileRule.Rule_CHOICES)
    return HttpResponse(template.render({'fileRules':fileRules,'user':request.user, 'dict':dt}))
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def createRuleextPage(request):
    template = loader.get_template("createRuleExtPage.html")
    dt = list(FileRule.Rule_CHOICES)
    return HttpResponse(template.render({'user':request.user,'rule':dt}))
@csrf_exempt
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
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
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def rulesP(request):
    template = loader.get_template("rulesPage.html")
    rules = Rule.objects.all()
    dt = dict(Rule.Type_CHOICES)
    return HttpResponse(template.render({'rules':rules,'user':request.user, 'dict':dt}))
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def editRuleP(request,id):
    template = loader.get_template("createRulePage.html")
    if id=="None":
        return HttpResponse(template.render({'dict':list(Rule.Type_CHOICES),'user':request.user}))

@csrf_exempt
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def newRule(request):
    title = request.POST.get('title')
    rtype = request.POST.get('type')
    content = request.POST.get('content')
    try:
        priority = int(request.POST.get('priority'))
    except:
        return redirect('/diagnostics/rules/')
    rule = Rule.objects.create(priority=priority)
    rule.title = title
    rule.ruletype = rtype
    rule.content = content
    rule.save()
    return redirect('/diagnostics/rules/')
@csrf_exempt
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def deleteRule(request,ruleset_id):
    rule = Rule.objects.get(id=ruleset_id)
    rule.delete()
    return redirect('/diagnostics/rules/')
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def ruleHelpDdmr(request):
    my_file = Path("./diagnostics/custom_variables_d.py")
    if my_file.is_file():
        module = import_module('.custom_variables_d',package="diagnostics")
        data = export_rule_data(module.CustomDiseaseVariables, DiseaseActions)
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data = export_rule_data(DiseaseVariables, DiseaseActions)
        return HttpResponse(json.dumps(data), content_type="application/json")
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def ruleHelpPadr(request):
    data = export_rule_data(AlergyVariables, AlergyActions)
    return HttpResponse(json.dumps(data), content_type="application/json")
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def ruleHelpFdsr(request):
    data = export_rule_data(SyndromeVariables, SyndromeActions)
    return HttpResponse(json.dumps(data), content_type="application/json")
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def ruleHelpDdbosr(request):
    data = export_rule_data(DiseasesVariables, DiseasesActions)
    return HttpResponse(json.dumps(data), content_type="application/json")
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
def ruleHelpMar(request):
    my_file = Path("./monitoring/custom_variables_m.py")
    if my_file.is_file():
        module = import_module('.custom_variables_m',package="monitoring")
        data = export_rule_data(module.CustomMonitoringVariables, MonitoringActions)
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        data = export_rule_data(MonitoringVariables, MonitoringActions)
        return HttpResponse(json.dumps(data), content_type="application/json")
@login_required(login_url="/diagnostics/loginPage")
@permission_required('diagnostics.manage_rules')
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
        if user.has_perm('diagnostics.manage_rules'):
            return redirect('patientsPage')
        else:
            return redirect('diagnosePage')
    else:
        return redirect('loginP')

@login_required(login_url="/diagnostics/loginPage/")
def logoutF(request):#TOTALY DONE
    logout(request)
    return redirect('loginP')

def loginP(request):#TOTALY DONE
    template = loader.get_template("static/login.html")
    return HttpResponse(template.render())
#added
@login_required(login_url="/diagnostics/loginPage/")
@permission_required('diagnostics.run_rules')
def symPickPage(request):
    template = loader.get_template("diseaseSyndromePick.html")
    symptoms = Symptom.objects.all()
    return HttpResponse(template.render({'user':request.user,'symptoms':symptoms}))
@login_required(login_url="/diagnostics/loginPage/")
@permission_required('diagnostics.manage_rules')
def rulesPickPage(request):
    template = loader.get_template("rulesPickPage.html")
    return HttpResponse(template.render({'dict':list(Rule.Type_CHOICES),'user':request.user}))
@login_required(login_url="/diagnostics/loginPage/")
@permission_required('diagnostics.manage_rules')
def rulesAllPage(request):
    ruletype = request.GET.get("type")
    rules = Rule.objects.filter(ruletype=int(ruletype)).order_by('-priority')
    result = []
    for rule in rules:
        result.append(json.loads(rule.content))
    return HttpResponse(json.dumps(result), content_type="application/json")

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