from django.shortcuts import render, redirect
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Doctor, Patient, Nurse, Admin, Pharmacist, DrugSupplier, LabTechnician
from .serializers import (
    UserRegisterSerializer, DoctorSerializer, PatientSerializer, NurseSerializer,
    AdminSerializer, PharmacistSerializer, DrugSupplierSerializer, LabTechnicianSerializer
)

def home(request):
    # If already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('/api/healthcare/dashboard/')
    
    # Context for possible error messages
    context = {}
    if 'error' in request.GET:
        context['error'] = request.GET.get('error')
    
    return render(request, 'healthcare/index.html', context)

@login_required(login_url='/api/healthcare/')
def dashboard(request):
    return render(request, 'healthcare/dashboard.html')

@login_required(login_url='/api/healthcare/')
def doctors(request):
    return render(request, 'healthcare/doctors.html')

@login_required(login_url='/api/healthcare/')
def patients(request):
    return render(request, 'healthcare/patients.html')

@login_required(login_url='/api/healthcare/')
def nurses(request):
    return render(request, 'healthcare/nurses.html')

@login_required(login_url='/api/healthcare/')
def pharmacists(request):
    return render(request, 'healthcare/pharmacists.html')

@login_required(login_url='/api/healthcare/')
def lab_technicians(request):
    return render(request, 'healthcare/lab_technicians.html')

@login_required(login_url='/api/healthcare/')
def drug_suppliers(request):
    return render(request, 'healthcare/drug_suppliers.html')

class RegisterView(APIView):    
    permission_classes = [AllowAny]
    
    def post(self, request):
        data = request.data.copy()
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            # Log the user in after registration
            login(request, user)
            # Redirect to dashboard
            return redirect('/api/healthcare/dashboard/')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/api/healthcare/dashboard/')
        else:
            # Handle login failure
            return render(request, 'healthcare/index.html', {'error': 'Invalid credentials'})
    return redirect('/api/healthcare/')

def custom_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            return render(request, 'healthcare/index.html', {'reg_error': 'Passwords do not match'})
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'healthcare/index.html', {'reg_error': 'Username already exists'})
        
        # Create the user
        user = User.objects.create_user(username=username, password=password)
        # Log the user in
        login(request, user)
        return redirect('/api/healthcare/dashboard/')
    
    return redirect('/api/healthcare/')

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # Log the user in and create a session
            login(request, user)
            # Redirect to dashboard
            return redirect('/api/healthcare/dashboard/')
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

def user_logout(request):
    """Log the user out and redirect to the login page"""
    logout(request)
    return redirect('/api/healthcare/')
