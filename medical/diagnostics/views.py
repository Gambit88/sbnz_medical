from django.shortcuts import render
from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from django.template.defaulttags import register

from .models import Patient,Ingredient,Medicine,Disease,Syndrome,FileRule,Rule

# Create your views here.

def something(request):
    pass

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
#Rules
def rulesP(request):
    template = loader.get_template("rulesPage.html")
    rules = Rule.objects.all()
    dt = dict(Rule.Type_CHOICES)
    return HttpResponse(template.render({'rules':rules,'user':request.user, 'dict':dt}))





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