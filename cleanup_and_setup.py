#!/usr/bin/env python3
"""
Complete cleanup and setup script for Hospital Management System
This will clean everything and start fresh
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description="", check=True):
    """Run a shell command and print the result"""
    print(f"\n{'='*50}")
    print(f"🔄 {description or command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and not check:
            print(f"Warning: {result.stderr}")
        
        if result.returncode == 0:
            print(f"✅ {description or command} - COMPLETED")
            return True
        else:
            print(f"⚠️  {description or command} - COMPLETED WITH WARNINGS")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def cleanup_project():
    """Clean up existing project files"""
    print("\n🧹 CLEANING UP PROJECT")
    print("=" * 50)
    
    # Files and directories to clean
    cleanup_items = [
        'db.sqlite3',
        'healthcare/migrations/0*.py',
        'healthcare/__pycache__',
        'chatbotAI/__pycache__',
        '__pycache__',
        '*.pyc',
        'logs/*',
        'staticfiles/*'
    ]
    
    for item in cleanup_items:
        if '*' in item:
            # Handle wildcard patterns
            import glob
            for path in glob.glob(item):
                try:
                    if os.path.isfile(path):
                        os.remove(path)
                        print(f"🗑️  Removed file: {path}")
                    elif os.path.isdir(path):
                        shutil.rmtree(path)
                        print(f"🗑️  Removed directory: {path}")
                except Exception as e:
                    print(f"⚠️  Could not remove {path}: {e}")
        else:
            try:
                if os.path.exists(item):
                    if os.path.isfile(item):
                        os.remove(item)
                        print(f"🗑️  Removed file: {item}")
                    elif os.path.isdir(item):
                        shutil.rmtree(item)
                        print(f"🗑️  Removed directory: {item}")
            except Exception as e:
                print(f"⚠️  Could not remove {item}: {e}")

def create_basic_structure():
    """Create basic project structure"""
    print("\n📁 CREATING BASIC STRUCTURE")
    print("=" * 50)
    
    directories = [
        'healthcare/management',
        'healthcare/management/commands',
        'healthcare/migrations',
        'logs',
        'media',
        'static',
        'staticfiles',
        'templates'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created: {directory}")
    
    # Create __init__.py files
    init_files = [
        'healthcare/management/__init__.py',
        'healthcare/management/commands/__init__.py'
    ]
    
    for init_file in init_files:
        with open(init_file, 'w') as f:
            f.write('# This file makes Python treat the directory as a package\n')
        print(f"📄 Created: {init_file}")

def create_minimal_models():
    """Create minimal models.py"""
    print("\n📄 Creating minimal models.py...")
    
    minimal_models = '''from django.db import models
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
'''
    
    with open('healthcare/models.py', 'w') as f:
        f.write(minimal_models)

def create_minimal_serializers():
    """Create minimal serializers.py"""
    print("\n📄 Creating minimal serializers.py...")
    
    minimal_serializers = '''from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Doctor, Patient, Nurse, Admin, Pharmacist, DrugSupplier, LabTechnician

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
'''
    
    with open('healthcare/serializers.py', 'w') as f:
        f.write(minimal_serializers)

def create_minimal_views():
    """Create minimal views.py"""
    print("\n📄 Creating minimal views.py...")
    
    minimal_views = '''from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate

from .models import Doctor, Patient, Nurse, Admin, Pharmacist, DrugSupplier, LabTechnician
from .serializers import (
    UserRegisterSerializer, DoctorSerializer, PatientSerializer, NurseSerializer,
    AdminSerializer, PharmacistSerializer, DrugSupplierSerializer, LabTechnicianSerializer
)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully',
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({
                'message': 'Login successful',
                'user_id': user.id
            }, status=status.HTTP_200_OK)
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

class NurseViewSet(viewsets.ModelViewSet):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer
    permission_classes = [IsAuthenticated]

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated]

class PharmacistViewSet(viewsets.ModelViewSet):
    queryset = Pharmacist.objects.all()
    serializer_class = PharmacistSerializer
    permission_classes = [IsAuthenticated]

class DrugSupplierViewSet(viewsets.ModelViewSet):
    queryset = DrugSupplier.objects.all()
    serializer_class = DrugSupplierSerializer
    permission_classes = [IsAuthenticated]

class LabTechnicianViewSet(viewsets.ModelViewSet):
    queryset = LabTechnician.objects.all()
    serializer_class = LabTechnicianSerializer
    permission_classes = [IsAuthenticated]

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        stats = {
            'total_doctors': Doctor.objects.count(),
            'total_patients': Patient.objects.count(),
            'total_nurses': Nurse.objects.count(),
            'total_pharmacists': Pharmacist.objects.count(),
            'total_lab_technicians': LabTechnician.objects.count(),
            'total_drug_suppliers': DrugSupplier.objects.count(),
        }
        return Response(stats)
'''
    
    with open('healthcare/views.py', 'w') as f:
        f.write(minimal_views)

def create_minimal_urls():
    """Create minimal urls.py"""
    print("\n📄 Creating minimal urls.py...")
    
    minimal_urls = '''from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView, LoginView, DashboardStatsView,
    DoctorViewSet, PatientViewSet, NurseViewSet, 
    AdminViewSet, PharmacistViewSet, DrugSupplierViewSet, 
    LabTechnicianViewSet
)

# Create router and register ViewSets
router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'nurses', NurseViewSet, basename='nurse')
router.register(r'admins', AdminViewSet, basename='admin')
router.register(r'pharmacists', PharmacistViewSet, basename='pharmacist')
router.register(r'drug-suppliers', DrugSupplierViewSet, basename='drugsupplier')
router.register(r'lab-technicians', LabTechnicianViewSet, basename='labtechnician')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Dashboard
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
    
    # API endpoints from router
    path('', include(router.urls)),
]
'''
    
    with open('healthcare/urls.py', 'w') as f:
        f.write(minimal_urls)

def create_setup_data_command():
    """Create management command for initial data"""
    print("\n📄 Creating setup data command...")
    
    setup_command = '''from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from healthcare.models import Doctor, Patient, Nurse, Admin, Pharmacist, DrugSupplier, LabTechnician
from datetime import date

class Command(BaseCommand):
    help = 'Setup initial data for the hospital management system'

    def handle(self, *args, **options):
        self.stdout.write('Creating initial data...')

        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@hospital.com',
                password='admin123',
                first_name='System',
                last_name='Administrator'
            )
            self.stdout.write('✅ Superuser created: admin/admin123')

        # Create sample doctors
        doctors_data = [
            {
                'name': 'Dr. Nguyễn Văn Nam',
                'specialization': 'Cardiology',
                'phone': '+84-123-456-789',
                'email': 'nam.nguyen@hospital.com'
            },
            {
                'name': 'Dr. Trần Thị Mai',
                'specialization': 'Pediatrics',
                'phone': '+84-123-456-790',
                'email': 'mai.tran@hospital.com'
            }
        ]

        for doctor_data in doctors_data:
            doctor, created = Doctor.objects.get_or_create(
                email=doctor_data['email'],
                defaults=doctor_data
            )
            if created:
                self.stdout.write(f'✅ Created doctor: {doctor.name}')

        # Create sample patients
        patients_data = [
            {
                'name': 'Nguyễn Văn An',
                'date_of_birth': date(1985, 3, 15),
                'phone': '+84-987-654-321',
                'email': 'an.nguyen@email.com',
                'address': '123 Đường ABC, Quận 1, TP.HCM'
            },
            {
                'name': 'Trần Thị Bình',
                'date_of_birth': date(1990, 7, 22),
                'phone': '+84-987-654-322',
                'email': 'binh.tran@email.com',
                'address': '456 Đường XYZ, Quận 2, TP.HCM'
            }
        ]

        for patient_data in patients_data:
            patient, created = Patient.objects.get_or_create(
                email=patient_data['email'],
                defaults=patient_data
            )
            if created:
                self.stdout.write(f'✅ Created patient: {patient.name}')

        # Create other staff
        Nurse.objects.get_or_create(
            email='nurse@hospital.com',
            defaults={'name': 'Y tá Nguyễn Thị Lan', 'phone': '+84-111-222-333'}
        )

        Pharmacist.objects.get_or_create(
            email='pharmacist@hospital.com',
            defaults={'name': 'Dược sĩ Lê Thị Hương', 'phone': '+84-222-333-444'}
        )

        LabTechnician.objects.get_or_create(
            email='labtech@hospital.com',
            defaults={'name': 'KTV Phạm Văn Đức', 'phone': '+84-333-444-555'}
        )

        DrugSupplier.objects.get_or_create(
            email='supplier@company.com',
            defaults={
                'name': 'Công ty Dược phẩm ABC',
                'contact_person': 'Nguyễn Văn Kinh',
                'phone': '+84-444-555-666',
                'address': '100 Đường Công nghiệp, Quận 9, TP.HCM'
            }
        )

        Admin.objects.get_or_create(
            email='admin.staff@hospital.com',
            defaults={'name': 'Quản trị viên Lê Văn Quản', 'phone': '+84-555-666-777'}
        )

        self.stdout.write(
            self.style.SUCCESS('🎉 Initial data setup completed successfully!')
        )
'''
    
    with open('healthcare/management/commands/setup_initial_data.py', 'w') as f:
        f.write(setup_command)

def main():
    """Main cleanup and setup function"""
    print("🏥 HOSPITAL MANAGEMENT SYSTEM - COMPLETE CLEANUP & SETUP")
    print("=" * 70)
    print("This will clean everything and start with a minimal working system")
    print("=" * 70)
    
    if not os.path.exists('manage.py'):
        print("❌ ERROR: manage.py not found. Please run from Django project root.")
        sys.exit(1)
    
    response = input("\n⚠️  This will DELETE all existing data. Continue? (y/N): ")
    if response.lower() != 'y':
        print("❌ Cancelled by user")
        sys.exit(1)
    
    try:
        # Step 1: Cleanup
        cleanup_project()
        
        # Step 2: Create structure
        create_basic_structure()
        
        # Step 3: Create minimal files
        create_minimal_models()
        create_minimal_serializers()
        create_minimal_views()
        create_minimal_urls()
        create_setup_data_command()
        
        # Step 4: Database setup
        print("\n🗄️  SETTING UP DATABASE")
        print("=" * 50)
        
        run_command("python manage.py makemigrations healthcare", "Creating migrations")
        run_command("python manage.py migrate", "Applying migrations")
        run_command("python manage.py setup_initial_data", "Creating initial data")
        
        print("\n" + "=" * 70)
        print("🎉 CLEANUP AND SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        
        print("\n🚀 NEXT STEPS:")
        print("1. Start the server:")
        print("   python manage.py runserver")
        
        print("\n2. Access the application:")
        print("   🌐 API Root:      http://127.0.0.1:8000/api/healthcare/")
        print("   📊 Dashboard:     http://127.0.0.1:8000/api/healthcare/dashboard/stats/")
        print("   🔧 Admin Panel:   http://127.0.0.1:8000/admin/")
        
        print("\n🔑 LOGIN CREDENTIALS:")
        print("   Username: admin")
        print("   Password: admin123")
        
        print("\n🧪 TEST API:")
        print("   # Get JWT token")
        print("   curl -X POST http://127.0.0.1:8000/api/healthcare/auth/login/ \\")
        print("     -H 'Content-Type: application/json' \\")
        print("     -d '{\"username\":\"admin\",\"password\":\"admin123\"}'")
        
        print("\n✅ The system is now clean and ready to use!")
        
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()