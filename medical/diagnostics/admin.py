from django.contrib import admin
from .models import Disease,Diagnosis,Syndrome,Patient,Medicine,Ingredient,Rule,MonitoringInfo,FileRule
# Register your models here.
admin.site.register(Syndrome)
admin.site.register(Disease)
admin.site.register(Medicine)
admin.site.register(Ingredient)
admin.site.register(Patient)
admin.site.register(Rule)
admin.site.register(MonitoringInfo)
admin.site.register(FileRule)
admin.site.register(Diagnosis)

admin.site.site_header = "SBNZ-Medical"
admin.site.site_title = "SBNZ-Medical"
admin.site.index_title = "SBNZ-Medical"