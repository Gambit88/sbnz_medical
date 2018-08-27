from django.contrib import admin
from .models import Disease,Syndrome,Patient,Medicine,Ingredient,Rule,MonitoringInfo
# Register your models here.
admin.site.register(Syndrome)
admin.site.register(Disease)
admin.site.register(Medicine)
admin.site.register(Ingredient)
admin.site.register(Patient)
admin.site.register(Rule)
admin.site.register(MonitoringInfo)

admin.site.site_header = "SBNZ-Medical"
admin.site.site_title = "SBNZ-Medical"
admin.site.index_title = "SBNZ-Medical"