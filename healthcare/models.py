from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import datetime, timedelta

# Base Models (existing)
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['specialization']),
            models.Index(fields=['is_available']),
        ]

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"

    @property
    def total_patients(self):
        """Get total number of patients treated"""
        return self.appointments.filter(status='completed').count()

    def get_today_appointments(self):
        """Get today's appointments"""
        today = timezone.now().date()
        return self.appointments.filter(
            appointment_date__date=today,
            status__in=['scheduled', 'in_progress']
        ).order_by('appointment_date')

class Patient(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    address = models.TextField()
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    blood_type = models.CharField(max_length=3, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ], blank=True)
    allergies = models.TextField(blank=True, help_text="List of known allergies")
    medical_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return f"{self.name} - {self.email}"

    @property
    def age(self):
        """Calculate age from date of birth"""
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    def get_recent_appointments(self, limit=5):
        """Get recent appointments"""
        return self.appointments.order_by('-appointment_date')[:limit]

class Nurse(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True)
    shift_type = models.CharField(max_length=20, choices=[
        ('morning', 'Morning (6AM-2PM)'),
        ('evening', 'Evening (2PM-10PM)'),
        ('night', 'Night (10PM-6AM)'),
        ('rotating', 'Rotating Shifts')
    ], default='morning')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nurse {self.name}"

class Admin(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=50, default="Administrator")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin {self.name}"

class Pharmacist(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pharmacist {self.name}"

class DrugSupplier(models.Model):
    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    address = models.TextField()
    license_number = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class LabTechnician(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    license_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, help_text="e.g., Hematology, Biochemistry")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lab Tech {self.name}"

# New Models for Week 2

class Medicine(models.Model):
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    manufacturer = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    dosage_form = models.CharField(max_length=50, choices=[
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('cream', 'Cream'),
        ('drops', 'Drops'),
        ('inhaler', 'Inhaler'),
        ('ointment', 'Ointment'),
    ])
    strength = models.CharField(max_length=50, help_text="e.g., 500mg, 10ml")
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    minimum_stock_level = models.PositiveIntegerField(default=10)
    expiry_date = models.DateField()
    supplier = models.ForeignKey(DrugSupplier, on_delete=models.CASCADE, related_name='medicines')
    requires_prescription = models.BooleanField(default=True)
    side_effects = models.TextField(blank=True)
    contraindications = models.TextField(blank=True)
    storage_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['generic_name']),
            models.Index(fields=['expiry_date']),
            models.Index(fields=['stock_quantity']),
        ]

    def __str__(self):
        return f"{self.name} - {self.strength}"

    @property
    def is_low_stock(self):
        """Check if medicine is low on stock"""
        return self.stock_quantity <= self.minimum_stock_level

    @property
    def is_expired(self):
        """Check if medicine is expired"""
        return self.expiry_date < timezone.now().date()

    @property
    def days_to_expire(self):
        """Days until expiry"""
        if self.expiry_date:
            return (self.expiry_date - timezone.now().date()).days
        return None

class Appointment(models.Model):
    APPOINTMENT_STATUS = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    APPOINTMENT_TYPE = [
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('emergency', 'Emergency'),
        ('routine_checkup', 'Routine Checkup'),
        ('surgery', 'Surgery'),
        ('lab_test', 'Lab Test'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE, default='consultation')
    status = models.CharField(max_length=20, choices=APPOINTMENT_STATUS, default='scheduled')
    duration_minutes = models.PositiveIntegerField(default=30)
    chief_complaint = models.TextField(blank=True, help_text="Main reason for visit")
    notes = models.TextField(blank=True, help_text="Doctor's notes")
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    nurse_assigned = models.ForeignKey(Nurse, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date']
        indexes = [
            models.Index(fields=['appointment_date']),
            models.Index(fields=['status']),
            models.Index(fields=['patient', 'appointment_date']),
            models.Index(fields=['doctor', 'appointment_date']),
        ]

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} - {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"

    def clean(self):
        """Custom validation"""
        from django.core.exceptions import ValidationError
        
        # Check if appointment is in the future (for new appointments)
        if not self.pk and self.appointment_date <= timezone.now():
            raise ValidationError("Appointment must be scheduled for future time")
        
        # Check doctor availability
        if self.doctor and not self.doctor.is_available:
            raise ValidationError("Doctor is not available")

    @property
    def is_today(self):
        """Check if appointment is today"""
        return self.appointment_date.date() == timezone.now().date()

    @property
    def is_upcoming(self):
        """Check if appointment is upcoming"""
        return self.appointment_date > timezone.now() and self.status == 'scheduled'

    def can_be_cancelled(self):
        """Check if appointment can be cancelled"""
        # Can cancel if it's more than 2 hours away and not completed
        time_diff = self.appointment_date - timezone.now()
        return time_diff.total_seconds() > 7200 and self.status not in ['completed', 'cancelled']

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='medical_records')
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, null=True, blank=True, related_name='medical_record')
    
    # Vital Signs
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="°C")
    blood_pressure_systolic = models.PositiveIntegerField(null=True, blank=True)
    blood_pressure_diastolic = models.PositiveIntegerField(null=True, blank=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True, help_text="BPM")
    respiratory_rate = models.PositiveIntegerField(null=True, blank=True, help_text="per minute")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="kg")
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="cm")
    
    # Medical Information
    symptoms = models.TextField(help_text="Patient reported symptoms")
    diagnosis = models.TextField(help_text="Doctor's diagnosis")
    treatment_plan = models.TextField(help_text="Treatment recommendations")
    prescription = models.TextField(blank=True, help_text="Prescribed medications")
    lab_tests_ordered = models.TextField(blank=True, help_text="Lab tests requested")
    follow_up_instructions = models.TextField(blank=True)
    next_appointment_recommended = models.DateField(null=True, blank=True)
    
    # Flags
    is_emergency = models.BooleanField(default=False)
    requires_follow_up = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient', 'created_at']),
            models.Index(fields=['doctor', 'created_at']),
            models.Index(fields=['is_emergency']),
        ]

    def __str__(self):
        return f"Record for {self.patient.name} - {self.created_at.strftime('%Y-%m-%d')}"

    @property
    def bmi(self):
        """Calculate BMI if height and weight are available"""
        if self.height and self.weight:
            height_m = float(self.height) / 100  # Convert cm to meters
            return round(float(self.weight) / (height_m ** 2), 2)
        return None

    @property
    def blood_pressure(self):
        """Get formatted blood pressure"""
        if self.blood_pressure_systolic and self.blood_pressure_diastolic:
            return f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic}"
        return None

class Prescription(models.Model):
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='prescriptions')
    dosage = models.CharField(max_length=100, help_text="e.g., 1 tablet twice daily")
    duration_days = models.PositiveIntegerField(help_text="Duration in days")
    quantity = models.PositiveIntegerField(help_text="Total quantity prescribed")
    instructions = models.TextField(blank=True, help_text="Special instructions")
    is_filled = models.BooleanField(default=False)
    filled_by = models.ForeignKey(Pharmacist, on_delete=models.SET_NULL, null=True, blank=True, related_name='filled_prescriptions')
    filled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.medicine.name} for {self.medical_record.patient.name}"

    def mark_as_filled(self, pharmacist):
        """Mark prescription as filled"""
        self.is_filled = True
        self.filled_by = pharmacist
        self.filled_at = timezone.now()
        self.save()

class LabTest(models.Model):
    TEST_STATUS = [
        ('ordered', 'Ordered'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='lab_tests')
    test_name = models.CharField(max_length=200)
    test_type = models.CharField(max_length=100, choices=[
        ('blood', 'Blood Test'),
        ('urine', 'Urine Test'),
        ('xray', 'X-Ray'),
        ('ct_scan', 'CT Scan'),
        ('mri', 'MRI'),
        ('ultrasound', 'Ultrasound'),
        ('ecg', 'ECG'),
        ('biopsy', 'Biopsy'),
        ('other', 'Other'),
    ])
    status = models.CharField(max_length=20, choices=TEST_STATUS, default='ordered')
    ordered_by = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='ordered_tests')
    assigned_technician = models.ForeignKey(LabTechnician, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tests')
    results = models.TextField(blank=True)
    normal_range = models.CharField(max_length=200, blank=True)
    is_abnormal = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.test_name} for {self.medical_record.patient.name}"

    def mark_completed(self, results, is_abnormal=False):
        """Mark test as completed with results"""
        self.status = 'completed'
        self.results = results
        self.is_abnormal = is_abnormal
        self.completed_date = timezone.now()
        self.save()

# Signal handlers for automatic actions
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Appointment)
def update_appointment_fee(sender, instance, created, **kwargs):
    """Automatically set appointment fee based on doctor's consultation fee"""
    if created and not instance.fee and instance.doctor.consultation_fee:
        instance.fee = instance.doctor.consultation_fee
        instance.save(update_fields=['fee'])

@receiver(post_save, sender=Prescription)
def update_medicine_stock(sender, instance, created, **kwargs):
    """Update medicine stock when prescription is filled"""
    if instance.is_filled and instance.medicine.stock_quantity >= instance.quantity:
        instance.medicine.stock_quantity -= instance.quantity
        instance.medicine.save(update_fields=['stock_quantity'])