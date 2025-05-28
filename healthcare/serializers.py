from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from .models import (
    Doctor, Patient, Nurse, Admin, Pharmacist, DrugSupplier, LabTechnician,
    Medicine, Appointment, MedicalRecord, Prescription, LabTest
)

# Base Serializers (Updated)
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class DoctorSerializer(serializers.ModelSerializer):
    total_patients = serializers.ReadOnlyField()
    today_appointments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Doctor
        fields = '__all__'
    
    def get_today_appointments_count(self, obj):
        """Get count of today's appointments"""
        return obj.get_today_appointments().count()
    
    def validate_email(self, value):
        """Validate email uniqueness"""
        if self.instance:
            # For updates, exclude current instance
            if Doctor.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Email already exists")
        else:
            # For creates
            if Doctor.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already exists")
        return value
    
    def validate_consultation_fee(self, value):
        """Validate consultation fee"""
        if value < 0:
            raise serializers.ValidationError("Consultation fee cannot be negative")
        return value

class DoctorSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    total_patients = serializers.ReadOnlyField()
    
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'email', 'consultation_fee', 'is_available', 'total_patients']

class PatientSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()
    recent_appointments = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = '__all__'
    
    def get_recent_appointments(self, obj):
        """Get recent appointments summary"""
        recent = obj.get_recent_appointments()
        return [
            {
                'id': apt.id,
                'doctor_name': apt.doctor.name,
                'appointment_date': apt.appointment_date,
                'status': apt.status
            } for apt in recent
        ]
    
    def validate_email(self, value):
        if self.instance:
            if Patient.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Email already exists")
        else:
            if Patient.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already exists")
        return value
    
    def validate_date_of_birth(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Date of birth cannot be in the future")
        return value

class PatientSummarySerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = Patient
        fields = ['id', 'name', 'email', 'phone', 'age', 'blood_type']

# Updated existing serializers
class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = '__all__'
    
    def validate_email(self, value):
        if self.instance:
            if Nurse.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Email already exists")
        else:
            if Nurse.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already exists")
        return value

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class PharmacistSerializer(serializers.ModelSerializer):
    filled_prescriptions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Pharmacist
        fields = '__all__'
    
    def get_filled_prescriptions_count(self, obj):
        return obj.filled_prescriptions.count()

class DrugSupplierSerializer(serializers.ModelSerializer):
    medicines_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DrugSupplier
        fields = '__all__'
    
    def get_medicines_count(self, obj):
        return obj.medicines.count()

class LabTechnicianSerializer(serializers.ModelSerializer):
    assigned_tests_count = serializers.SerializerMethodField()
    
    class Meta:
        model = LabTechnician
        fields = '__all__'
    
    def get_assigned_tests_count(self, obj):
        return obj.assigned_tests.filter(status__in=['ordered', 'in_progress']).count()

# New Model Serializers

class MedicineSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    is_low_stock = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    days_to_expire = serializers.ReadOnlyField()
    
    class Meta:
        model = Medicine
        fields = '__all__'
    
    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative")
        return value
    
    def validate_price_per_unit(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        return value
    
    def validate_expiry_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError("Expiry date must be in the future")
        return value

class MedicineSummarySerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    is_low_stock = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = Medicine
        fields = ['id', 'name', 'strength', 'stock_quantity', 'price_per_unit', 
                 'supplier_name', 'is_low_stock', 'is_expired', 'expiry_date']

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    nurse_name = serializers.CharField(source='nurse_assigned.name', read_only=True)
    is_today = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()
    can_cancel = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = '__all__'
    
    def get_can_cancel(self, obj):
        return obj.can_be_cancelled()
    
    def validate_appointment_date(self, value):
        # For new appointments, must be in future
        if not self.instance and value <= timezone.now():
            raise serializers.ValidationError("Appointment must be scheduled for future time")
        return value
    
    def validate(self, data):
        # Check for doctor availability during appointment time
        doctor = data.get('doctor')
        appointment_date = data.get('appointment_date')
        duration = data.get('duration_minutes', 30)
        
        if doctor and appointment_date:
            # Check for overlapping appointments
            start_time = appointment_date
            end_time = start_time + timedelta(minutes=duration)
            
            overlapping_query = Appointment.objects.filter(
                doctor=doctor,
                appointment_date__lt=end_time,
                appointment_date__gte=start_time - timedelta(minutes=60),  # 1 hour buffer
                status__in=['scheduled', 'confirmed', 'in_progress']
            )
            
            if self.instance:
                overlapping_query = overlapping_query.exclude(pk=self.instance.pk)
            
            if overlapping_query.exists():
                raise serializers.ValidationError(
                    "Doctor has conflicting appointment during this time"
                )
        
        return data

class AppointmentSummarySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'patient_name', 'doctor_name', 'appointment_date', 
                 'appointment_type', 'status', 'chief_complaint']

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    appointment_date = serializers.DateTimeField(source='appointment.appointment_date', read_only=True)
    bmi = serializers.ReadOnlyField()
    blood_pressure = serializers.ReadOnlyField()
    
    class Meta:
        model = MedicalRecord
        fields = '__all__'
    
    def validate_temperature(self, value):
        if value and (value < 30 or value > 50):
            raise serializers.ValidationError("Temperature seems abnormal (30-50°C)")
        return value
    
    def validate_blood_pressure_systolic(self, value):
        if value and (value < 70 or value > 250):
            raise serializers.ValidationError("Systolic pressure seems abnormal (70-250 mmHg)")
        return value
    
    def validate_blood_pressure_diastolic(self, value):
        if value and (value < 40 or value > 150):
            raise serializers.ValidationError("Diastolic pressure seems abnormal (40-150 mmHg)")
        return value

class MedicalRecordSummarySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient_name', 'doctor_name', 'diagnosis', 
                 'created_at', 'is_emergency', 'requires_follow_up']

class PrescriptionSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    patient_name = serializers.CharField(source='medical_record.patient.name', read_only=True)
    pharmacist_name = serializers.CharField(source='filled_by.name', read_only=True)
    
    class Meta:
        model = Prescription
        fields = '__all__'
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero")
        return value
    
    def validate_duration_days(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration must be greater than zero")
        return value
    
    def validate(self, data):
        # Check medicine stock availability
        medicine = data.get('medicine')
        quantity = data.get('quantity')
        
        if medicine and quantity:
            if medicine.stock_quantity < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock. Available: {medicine.stock_quantity}, Required: {quantity}"
                )
        
        return data

class LabTestSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='medical_record.patient.name', read_only=True)
    doctor_name = serializers.CharField(source='ordered_by.name', read_only=True)
    technician_name = serializers.CharField(source='assigned_technician.name', read_only=True)
    
    class Meta:
        model = LabTest
        fields = '__all__'
    
    def validate_scheduled_date(self, value):
        if value and value <= timezone.now():
            raise serializers.ValidationError("Scheduled date must be in the future")
        return value

class LabTestSummarySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='medical_record.patient.name', read_only=True)
    doctor_name = serializers.CharField(source='ordered_by.name', read_only=True)
    
    class Meta:
        model = LabTest
        fields = ['id', 'test_name', 'test_type', 'status', 'patient_name', 
                 'doctor_name', 'scheduled_date', 'is_abnormal']

# Nested Serializers for Complex Views

class PatientDetailSerializer(PatientSerializer):
    """Detailed patient info with related data"""
    recent_medical_records = serializers.SerializerMethodField()
    upcoming_appointments = serializers.SerializerMethodField()
    
    def get_recent_medical_records(self, obj):
        records = obj.medical_records.order_by('-created_at')[:5]
        return MedicalRecordSummarySerializer(records, many=True).data
    
    def get_upcoming_appointments(self, obj):
        upcoming = obj.appointments.filter(
            appointment_date__gt=timezone.now(),
            status__in=['scheduled', 'confirmed']
        ).order_by('appointment_date')[:5]
        return AppointmentSummarySerializer(upcoming, many=True).data

class DoctorDetailSerializer(DoctorSerializer):
    """Detailed doctor info with related data"""
    today_appointments = serializers.SerializerMethodField()
    recent_patients = serializers.SerializerMethodField()
    
    def get_today_appointments(self, obj):
        today_appointments = obj.get_today_appointments()
        return AppointmentSummarySerializer(today_appointments, many=True).data
    
    def get_recent_patients(self, obj):
        # Get unique patients from recent appointments
        recent_appointment_patients = obj.appointments.filter(
            status='completed'
        ).order_by('-appointment_date')[:10].values_list('patient', flat=True)
        
        patients = Patient.objects.filter(
            id__in=recent_appointment_patients
        ).distinct()[:5]
        
        return PatientSummarySerializer(patients, many=True).data

class MedicalRecordDetailSerializer(MedicalRecordSerializer):
    """Detailed medical record with prescriptions and lab tests"""
    prescriptions = PrescriptionSerializer(many=True, read_only=True)
    lab_tests = LabTestSerializer(many=True, read_only=True)

# Bulk Operations Serializers

class BulkAppointmentCreateSerializer(serializers.Serializer):
    """For creating multiple appointments"""
    appointments = AppointmentSerializer(many=True)
    
    def create(self, validated_data):
        appointments_data = validated_data['appointments']
        appointments = []
        for appointment_data in appointments_data:
            appointment = Appointment.objects.create(**appointment_data)
            appointments.append(appointment)
        return appointments

class BulkMedicineStockUpdateSerializer(serializers.Serializer):
    """For bulk updating medicine stock"""
    updates = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField())
    )
    
    def update(self, instance, validated_data):
        updates = validated_data['updates']
        updated_medicines = []
        
        for update in updates:
            medicine_id = update.get('id')
            new_stock = int(update.get('stock_quantity', 0))
            
            try:
                medicine = Medicine.objects.get(id=medicine_id)
                medicine.stock_quantity = new_stock
                medicine.save()
                updated_medicines.append(medicine)
            except Medicine.DoesNotExist:
                continue
        
        return updated_medicines