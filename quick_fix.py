#!/usr/bin/env python3
"""
Quick fix script for common Django errors
Run this if you encounter import or circular import errors
"""

import os
import sys

def fix_pagination_import():
    """Fix pagination circular import issue"""
    print("🔧 Fixing pagination import issue...")
    
    # Create pagination.py file
    pagination_content = '''from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination for most API endpoints"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'page_size': self.page_size,
            'results': data
        })

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 200
'''
    
    with open('healthcare/pagination.py', 'w') as f:
        f.write(pagination_content)
    
    print("✅ Created healthcare/pagination.py")

def fix_settings_pagination():
    """Fix settings.py pagination reference"""
    print("🔧 Fixing settings.py pagination reference...")
    
    if not os.path.exists('chatbotAI/settings.py'):
        print("❌ settings.py not found")
        return
    
    with open('chatbotAI/settings.py', 'r') as f:
        content = f.read()
    
    # Fix pagination class reference
    content = content.replace(
        "'DEFAULT_PAGINATION_CLASS': 'healthcare.views.StandardResultsSetPagination',",
        "'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',"
    )
    
    with open('chatbotAI/settings.py', 'w') as f:
        f.write(content)
    
    print("✅ Fixed settings.py pagination reference")

def fix_views_imports():
    """Fix views.py imports"""
    print("🔧 Fixing views.py imports...")
    
    if not os.path.exists('healthcare/views.py'):
        print("❌ views.py not found")
        return
    
    with open('healthcare/views.py', 'r') as f:
        content = f.read()
    
    # Add missing imports
    if 'from django.db.models import Q, Count, Sum, Avg, F' not in content:
        content = content.replace(
            'from django.db.models import Q, Count, Sum, Avg',
            'from django.db.models import Q, Count, Sum, Avg, F'
        )
    
    # Fix pagination imports
    if 'from .pagination import' not in content:
        content = content.replace(
            'from rest_framework.pagination import PageNumberPagination',
            'from .pagination import StandardResultsSetPagination, LargeResultsSetPagination'
        )
    
    # Remove pagination class definitions from views.py
    lines = content.split('\n')
    filtered_lines = []
    skip_pagination = False
    
    for line in lines:
        if 'class StandardResultsSetPagination' in line or 'class LargeResultsSetPagination' in line:
            skip_pagination = True
            continue
        elif skip_pagination and (line.startswith('class ') or line.startswith('# ')):
            skip_pagination = False
        
        if not skip_pagination:
            filtered_lines.append(line)
    
    content = '\n'.join(filtered_lines)
    
    # Fix models.F references
    content = content.replace('models.F(', 'F(')
    
    with open('healthcare/views.py', 'w') as f:
        f.write(content)
    
    print("✅ Fixed views.py imports and references")

def check_requirements():
    """Check if all required files exist"""
    print("🔍 Checking required files...")
    
    required_files = [
        'manage.py',
        'chatbotAI/settings.py',
        'healthcare/models.py',
        'healthcare/views.py',
        'healthcare/serializers.py',
        'healthcare/urls.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        print("Please ensure all code files from artifacts are in place.")
        return False
    else:
        print("✅ All required files present")
        return True

def create_minimal_views():
    """Create minimal views.py if it doesn't exist"""
    if os.path.exists('healthcare/views.py'):
        return
    
    print("🔧 Creating minimal views.py...")
    
    minimal_views = '''from django.shortcuts import render
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

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
    
    print("✅ Created minimal views.py")

def main():
    print("🏥 Hospital Management System - Quick Fix Script")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ ERROR: manage.py not found. Please run from Django project root.")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        print("⚠️  Some files are missing. Creating minimal versions...")
        create_minimal_views()
    
    # Apply fixes
    fix_pagination_import()
    fix_settings_pagination()
    fix_views_imports()
    
    print("\n" + "=" * 60)
    print("🎉 QUICK FIX COMPLETED!")
    print("=" * 60)
    
    print("\nNext steps:")
    print("1. Try running the server:")
    print("   python manage.py runserver")
    
    print("\n2. If you still get errors, try:")
    print("   python manage.py makemigrations")
    print("   python manage.py migrate")
    
    print("\n3. Create sample data:")
    print("   python manage.py setup_initial_data")
    
    print("\n4. Access the application:")
    print("   http://127.0.0.1:8000/api/healthcare/")

if __name__ == "__main__":
    main()