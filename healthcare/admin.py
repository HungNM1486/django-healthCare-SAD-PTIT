from django.contrib import admin
from .models import Doctor, Patient, Nurse, Admin, Pharmacist, DrugSupplier, LabTechnician

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Nurse)
admin.site.register(Admin)
admin.site.register(Pharmacist)
admin.site.register(DrugSupplier)
admin.site.register(LabTechnician)
