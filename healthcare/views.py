from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count, Sum, Avg, F
from django.utils import timezone
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import StandardResultsSetPagination, LargeResultsSetPagination
from datetime import datetime, timedelta, date

from .models import (
    Doctor, Patient, Nurse, Admin, Pharmacist, DrugSupplier, LabTechnician,
    Medicine, Appointment, MedicalRecord, Prescription, LabTest
)
from .serializers import (
    UserRegisterSerializer, DoctorSerializer, PatientSerializer, NurseSerializer,
    AdminSerializer, PharmacistSerializer, DrugSupplierSerializer, LabTechnicianSerializer,
    DoctorSummarySerializer, PatientSummarySerializer, DoctorDetailSerializer, PatientDetailSerializer,
    MedicineSerializer, MedicineSummarySerializer, AppointmentSerializer, AppointmentSummarySerializer,
    MedicalRecordSerializer, MedicalRecordSummarySerializer, MedicalRecordDetailSerializer,
    PrescriptionSerializer, LabTestSerializer, LabTestSummarySerializer,
    BulkAppointmentCreateSerializer, BulkMedicineStockUpdateSerializer
)

# Custom Pagination
# Authentication Views (Updated)
class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully',
                'user_id': user.id,
                'username': user.username
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
                'user_id': user.id,
                'username': user.username
            }, status=status.HTTP_200_OK)
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

# Base ViewSet with enhanced functionality
class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_name = str(instance)
        
        # Check if instance can be deleted (has dependencies)
        if hasattr(instance, 'can_be_deleted'):
            if not instance.can_be_deleted():
                return Response(
                    {'error': f'{instance_name} cannot be deleted due to existing dependencies'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        self.perform_destroy(instance)
        return Response(
            {'message': f'{instance_name} deleted successfully'}, 
            status=status.HTTP_204_NO_CONTENT
        )

# Enhanced Doctor ViewSet
class DoctorViewSet(BaseModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    search_fields = ['name', 'specialization', 'email', 'license_number']
    filterset_fields = ['specialization', 'is_available']
    ordering_fields = ['name', 'specialization', 'consultation_fee', 'years_of_experience']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return DoctorSummarySerializer
        elif self.action == 'retrieve':
            return DoctorDetailSerializer
        return DoctorSerializer
    
    def get_queryset(self):
        queryset = Doctor.objects.all()
        
        # Filter by availability
        available_only = self.request.query_params.get('available_only', None)
        if available_only and available_only.lower() == 'true':
            queryset = queryset.filter(is_available=True)
        
        # Filter by experience range
        min_experience = self.request.query_params.get('min_experience', None)
        if min_experience:
            queryset = queryset.filter(years_of_experience__gte=int(min_experience))
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def specializations(self, request):
        """Get list of all specializations with counts"""
        specializations = Doctor.objects.values('specialization').annotate(
            count=Count('id')
        ).order_by('specialization')
        return Response({'specializations': list(specializations)})
    
    @action(detail=False, methods=['get'])
    def available_today(self, request):
        """Get doctors available today"""
        today = timezone.now().date()
        available_doctors = Doctor.objects.filter(
            is_available=True
        ).exclude(
            appointments__appointment_date__date=today,
            appointments__status__in=['scheduled', 'confirmed', 'in_progress']
        )
        serializer = DoctorSummarySerializer(available_doctors, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        """Get doctor's schedule for a specific date range"""
        doctor = self.get_object()
        start_date = request.query_params.get('start_date', timezone.now().date())
        end_date = request.query_params.get('end_date', timezone.now().date() + timedelta(days=7))
        
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        appointments = doctor.appointments.filter(
            appointment_date__date__range=[start_date, end_date],
            status__in=['scheduled', 'confirmed', 'in_progress']
        ).order_by('appointment_date')
        
        serializer = AppointmentSummarySerializer(appointments, many=True)
        return Response({
            'doctor': doctor.name,
            'period': f"{start_date} to {end_date}",
            'appointments': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def toggle_availability(self, request, pk=None):
        """Toggle doctor availability"""
        doctor = self.get_object()
        doctor.is_available = not doctor.is_available
        doctor.save()
        return Response({
            'message': f"Doctor {doctor.name} is now {'available' if doctor.is_available else 'unavailable'}",
            'is_available': doctor.is_available
        })

# Enhanced Patient ViewSet
class PatientViewSet(BaseModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    search_fields = ['name', 'email', 'phone', 'blood_type']
    filterset_fields = ['blood_type']
    ordering_fields = ['name', 'date_of_birth', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PatientSummarySerializer
        elif self.action == 'retrieve':
            return PatientDetailSerializer
        return PatientSerializer
    
    def get_queryset(self):
        queryset = Patient.objects.all()
        
        # Filter by age range
        min_age = self.request.query_params.get('min_age', None)
        max_age = self.request.query_params.get('max_age', None)
        
        if min_age or max_age:
            today = timezone.now().date()
            if min_age:
                min_birth_date = today.replace(year=today.year - int(min_age))
                queryset = queryset.filter(date_of_birth__lte=min_birth_date)
            if max_age:
                max_birth_date = today.replace(year=today.year - int(max_age))
                queryset = queryset.filter(date_of_birth__gte=max_birth_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def search_by_phone(self, request):
        """Search patient by phone number"""
        phone = request.query_params.get('phone', '')
        if phone:
            patients = Patient.objects.filter(phone__icontains=phone)
            serializer = PatientSummarySerializer(patients, many=True)
            return Response(serializer.data)
        return Response({'error': 'Phone parameter required'}, status=400)
    
    @action(detail=False, methods=['get'])
    def blood_type_stats(self, request):
        """Get blood type distribution statistics"""
        stats = Patient.objects.values('blood_type').annotate(
            count=Count('id')
        ).order_by('blood_type')
        return Response({'blood_type_stats': list(stats)})
    
    @action(detail=True, methods=['get'])
    def medical_history(self, request, pk=None):
        """Get patient's complete medical history"""
        patient = self.get_object()
        
        # Get medical records
        medical_records = patient.medical_records.order_by('-created_at')[:10]
        
        # Get appointments
        appointments = patient.appointments.order_by('-appointment_date')[:10]
        
        # Get prescriptions
        prescriptions = Prescription.objects.filter(
            medical_record__patient=patient
        ).order_by('-created_at')[:10]
        
        return Response({
            'patient': PatientSerializer(patient).data,
            'medical_records': MedicalRecordSummarySerializer(medical_records, many=True).data,
            'recent_appointments': AppointmentSummarySerializer(appointments, many=True).data,
            'recent_prescriptions': PrescriptionSerializer(prescriptions, many=True).data
        })

# Medicine ViewSet
class MedicineViewSet(BaseModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    search_fields = ['name', 'generic_name', 'manufacturer']
    filterset_fields = ['dosage_form', 'requires_prescription', 'supplier']
    ordering_fields = ['name', 'price_per_unit', 'stock_quantity', 'expiry_date']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MedicineSummarySerializer
        return MedicineSerializer
    
    def get_queryset(self):
        queryset = Medicine.objects.select_related('supplier')
        
        # Filter by stock status
        stock_status = self.request.query_params.get('stock_status', None)
        if stock_status == 'low':
            queryset = queryset.filter(stock_quantity__lte=F('minimum_stock_level'))
        elif stock_status == 'out':
            queryset = queryset.filter(stock_quantity=0)
        
        # Filter by expiry status
        expiry_status = self.request.query_params.get('expiry_status', None)
        if expiry_status == 'expired':
            queryset = queryset.filter(expiry_date__lt=timezone.now().date())
        elif expiry_status == 'expiring_soon':
            week_from_now = timezone.now().date() + timedelta(days=30)
            queryset = queryset.filter(expiry_date__lte=week_from_now, expiry_date__gte=timezone.now().date())
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get medicines with low stock"""
        from django.db.models import F
        low_stock_medicines = Medicine.objects.filter(
            stock_quantity__lte=F('minimum_stock_level')
        ).order_by('stock_quantity')
        serializer = MedicineSummarySerializer(low_stock_medicines, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def expiring_soon(self, request):
        """Get medicines expiring within 30 days"""
        thirty_days_from_now = timezone.now().date() + timedelta(days=30)
        expiring_medicines = Medicine.objects.filter(
            expiry_date__lte=thirty_days_from_now,
            expiry_date__gte=timezone.now().date()
        ).order_by('expiry_date')
        serializer = MedicineSummarySerializer(expiring_medicines, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def bulk_update_stock(self, request):
        """Bulk update medicine stock quantities"""
        serializer = BulkMedicineStockUpdateSerializer(data=request.data)
        if serializer.is_valid():
            updated_medicines = serializer.save()
            return Response({
                'message': f'{len(updated_medicines)} medicines updated successfully',
                'updated_count': len(updated_medicines)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        """Adjust medicine stock (add or remove)"""
        medicine = self.get_object()
        adjustment = request.data.get('adjustment', 0)
        reason = request.data.get('reason', '')
        
        try:
            adjustment = int(adjustment)
            new_stock = max(0, medicine.stock_quantity + adjustment)
            old_stock = medicine.stock_quantity
            medicine.stock_quantity = new_stock
            medicine.save()
            
            return Response({
                'message': f'Stock adjusted successfully',
                'old_stock': old_stock,
                'new_stock': new_stock,
                'adjustment': adjustment,
                'reason': reason
            })
        except ValueError:
            return Response(
                {'error': 'Invalid adjustment value'},
                status=status.HTTP_400_BAD_REQUEST
            )

# Appointment ViewSet
class AppointmentViewSet(BaseModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    search_fields = ['patient__name', 'doctor__name', 'chief_complaint']
    filterset_fields = ['status', 'appointment_type', 'doctor', 'patient']
    ordering_fields = ['appointment_date', 'created_at']
    ordering = ['-appointment_date']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AppointmentSummarySerializer
        return AppointmentSerializer
    
    def get_queryset(self):
        queryset = Appointment.objects.select_related('patient', 'doctor', 'nurse_assigned')
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            queryset = queryset.filter(appointment_date__date__gte=start_date)
        
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(appointment_date__date__lte=end_date)
        
        # Filter by today's appointments
        today_only = self.request.query_params.get('today_only', None)
        if today_only and today_only.lower() == 'true':
            queryset = queryset.filter(appointment_date__date=timezone.now().date())
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's appointments"""
        today_appointments = Appointment.objects.filter(
            appointment_date__date=timezone.now().date()
        ).order_by('appointment_date')
        serializer = AppointmentSummarySerializer(today_appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming appointments"""
        upcoming_appointments = Appointment.objects.filter(
            appointment_date__gt=timezone.now(),
            status__in=['scheduled', 'confirmed']
        ).order_by('appointment_date')[:20]
        serializer = AppointmentSummarySerializer(upcoming_appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an appointment"""
        appointment = self.get_object()
        
        if not appointment.can_be_cancelled():
            return Response(
                {'error': 'Appointment cannot be cancelled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointment.status = 'cancelled'
        appointment.save()
        
        return Response({
            'message': 'Appointment cancelled successfully',
            'appointment_id': appointment.id
        })
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark appointment as completed"""
        appointment = self.get_object()
        
        if appointment.status != 'in_progress':
            return Response(
                {'error': 'Only in-progress appointments can be completed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointment.status = 'completed'
        appointment.save()
        
        return Response({
            'message': 'Appointment completed successfully',
            'appointment_id': appointment.id
        })
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Create multiple appointments"""
        serializer = BulkAppointmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            appointments = serializer.save()
            return Response({
                'message': f'{len(appointments)} appointments created successfully',
                'appointment_ids': [apt.id for apt in appointments]
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Medical Record ViewSet
class MedicalRecordViewSet(BaseModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    search_fields = ['patient__name', 'doctor__name', 'diagnosis', 'symptoms']
    filterset_fields = ['is_emergency', 'requires_follow_up', 'doctor', 'patient']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MedicalRecordSummarySerializer
        elif self.action == 'retrieve':
            return MedicalRecordDetailSerializer
        return MedicalRecordSerializer
    
    def get_queryset(self):
        queryset = MedicalRecord.objects.select_related('patient', 'doctor', 'appointment')
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            queryset = queryset.filter(created_at__date__gte=start_date)
        
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(created_at__date__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def emergency_cases(self, request):
        """Get emergency medical records"""
        emergency_records = MedicalRecord.objects.filter(
            is_emergency=True
        ).order_by('-created_at')
        serializer = MedicalRecordSummarySerializer(emergency_records, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def follow_up_required(self, request):
        """Get records requiring follow-up"""
        follow_up_records = MedicalRecord.objects.filter(
            requires_follow_up=True
        ).order_by('-created_at')
        serializer = MedicalRecordSummarySerializer(follow_up_records, many=True)
        return Response(serializer.data)

# Continue with other ViewSets (Prescription, LabTest, etc.)
class PrescriptionViewSet(BaseModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    search_fields = ['medicine__name', 'medical_record__patient__name']
    filterset_fields = ['is_filled', 'medicine', 'filled_by']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Prescription.objects.select_related(
            'medicine', 'medical_record__patient', 'filled_by'
        )
        
        # Filter by fill status
        unfilled_only = self.request.query_params.get('unfilled_only', None)
        if unfilled_only and unfilled_only.lower() == 'true':
            queryset = queryset.filter(is_filled=False)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def fill(self, request, pk=None):
        """Mark prescription as filled"""
        prescription = self.get_object()
        pharmacist_id = request.data.get('pharmacist_id')
        
        if prescription.is_filled:
            return Response(
                {'error': 'Prescription already filled'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            pharmacist = Pharmacist.objects.get(id=pharmacist_id)
            prescription.mark_as_filled(pharmacist)
            
            return Response({
                'message': 'Prescription filled successfully',
                'filled_by': pharmacist.name,
                'filled_at': prescription.filled_at
            })
        except Pharmacist.DoesNotExist:
            return Response(
                {'error': 'Pharmacist not found'},
                status=status.HTTP_404_NOT_FOUND
            )

# Enhanced existing ViewSets
class NurseViewSet(BaseModelViewSet):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer
    search_fields = ['name', 'email', 'phone', 'department']
    filterset_fields = ['department', 'shift_type', 'is_available']
    ordering_fields = ['name', 'department']
    ordering = ['name']

class AdminViewSet(BaseModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    search_fields = ['name', 'email', 'phone', 'department']
    filterset_fields = ['department', 'role']
    ordering_fields = ['name', 'department']
    ordering = ['name']

class PharmacistViewSet(BaseModelViewSet):
    queryset = Pharmacist.objects.all()
    serializer_class = PharmacistSerializer
    search_fields = ['name', 'email', 'phone', 'license_number']
    filterset_fields = ['license_number']
    ordering_fields = ['name']
    ordering = ['name']

class DrugSupplierViewSet(BaseModelViewSet):
    queryset = DrugSupplier.objects.all()
    serializer_class = DrugSupplierSerializer
    search_fields = ['name', 'contact_person', 'email']
    filterset_fields = ['name', 'contact_person']
    ordering_fields = ['name', 'contact_person']
    ordering = ['name']

class LabTechnicianViewSet(BaseModelViewSet):
    queryset = LabTechnician.objects.all()
    serializer_class = LabTechnicianSerializer
    search_fields = ['name', 'email', 'phone', 'specialization']
    filterset_fields = ['specialization']
    ordering_fields = ['name', 'specialization']
    ordering = ['name']

class LabTestViewSet(BaseModelViewSet):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer
    search_fields = ['test_name', 'medical_record__patient__name']
    filterset_fields = ['test_type', 'status', 'is_abnormal', 'ordered_by']
    ordering_fields = ['created_at', 'scheduled_date']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return LabTestSummarySerializer
        return LabTestSerializer
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark lab test as completed with results"""
        lab_test = self.get_object()
        results = request.data.get('results', '')
        is_abnormal = request.data.get('is_abnormal', False)
        
        if lab_test.status == 'completed':
            return Response(
                {'error': 'Lab test already completed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        lab_test.mark_completed(results, is_abnormal)
        
        return Response({
            'message': 'Lab test completed successfully',
            'test_id': lab_test.id,
            'results': results,
            'is_abnormal': is_abnormal
        })

# Enhanced Dashboard Statistics View
class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get comprehensive dashboard statistics"""
        today = timezone.now().date()
        
        # Basic counts
        basic_stats = {
            'total_doctors': Doctor.objects.count(),
            'total_patients': Patient.objects.count(),
            'total_nurses': Nurse.objects.count(),
            'total_pharmacists': Pharmacist.objects.count(),
            'total_lab_technicians': LabTechnician.objects.count(),
            'total_drug_suppliers': DrugSupplier.objects.count(),
            'total_medicines': Medicine.objects.count(),
        }
        
        # Today's statistics
        today_stats = {
            'today_appointments': Appointment.objects.filter(
                appointment_date__date=today
            ).count(),
            'today_completed_appointments': Appointment.objects.filter(
                appointment_date__date=today,
                status='completed'
            ).count(),
            'today_medical_records': MedicalRecord.objects.filter(
                created_at__date=today
            ).count(),
            'today_prescriptions': Prescription.objects.filter(
                created_at__date=today
            ).count(),
        }
        
        # Medicine statistics
        medicine_stats = {
            'low_stock_medicines': Medicine.objects.filter(
                stock_quantity__lte=F('minimum_stock_level')
            ).count(),
            'expired_medicines': Medicine.objects.filter(
                expiry_date__lt=today
            ).count(),
            'expiring_soon_medicines': Medicine.objects.filter(
                expiry_date__lte=today + timedelta(days=30),
                expiry_date__gte=today
            ).count(),
        }
        
        # Appointment statistics
        appointment_stats = {
            'upcoming_appointments': Appointment.objects.filter(
                appointment_date__gt=timezone.now(),
                status__in=['scheduled', 'confirmed']
            ).count(),
            'pending_appointments': Appointment.objects.filter(
                status='scheduled'
            ).count(),
            'emergency_records': MedicalRecord.objects.filter(
                is_emergency=True,
                created_at__date=today
            ).count(),
        }
        
        # Recent activity
        recent_activity = {
            'recent_appointments': AppointmentSummarySerializer(
                Appointment.objects.order_by('-created_at')[:5], many=True
            ).data,
            'recent_medical_records': MedicalRecordSummarySerializer(
                MedicalRecord.objects.order_by('-created_at')[:5], many=True
            ).data,
        }
        
        return Response({
            'basic_stats': basic_stats,
            'today_stats': today_stats,
            'medicine_stats': medicine_stats,
            'appointment_stats': appointment_stats,
            'recent_activity': recent_activity,
            'last_updated': timezone.now().isoformat()
        })

# Analytics View
class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get analytics data"""
        # Monthly appointment trends
        monthly_appointments = Appointment.objects.filter(
            appointment_date__month=timezone.now().month
        ).values('appointment_date__day').annotate(
            count=Count('id')
        ).order_by('appointment_date__day')
        
        # Doctor performance
        doctor_performance = Doctor.objects.annotate(
            total_appointments=Count('appointments'),
            completed_appointments=Count(
                'appointments',
                filter=Q(appointments__status='completed')
            )
        ).order_by('-total_appointments')[:10]
        
        # Popular medicines
        popular_medicines = Medicine.objects.annotate(
            prescription_count=Count('prescriptions')
        ).order_by('-prescription_count')[:10]
        
        return Response({
            'monthly_appointments': list(monthly_appointments),
            'top_doctors': DoctorSummarySerializer(doctor_performance, many=True).data,
            'popular_medicines': MedicineSummarySerializer(popular_medicines, many=True).data,
        })