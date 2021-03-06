from django.contrib import admin
from .models import Alarm,Disease,Diagnosis,Symptom,Patient,Medicine,Ingredient,Rule,MonitoringInfo,FileRule
# Register your models here.
admin.site.register(Symptom)
admin.site.register(Disease)
admin.site.register(Medicine)
admin.site.register(Ingredient)
admin.site.register(Patient)
admin.site.register(Rule)
admin.site.register(MonitoringInfo)
admin.site.register(FileRule)
admin.site.register(Diagnosis)
admin.site.register(Alarm)

admin.site.site_header = "SBNZ-Medical"
admin.site.site_title = "SBNZ-Medical"
admin.site.index_title = "SBNZ-Medical"