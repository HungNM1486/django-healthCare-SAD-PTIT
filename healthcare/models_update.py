from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"

class Patient(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

    @property
    def age(self):
        """Calculate age from date of birth"""
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

class Nurse(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nurse {self.name}"

class Admin(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin {self.name}"

class Pharmacist(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pharmacist {self.name}"

class DrugSupplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class LabTechnician(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lab Tech {self.name}"

# New models for the additional functionality

class Medication(models.Model):
    CATEGORY_CHOICES = [
        ('analgesics', 'Analgesics'),
        ('antibiotics', 'Antibiotics'),
        ('antivirals', 'Antivirals'),
        ('cardiovascular', 'Cardiovascular'),
        ('diabetes', 'Diabetes'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    generic_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    reorder_level = models.IntegerField()
    supplier = models.ForeignKey(DrugSupplier, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.generic_name})"
    
    @property
    def stock_status(self):
        if self.stock_quantity <= 0:
            return "Out of Stock"
        elif self.stock_quantity <= self.reorder_level:
            return "Low Stock"
        else:
            return "In Stock"

class Appointment(models.Model):
    TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('examination', 'Examination'),
        ('procedure', 'Procedure'),
        ('emergency', 'Emergency'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    DURATION_CHOICES = [
        ('15', '15 minutes'),
        ('30', '30 minutes'),
        ('45', '45 minutes'),
        ('60', '1 hour'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    appointment_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES, default='30')
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} - {self.appointment_date}"

class PatientRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    record_date = models.DateField(default=timezone.now)
    record_type = models.CharField(max_length=100)  # e.g., "Diagnosis", "Procedure", "Lab Result"
    description = models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    attachments = models.FileField(upload_to='patient_records/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient.name} - {self.record_type} - {self.record_date}"

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient.name} - {self.medication.name}"
    
    @property
    def status(self):
        today = date.today()
        if not self.is_active:
            return "Cancelled"
        if today > self.end_date:
            return "Completed"
        return "Active"

class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    visit_date = models.DateField()
    reason = models.CharField(max_length=200)
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient.name} - {self.visit_date}"

class LabResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_results')
    test_name = models.CharField(max_length=100)
    test_date = models.DateField()
    results = models.TextField()
    technician = models.ForeignKey(LabTechnician, on_delete=models.SET_NULL, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.patient.name} - {self.test_name} - {self.test_date}"
