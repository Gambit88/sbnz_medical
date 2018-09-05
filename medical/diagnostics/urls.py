from django.urls import path, re_path

from . import views


urlpatterns = [
    path('login/',views.loginF,name="login"),
    path('logout/', views.logoutF, name="logout"),
    path('loginPage/', views.loginP, name="loginP"),

    path('patients/',views.patientsP,name="patientsPage"),
    path('patients/create/',views.editPatientsP,{'id':'None'},name="createPatientPage"),
    path('patients/create/<int:id>',views.editPatientsP,name="editPatientPage"),
    path('patients/new/',views.newPatient,name="newPatient"),
    path('patients/edit/<int:patient_id>/',views.editPatient,name="editPatient"),

    path('syndromes/',views.syndromesP,name="syndromesPage"),
    path('syndromes/create/',views.createSyndromePage,name="createSyndromePage"),
    path('syndromes/new/',views.newSyndrome,name="newSyndrome"),

    path('diseases/',views.diseasesP,name="diseasesPage"),
    path('diseases/create/',views.editDiseasesP,{'id':'None'},name="createDiseasePage"),
    path('diseases/create/<int:id>/',views.editDiseasesP,name="editDiseasePage"),
    path('diseases/new/',views.newDisease,name="newDisease"),
    path('diseases/edit/<int:disease_id>/',views.editDisease,name="editDisease"),

    path('ingredients/',views.ingredientsP,name="ingredientsPage"),
    path('ingredients/create/',views.createIngredientPage,name="createIngredientPage"),
    path('ingredients/new/',views.newIngredient,name="newIngredient"),

    path('medicines/',views.medicinesP,name="medicinesPage"),
    path('medicines/create/',views.editMedicineP,{'id':'None'},name="createMedicinePage"),
    path('medicines/create/<int:id>',views.editMedicineP,name="editMedicinePage"),
    path('medicines/new/',views.newMedicine,name="newMedicine"),
    path('medicines/edit/<int:medicine_id>/',views.editMedicine,name="editMedicine"),
    
    path('ruleextensions/',views.ruleextsP,name="ruleextensionsPage"),
    path('ruleextensions/new/',views.something,name="newRuleextension"),
    path('ruleextensions/create/',views.something,name="createRuleextensionPage"),

    path('rules/',views.rulesP,name="rulesPage"),
    path('rules/create/',views.something,name="createRulePage"),
    path('rules/create/<int:ruleset_id>/',views.something,name="editRulePage"),
    path('rules/new/',views.something,name="newRule"),
    path('rules/edit/<int:ruleset_id>/',views.something,name="editRule"),
    path('rules/delete/<int:ruleset_id>/',views.something,name="deleteRule"),

    path('diagnose/',views.something,name="diagnosePage"),
    path('diagnose/autodiagnose/',views.something,name=""),
    path('diagnose/diseases/',views.something,name=""),
    path('diagnose/syndromes/',views.something,name=""),
    path('diagnose/prescribe/',views.something,name=""),

    path('reports/', views.something,name="reportsPage"),
    path('reports/<int:ruleset_id>/', views.something,name=""),

]