from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView, LoginView, DashboardStatsView,
    DoctorViewSet, PatientViewSet, NurseViewSet, 
    AdminViewSet, PharmacistViewSet, DrugSupplierViewSet, 
    LabTechnicianViewSet, MedicationViewSet, AppointmentViewSet,
    PatientRecordViewSet, PrescriptionViewSet, VisitViewSet,
    LabResultViewSet,
    home, dashboard, doctors, patients, nurses, pharmacists, 
    lab_technicians, drug_suppliers, custom_login, custom_register, user_logout,
    appointment_view, medications_view, patient_record_view,
    appointment_create, appointment_update, appointment_delete, appointment_status,
    medication_create, medication_update, medication_delete,
    patient_record_create, patient_record_update, patient_record_delete
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
router.register(r'medications', MedicationViewSet, basename='medication')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'patient-records', PatientRecordViewSet, basename='patientrecord')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')
router.register(r'visits', VisitViewSet, basename='visit')
router.register(r'lab-results', LabResultViewSet, basename='labresult')

urlpatterns = [
    path('', home, name='home'),
    path('login/', custom_login, name='custom_login'),
    path('register/', custom_register, name='custom_register'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    
    # Entity management pages
    path('doctors/', doctors, name='doctors'),
    path('patients/', patients, name='patients'),
    path('nurses/', nurses, name='nurses'),
    path('pharmacists/', pharmacists, name='pharmacists'),
    path('lab-technicians/', lab_technicians, name='lab_technicians'),
    path('drug-suppliers/', drug_suppliers, name='drug_suppliers'),
    
    # Appointment management
    path('appointment/', appointment_view, name='appointment'),
    path('appointment/create/', appointment_create, name='appointment_create'),
    path('appointment/update/<int:appointment_id>/', appointment_update, name='appointment_update'),
    path('appointment/delete/<int:appointment_id>/', appointment_delete, name='appointment_delete'),
    path('appointment/status/<int:appointment_id>/', appointment_status, name='appointment_status'),
    
    # Medication management
    path('medications/', medications_view, name='medications'),
    path('medications/create/', medication_create, name='medication_create'),
    path('medications/update/<int:medication_id>/', medication_update, name='medication_update'),
    path('medications/delete/<int:medication_id>/', medication_delete, name='medication_delete'),
    
    # Patient records
    path('patient-record/', patient_record_view, name='patient_record'),
    path('patient-record/create/', patient_record_create, name='patient_record_create'),
    path('patient-record/update/<int:record_id>/', patient_record_update, name='patient_record_update'),
    path('patient-record/delete/<int:record_id>/', patient_record_delete, name='patient_record_delete'),
    
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Dashboard
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
    
    # API endpoints from router
    path('', include(router.urls)),
]
