from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Doctor, Patient, Nurse, Admin, Pharmacist, DrugSupplier, LabTechnician,
    Medication, Appointment, PatientRecord, Prescription, Visit, LabResult
)

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
    class Meta:
        model = Doctor
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = Patient
        fields = '__all__'

class NurseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nurse
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class PharmacistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacist
        fields = '__all__'

class DrugSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugSupplier
        fields = '__all__'

class LabTechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTechnician
        fields = '__all__'

class MedicationSerializer(serializers.ModelSerializer):
    supplier_name = serializers.ReadOnlyField(source='supplier.name')
    stock_status = serializers.ReadOnlyField()
    
    class Meta:
        model = Medication
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.name')
    doctor_name = serializers.ReadOnlyField(source='doctor.name')
    
    class Meta:
        model = Appointment
        fields = '__all__'

class PatientRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.name')
    doctor_name = serializers.ReadOnlyField(source='doctor.name')
    
    class Meta:
        model = PatientRecord
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.name')
    doctor_name = serializers.ReadOnlyField(source='doctor.name')
    medication_name = serializers.ReadOnlyField(source='medication.name')
    status = serializers.ReadOnlyField()
    
    class Meta:
        model = Prescription
        fields = '__all__'

class VisitSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.name')
    doctor_name = serializers.ReadOnlyField(source='doctor.name')
    
    class Meta:
        model = Visit
        fields = '__all__'

class LabResultSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.name')
    doctor_name = serializers.ReadOnlyField(source='doctor.name')
    technician_name = serializers.ReadOnlyField(source='technician.name')
    
    class Meta:
        model = LabResult
        fields = '__all__'
