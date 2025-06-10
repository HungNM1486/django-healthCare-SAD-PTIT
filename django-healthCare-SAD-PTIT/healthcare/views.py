import os
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
    """Landing page with login/register forms"""
    if request.user.is_authenticated:
        return redirect('/api/healthcare/dashboard/')
    
    # Get error messages from URL parameters or session
    context = {}
    
    # Login error
    if 'error' in request.GET:
        context['error'] = request.GET.get('error')
    
    # Registration error  
    if 'reg_error' in request.GET:
        context['reg_error'] = request.GET.get('reg_error')
        
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
    """View to display doctors with search and filter functionality"""
    doctors_list = Doctor.objects.all()
    
    # Handle search query
    search = request.GET.get('search')
    if search:
        doctors_list = doctors_list.filter(
            Q(name__icontains=search) | 
            Q(specialization__icontains=search) |
            Q(email__icontains=search)
        )
    
    # Handle specialization filter
    specialization = request.GET.get('specialization')
    if specialization and specialization != 'All Specializations':
        doctors_list = doctors_list.filter(specialization=specialization)
    
    # Get distinct specializations for filter dropdown
    specializations = Doctor.objects.values_list('specialization', flat=True).distinct()
    
    context = {
        'doctors': doctors_list,
        'specializations': specializations
    }
    return render(request, 'healthcare/doctors.html', context)

@login_required(login_url='/api/healthcare/')
def patients(request):
    """View to display patients with search functionality"""
    patients_list = Patient.objects.all()
    
    # Handle search query
    search = request.GET.get('search')
    if search:
        patients_list = patients_list.filter(
            Q(name__icontains=search) | 
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )
    
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
    
    # Handle search query
    search = request.GET.get('search')
    if search:
        appointments_list = appointments_list.filter(
            Q(patient__name__icontains=search) | 
            Q(doctor__name__icontains=search) |
            Q(appointment_type__icontains=search)
        )
    
    # Handle status filter
    status = request.GET.get('status')
    if status and status != 'All Status':
        appointments_list = appointments_list.filter(status=status)
    
    # Handle date filter
    date = request.GET.get('date')
    if date:
        appointments_list = appointments_list.filter(appointment_date=date)
    
    # Handle patient filter
    patient_id = request.GET.get('patient_id')
    if patient_id:
        appointments_list = appointments_list.filter(patient_id=patient_id)
    
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
    medications_list = Medication.objects.all().select_related('supplier')
    suppliers_list = DrugSupplier.objects.all()
    
    # Handle search query
    search = request.GET.get('search')
    if search:
        medications_list = medications_list.filter(
            Q(name__icontains=search) | 
            Q(generic_name__icontains=search) |
            Q(category__icontains=search)
        )
    
    # Handle category filter
    category = request.GET.get('category')
    if category:
        medications_list = medications_list.filter(category=category)
    
    # Handle stock status filter
    status = request.GET.get('status')
    if status:
        if status == 'Low Stock':
            medications_list = medications_list.filter(stock_quantity__lte='reorder_level')
        elif status == 'Out of Stock':
            medications_list = medications_list.filter(stock_quantity__lte=0)
        elif status == 'In Stock':
            medications_list = medications_list.filter(stock_quantity__gt='reorder_level')
    
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
            supplier = None
            if supplier_id:
                supplier = DrugSupplier.objects.get(id=supplier_id)
                
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
            
            return JsonResponse({'success': True, 'message': 'Medication created successfully!'})
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
                medication.supplier = DrugSupplier.objects.get(id=supplier_id)
            except DrugSupplier.DoesNotExist:
                medication.supplier = None
        else:
            medication.supplier = None
        
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
    from django.utils import timezone
    
    # Get all doctors for the forms
    doctors_list = Doctor.objects.all()
    
    # Get all medications, lab technicians, and suppliers for the forms
    medications_list = Medication.objects.all()
    lab_technicians_list = LabTechnician.objects.all()
    suppliers_list = DrugSupplier.objects.all()
    
    # Get recent patients (last 5 patients with records or created recently)
    recent_patients = Patient.objects.order_by('-created_at')[:5]
    
    current_patient = None
    patient_records = []
    patient_appointments = []
    patient_prescriptions = []
    patient_lab_results = []
    
    # Handle patient selection
    patient_id = request.GET.get('patient_id')
    if patient_id:
        try:
            current_patient = Patient.objects.get(id=patient_id)
            patient_records = PatientRecord.objects.filter(patient=current_patient).order_by('-record_date')
            patient_appointments = Appointment.objects.filter(patient=current_patient).order_by('-appointment_date')
            patient_prescriptions = Prescription.objects.filter(patient=current_patient).order_by('-start_date')
            patient_lab_results = LabResult.objects.filter(patient=current_patient).order_by('-test_date')
        except Patient.DoesNotExist:
            pass
    
    # Handle search
    search = request.GET.get('search')
    if search:
        searched_patients = Patient.objects.filter(name__icontains=search)
        if searched_patients.exists():
            current_patient = searched_patients.first()
            patient_records = PatientRecord.objects.filter(patient=current_patient).order_by('-record_date')
            patient_appointments = Appointment.objects.filter(patient=current_patient).order_by('-appointment_date')
            patient_prescriptions = Prescription.objects.filter(patient=current_patient).order_by('-start_date')
            patient_lab_results = LabResult.objects.filter(patient=current_patient).order_by('-test_date')
    
    context = {
        'doctors': doctors_list,
        'medications': medications_list,
        'lab_technicians': lab_technicians_list,
        'suppliers': suppliers_list,
        'recent_patients': recent_patients,
        'current_patient': current_patient,
        'patient_records': patient_records,
        'patient_appointments': patient_appointments,
        'patient_prescriptions': patient_prescriptions,
        'patient_lab_results': patient_lab_results,
        'today_date': timezone.now()
    }
    
    return render(request, 'healthcare/patient_record.html', context)

@login_required(login_url='/api/healthcare/')
def patient_record_create(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        record_date = request.POST.get('record_date')
        record_type = request.POST.get('record_type')
        description = request.POST.get('description')
        
        try:
            patient = Patient.objects.get(id=patient_id)
            doctor = Doctor.objects.get(id=doctor_id)
            
            record = PatientRecord(
                patient=patient,
                doctor=doctor,
                record_date=record_date,
                record_type=record_type,
                description=description
            )
            
            # Handle file upload if present
            if 'attachments' in request.FILES:
                record.attachments = request.FILES['attachments']
            
            record.save()
            
            return JsonResponse({'success': True, 'message': 'Patient record created successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='/api/healthcare/')
def patient_record_update(request, record_id):
    record = get_object_or_404(PatientRecord, id=record_id)
    
    if request.method == 'POST':
        record.patient_id = request.POST.get('patient', record.patient_id)
        record.doctor_id = request.POST.get('doctor', record.doctor_id)
        record.record_date = request.POST.get('record_date', record.record_date)
        record.record_type = request.POST.get('record_type', record.record_type)
        record.description = request.POST.get('description', record.description)
        
        # Handle file upload if present
        if 'attachments' in request.FILES:
            # Delete old file if it exists
            if record.attachments:
                try:
                    old_file_path = record.attachments.path
                    if os.path.isfile(old_file_path):
                        os.remove(old_file_path)
                except:
                    pass
            record.attachments = request.FILES['attachments']
        
        record.save()
        return JsonResponse({'success': True, 'message': 'Patient record updated successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='/api/healthcare/')
def patient_record_delete(request, record_id):
    record = get_object_or_404(PatientRecord, id=record_id)
    
    if request.method == 'POST':
        record.delete()
        return JsonResponse({'success': True, 'message': 'Patient record deleted successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

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
    """Handle login form submission"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/api/healthcare/dashboard/')
        else:
            # Redirect back with error message
            return redirect('/api/healthcare/?error=Tên đăng nhập hoặc mật khẩu không đúng')
    
    return redirect('/api/healthcare/')

def custom_register(request):
    """Handle registration form submission"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email', '')
        
        # Validate passwords match
        if password != password2:
            return redirect('/api/healthcare/?reg_error=Mật khẩu xác nhận không khớp')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return redirect('/api/healthcare/?reg_error=Tên đăng nhập đã tồn tại')
        
        # Check if email already exists (if provided)
        if email and User.objects.filter(email=email).exists():
            return redirect('/api/healthcare/?reg_error=Email đã được sử dụng')
        
        try:
            # Create the user
            user = User.objects.create_user(
                username=username, 
                password=password,
                email=email
            )
            
            # Auto login after registration
            login(request, user)
            return redirect('/api/healthcare/dashboard/')
            
        except Exception as e:
            return redirect('/api/healthcare/?reg_error=Có lỗi xảy ra khi tạo tài khoản')
    
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
    permission_classes = [AllowAny]  # Allow public access for development
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
    permission_classes = [AllowAny]  # Allow public access for development
    
    @action(detail=False, methods=['get'])
    def by_patient(self, request):
        patient_id = request.query_params.get('patient_id', None)
        if patient_id:
            records = self.queryset.filter(patient_id=patient_id)
            serializer = self.serializer_class(records, many=True)
            return Response(serializer.data)
        return Response({"error": "Patient ID required"}, status=status.HTTP_400_BAD_REQUEST)

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
        }
        return Response(stats)

def user_logout(request):
    """Log the user out and redirect to the login page"""
    logout(request)
    return redirect('/api/healthcare/')

@login_required(login_url='/api/healthcare/')
def doctor_create(request):
    """Create a new doctor"""
    if request.method == 'POST':
        name = request.POST.get('name')
        specialization = request.POST.get('specialization')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        
        try:
            # Check if email already exists
            if Doctor.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'A doctor with this email already exists.'})
            
            doctor = Doctor.objects.create(
                name=name,
                specialization=specialization,
                phone=phone,
                email=email
            )
            
            return JsonResponse({'success': True, 'message': 'Doctor created successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='/api/healthcare/')
def doctor_update(request, doctor_id):
    """Update an existing doctor"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        specialization = request.POST.get('specialization')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        
        try:
            # Check if email already exists for another doctor
            if Doctor.objects.filter(email=email).exclude(id=doctor_id).exists():
                return JsonResponse({'success': False, 'message': 'Another doctor with this email already exists.'})
            
            doctor.name = name
            doctor.specialization = specialization
            doctor.phone = phone
            doctor.email = email
            doctor.save()
            
            return JsonResponse({'success': True, 'message': 'Doctor updated successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='/api/healthcare/')
def doctor_delete(request, doctor_id):
    """Delete a doctor"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        try:
            # Check if doctor has related appointments
            appointment_count = Appointment.objects.filter(doctor=doctor).count()
            if appointment_count > 0:
                return JsonResponse({
                    'success': False, 
                    'message': f'Cannot delete this doctor as they have {appointment_count} appointments.'
                })
            
            # Check if doctor has related patient records
            record_count = PatientRecord.objects.filter(doctor=doctor).count()
            if record_count > 0:
                return JsonResponse({
                    'success': False, 
                    'message': f'Cannot delete this doctor as they are associated with {record_count} patient records.'
                })
            
            doctor_name = doctor.name
            doctor.delete()
            return JsonResponse({'success': True, 'message': f'Doctor {doctor_name} deleted successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='/api/healthcare/')
def patient_create(request):
    """Create a new patient"""
    if request.method == 'POST':
        name = request.POST.get('name')
        date_of_birth = request.POST.get('date_of_birth')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        
        try:
            # Check if email already exists
            if Patient.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'A patient with this email already exists.'})
            
            patient = Patient.objects.create(
                name=name,
                date_of_birth=date_of_birth,
                phone=phone,
                email=email,
                address=address
            )
            
            return JsonResponse({'success': True, 'message': 'Patient created successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='/api/healthcare/')
def patient_update(request, patient_id):
    """Update an existing patient"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        date_of_birth = request.POST.get('date_of_birth')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        
        try:
            # Check if email already exists for another patient
            if Patient.objects.filter(email=email).exclude(id=patient_id).exists():
                return JsonResponse({'success': False, 'message': 'Another patient with this email already exists.'})
            
            patient.name = name
            patient.date_of_birth = date_of_birth
            patient.phone = phone
            patient.email = email
            patient.address = address
            patient.save()
            
            return JsonResponse({'success': True, 'message': 'Patient updated successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='/api/healthcare/')
def patient_delete(request, patient_id):
    """Delete a patient"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        try:
            # Check if patient has related appointments
            appointment_count = Appointment.objects.filter(patient=patient).count()
            record_count = PatientRecord.objects.filter(patient=patient).count()
            prescription_count = Prescription.objects.filter(patient=patient).count()
            visit_count = Visit.objects.filter(patient=patient).count()
            lab_count = LabResult.objects.filter(patient=patient).count()
            
            total_related = appointment_count + record_count + prescription_count + visit_count + lab_count
            
            if total_related > 0:
                message = f"This patient has {total_related} related records: "
                details = []
                if appointment_count > 0:
                    details.append(f"{appointment_count} appointments")
                if record_count > 0:
                    details.append(f"{record_count} medical records")
                if prescription_count > 0:
                    details.append(f"{prescription_count} prescriptions")
                if visit_count > 0:
                    details.append(f"{visit_count} visits")
                if lab_count > 0:
                    details.append(f"{lab_count} lab results")
                
                message += ", ".join(details) + ". Are you sure you want to delete this patient?"
                
                # If we want to prevent deletion with related records, uncomment this
                # return JsonResponse({'success': False, 'message': message})
            
            patient_name = patient.name
            patient.delete()
            return JsonResponse({'success': True, 'message': f'Patient {patient_name} and all related records deleted successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required(login_url='/api/healthcare/')
def patient_detail(request, patient_id):
    """Get patient details"""
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'GET':
        data = {
            'id': patient.id,
            'name': patient.name,
            'date_of_birth': patient.date_of_birth,
            'age': patient.age,
            'phone': patient.phone,
            'email': patient.email,
            'address': patient.address,
            'created_at': patient.created_at
        }
        return JsonResponse(data)
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
