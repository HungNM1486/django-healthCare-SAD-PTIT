from django.contrib import admin
from .models import (
    Doctor, Patient, Nurse, Admin, Pharmacist, DrugSupplier, LabTechnician,
    Medication, Appointment, PatientRecord, Prescription, Visit, LabResult
)

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Nurse)
admin.site.register(Admin)
admin.site.register(Pharmacist)
admin.site.register(DrugSupplier)
admin.site.register(LabTechnician)

# Register new models
admin.site.register(Medication)
admin.site.register(Appointment)
admin.site.register(PatientRecord)
admin.site.register(Prescription)
admin.site.register(Visit)
admin.site.register(LabResult)
