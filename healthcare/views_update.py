from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.decorators import action

from .models import (
    Doctor, Patient, Nurse, Admin, Pharmacist, DrugSupplier, LabTechnician,
    Medication, Appointment, PatientRecord, Prescription, Visit, LabResult
)
from .serializers import (
    UserRegisterSerializer, DoctorSerializer, PatientSerializer, NurseSerializer,
    AdminSerializer, PharmacistSerializer, DrugSupplierSerializer, LabTechnicianSerializer,
    MedicationSerializer, AppointmentSerializer, PatientRecordSerializer,
    PrescriptionSerializer, VisitSerializer, LabResultSerializer
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
    # Get counts for dashboard stats
    context = {
        'doctors_count': Doctor.objects.count(),
        'patients_count': Patient.objects.count(),
        'appointments_count': Appointment.objects.count(),
        'nurses_count': Nurse.objects.count(),
        'pharmacists_count': Pharmacist.objects.count(),
        'lab_technicians_count': LabTechnician.objects.count(),
        'medications_count': Medication.objects.count(),
    }
    return render(request, 'healthcare/dashboard.html', context)

@login_required(login_url='/api/healthcare/')
def doctors(request):
    doctors_list = Doctor.objects.all()
    return render(request, 'healthcare/doctors.html', {'doctors': doctors_list})

@login_required(login_url='/api/healthcare/')
def patients(request):
    patients_list = Patient.objects.all()
    return render(request, 'healthcare/patients.html', {'patients': patients_list})

@login_required(login_url='/api/healthcare/')
def nurses(request):
    nurses_list = Nurse.objects.all()
    return render(request, 'healthcare/nurses.html', {'nurses': nurses_list})

@login_required(login_url='/api/healthcare/')
def pharmacists(request):
    pharmacists_list = Pharmacist.objects.all()
    return render(request, 'healthcare/pharmacists.html', {'pharmacists': pharmacists_list})

@login_required(login_url='/api/healthcare/')
def lab_technicians(request):
    technicians_list = LabTechnician.objects.all()
    return render(request, 'healthcare/lab_technicians.html', {'technicians': technicians_list})

@login_required(login_url='/api/healthcare/')
def drug_suppliers(request):
    suppliers_list = DrugSupplier.objects.all()
    return render(request, 'healthcare/drug_suppliers.html', {'suppliers': suppliers_list})

# APPOINTMENT VIEWS
@login_required(login_url='/api/healthcare/')
def appointment_view(request):
    doctors_list = Doctor.objects.all()
    patients_list = Patient.objects.all()
    appointments_list = Appointment.objects.all().order_by('-appointment_date', '-appointment_time')
    
    context = {
        'doctors': doctors_list,
        'patients': patients_list,
        'appointments': appointments_list
    }
    
    return render(request, 'healthcare/appointment.html', context)

@login_required(login_url='/api/healthcare/')
def appointment_create(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('date')
        appointment_time = request.POST.get('time')
        appointment_type = request.POST.get('type')
        duration = request.POST.get('duration')
        notes = request.POST.get('notes')
        
        try:
            patient = Patient.objects.get(id=patient_id)
            doctor = Doctor.objects.get(id=doctor_id)
            
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                appointment_type=appointment_type,
                duration=duration,
                notes=notes,
                status='scheduled'
            )
            
            return JsonResponse({'success': True, 'message': 'Appointment created successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='/api/healthcare/')
def appointment_update(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        appointment.patient_id = request.POST.get('patient', appointment.patient_id)
        appointment.doctor_id = request.POST.get('doctor', appointment.doctor_id)
        appointment.appointment_date = request.POST.get('date', appointment.appointment_date)
        appointment.appointment_time = request.POST.get('time', appointment.appointment_time)
        appointment.appointment_type = request.POST.get('type', appointment.appointment_type)
        appointment.duration = request.POST.get('duration', appointment.duration)
        appointment.status = request.POST.get('status', appointment.status)
        appointment.notes = request.POST.get('notes', appointment.notes)
        
        appointment.save()
        return JsonResponse({'success': True, 'message': 'Appointment updated successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='/api/healthcare/')
def appointment_delete(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        appointment.delete()
        return JsonResponse({'success': True, 'message': 'Appointment deleted successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='/api/healthcare/')
def appointment_status(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in [s[0] for s in Appointment.STATUS_CHOICES]:
            appointment.status = status
            appointment.save()
            return JsonResponse({'success': True, 'message': f'Appointment marked as {status}!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

# MEDICATION VIEWS
@login_required(login_url='/api/healthcare/')
def medications_view(request):
    medications_list = Medication.objects.all()
    suppliers_list = DrugSupplier.objects.all()
    
    context = {
        'medications': medications_list,
        'suppliers': suppliers_list
    }
    
    return render(request, 'healthcare/medications.html', context)

@login_required(login_url='/api/healthcare/')
def medication_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        generic_name = request.POST.get('generic_name')
        category = request.POST.get('category')
        description = request.POST.get('description')
        unit_price = request.POST.get('unit_price')
        stock_quantity = request.POST.get('stock_quantity')
        reorder_level = request.POST.get('reorder_level')
        supplier_id = request.POST.get('supplier')
        
        try:
            supplier = DrugSupplier.objects.get(id=supplier_id) if supplier_id else None
            
            medication = Medication.objects.create(
                name=name,
                generic_name=generic_name,
                category=category,
                description=description,
                unit_price=unit_price,
                stock_quantity=stock_quantity,
                reorder_level=reorder_level,
                supplier=supplier
            )
            
            return JsonResponse({'success': True, 'message': 'Medication added successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='/api/healthcare/')
def medication_update(request, medication_id):
    medication = get_object_or_404(Medication, id=medication_id)
    
    if request.method == 'POST':
        medication.name = request.POST.get('name', medication.name)
        medication.generic_name = request.POST.get('generic_name', medication.generic_name)
        medication.category = request.POST.get('category', medication.category)
        medication.description = request.POST.get('description', medication.description)
        medication.unit_price = request.POST.get('unit_price', medication.unit_price)
        medication.stock_quantity = request.POST.get('stock_quantity', medication.stock_quantity)
        medication.reorder_level = request.POST.get('reorder_level', medication.reorder_level)
        
        supplier_id = request.POST.get('supplier')
        if supplier_id:
            try:
                supplier = DrugSupplier.objects.get(id=supplier_id)
                medication.supplier = supplier
            except DrugSupplier.DoesNotExist:
                pass
        
        medication.save()
        return JsonResponse({'success': True, 'message': 'Medication updated successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='/api/healthcare/')
def medication_delete(request, medication_id):
    medication = get_object_or_404(Medication, id=medication_id)
    
    if request.method == 'POST':
        medication.delete()
        return JsonResponse({'success': True, 'message': 'Medication deleted successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# PATIENT RECORD VIEWS
@login_required(login_url='/api/healthcare/')
def patient_record_view(request):
    patients_list = Patient.objects.all()
    doctors_list = Doctor.objects.all()
    
    # If a specific patient is requested
    patient_id = request.GET.get('patient_id')
    patient = None
    records = []
    visits = []
    prescriptions = []
    lab_results = []
    
    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
            records = PatientRecord.objects.filter(patient=patient).order_by('-record_date')
            visits = Visit.objects.filter(patient=patient).order_by('-visit_date')
            prescriptions = Prescription.objects.filter(patient=patient).order_by('-created_at')
            lab_results = LabResult.objects.filter(patient=patient).order_by('-test_date')
        except Patient.DoesNotExist:
            pass
    
    context = {
        'patients': patients_list,
        'doctors': doctors_list,
        'selected_patient': patient,
        'medical_records': records,
        'visits': visits,
        'prescriptions': prescriptions,
        'lab_results': lab_results
    }
    
    return render(request, 'healthcare/patient_record.html', context)

@login_required(login_url='/api/healthcare/')
def patient_record_create(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        record_type = request.POST.get('record_type')
        description = request.POST.get('description')
        record_date = request.POST.get('record_date')
        doctor_id = request.POST.get('doctor')
        attachments = request.FILES.get('attachments')
        
        try:
            patient = Patient.objects.get(id=patient_id)
            doctor = Doctor.objects.get(id=doctor_id) if doctor_id else None
            
            record = PatientRecord.objects.create(
                patient=patient,
                record_type=record_type,
                description=description,
                record_date=record_date,
                doctor=doctor
            )
            
            if attachments:
                record.attachments = attachments
                record.save()
            
            return JsonResponse({'success': True, 'message': 'Medical record added successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='/api/healthcare/')
def patient_record_update(request, record_id):
    record = get_object_or_404(PatientRecord, id=record_id)
    
    if request.method == 'POST':
        record.record_type = request.POST.get('record_type', record.record_type)
        record.description = request.POST.get('description', record.description)
        record.record_date = request.POST.get('record_date', record.record_date)
        
        doctor_id = request.POST.get('doctor')
        if doctor_id:
            try:
                doctor = Doctor.objects.get(id=doctor_id)
                record.doctor = doctor
            except Doctor.DoesNotExist:
                pass
        
        attachments = request.FILES.get('attachments')
        if attachments:
            record.attachments = attachments
        
        record.save()
        return JsonResponse({'success': True, 'message': 'Medical record updated successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='/api/healthcare/')
def patient_record_delete(request, record_id):
    record = get_object_or_404(PatientRecord, id=record_id)
    
    if request.method == 'POST':
        record.delete()
        return JsonResponse({'success': True, 'message': 'Medical record deleted successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Other views
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
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'specialization', 'email']

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email', 'phone']

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

# New API ViewSets for the added models
class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'generic_name', 'category']
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        low_stock = self.queryset.filter(stock_quantity__lte='reorder_level')
        serializer = self.serializer_class(low_stock, many=True)
        return Response(serializer.data)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['patient__name', 'doctor__name', 'appointment_type', 'status']
    
    @action(detail=False, methods=['get'])
    def by_status(self, request):
        status = request.query_params.get('status', None)
        if status:
            appointments = self.queryset.filter(status=status)
            serializer = self.serializer_class(appointments, many=True)
            return Response(serializer.data)
        return Response({"error": "Status parameter required"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def by_date(self, request):
        date = request.query_params.get('date', None)
        if date:
            appointments = self.queryset.filter(appointment_date=date)
            serializer = self.serializer_class(appointments, many=True)
            return Response(serializer.data)
        return Response({"error": "Date parameter required"}, status=status.HTTP_400_BAD_REQUEST)

class PatientRecordViewSet(viewsets.ModelViewSet):
    queryset = PatientRecord.objects.all()
    serializer_class = PatientRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['patient__name', 'record_type', 'description']
    
    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        patient_id = request.query_params.get('patient_id', None)
        if patient_id:
            records = self.queryset.filter(patient_id=patient_id)
            serializer = self.serializer_class(records, many=True)
            return Response(serializer.data)
        return Response({"error": "Patient ID parameter required"}, status=status.HTTP_400_BAD_REQUEST)

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        active = self.queryset.filter(is_active=True)
        serializer = self.serializer_class(active, many=True)
        return Response(serializer.data)

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]

class LabResultViewSet(viewsets.ModelViewSet):
    queryset = LabResult.objects.all()
    serializer_class = LabResultSerializer
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
            'total_appointments': Appointment.objects.count(),
            'total_medications': Medication.objects.count(),
            'scheduled_appointments': Appointment.objects.filter(status='scheduled').count(),
            'low_stock_medications': Medication.objects.filter(stock_quantity__lte='reorder_level').count(),
        }
        return Response(stats)

def user_logout(request):
    """Log the user out and redirect to the login page"""
    logout(request)
    return redirect('/api/healthcare/')
