import os
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    home, custom_login, custom_register, user_logout, dashboard,
    doctors, patients, nurses, pharmacists, lab_technicians, drug_suppliers,
    doctor_create, doctor_update, doctor_delete, patient_create, patient_update, 
    patient_delete, patient_detail,
    appointment_view, appointment_create, appointment_update, appointment_delete, appointment_status,
    medications_view, medication_create, medication_update, medication_delete,
    patient_record_view, patient_record_create, patient_record_update, patient_record_delete,
    DoctorViewSet, PatientViewSet, NurseViewSet, AdminViewSet, PharmacistViewSet,
    DrugSupplierViewSet, LabTechnicianViewSet, MedicationViewSet, AppointmentViewSet,
    PatientRecordViewSet, PrescriptionViewSet, VisitViewSet, LabResultViewSet,
    DashboardStatsView, RegisterView, LoginView
)

# Create router for ViewSets (REST API)
router = DefaultRouter()
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'nurses', NurseViewSet)
router.register(r'admins', AdminViewSet)
router.register(r'pharmacists', PharmacistViewSet)
router.register(r'drug-suppliers', DrugSupplierViewSet)
router.register(r'lab-technicians', LabTechnicianViewSet)
router.register(r'medications', MedicationViewSet)
router.register(r'appointment', AppointmentViewSet)
router.register(r'patient-record', PatientRecordViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'visits', VisitViewSet)
router.register(r'lab-results', LabResultViewSet)

urlpatterns = [
    # Authentication and Dashboard
    path('', home, name='home'),
    path('login/', custom_login, name='custom_login'), 
    path('register/', custom_register, name='custom_register'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
      # API Authentication endpoints
    path('auth/login/', LoginView.as_view(), name='api_login'),
    path('auth/register/', RegisterView.as_view(), name='api_register'),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
    
    # Staff Management Views
    path('doctors/', doctors, name='doctors'),
    path('patients/', patients, name='patients'),
    path('nurses/', nurses, name='nurses'),
    path('pharmacists/', pharmacists, name='pharmacists'),
    path('lab-technicians/', lab_technicians, name='lab_technicians'),
    path('drug-suppliers/', drug_suppliers, name='drug_suppliers'),
    
    # Doctor CRUD Operations
    path('doctors/create/', doctor_create, name='doctor_create'),
    path('doctors/<int:doctor_id>/update/', doctor_update, name='doctor_update'),
    path('doctors/<int:doctor_id>/delete/', doctor_delete, name='doctor_delete'),
    
    # Patient CRUD Operations
    path('patients/create/', patient_create, name='patient_create'),
    path('patients/<int:patient_id>/update/', patient_update, name='patient_update'),
    path('patients/<int:patient_id>/delete/', patient_delete, name='patient_delete'),
    path('patients/<int:patient_id>/', patient_detail, name='patient_detail'),
    
    # Appointment Management
    path('appointments/', appointment_view, name='appointment_view'),
    path('appointments/create/', appointment_create, name='appointment_create'),
    path('appointments/<int:appointment_id>/update/', appointment_update, name='appointment_update'),
    path('appointments/<int:appointment_id>/delete/', appointment_delete, name='appointment_delete'),
    path('appointments/<int:appointment_id>/status/', appointment_status, name='appointment_status'),
    
    # Medication Management
    path('medications/', medications_view, name='medications_view'),
    path('medications/create/', medication_create, name='medication_create'),
    path('medications/<int:medication_id>/update/', medication_update, name='medication_update'),
    path('medications/<int:medication_id>/delete/', medication_delete, name='medication_delete'),
    
    # Patient Record Management
    path('patient-records/', patient_record_view, name='patient_record_view'),
    path('patient-records/create/', patient_record_create, name='patient_record_create'),
    path('patient-records/<int:record_id>/update/', patient_record_update, name='patient_record_update'),
    path('patient-records/<int:record_id>/delete/', patient_record_delete, name='patient_record_delete'),
    
    # Include API router URLs
    path('', include(router.urls)),
]