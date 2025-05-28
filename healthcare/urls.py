from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    # Authentication Views
    RegisterView, LoginView,
    
    # Dashboard and Analytics
    DashboardStatsView, AnalyticsView,
    
    # Core Entity ViewSets
    DoctorViewSet, PatientViewSet, NurseViewSet, 
    AdminViewSet, PharmacistViewSet, DrugSupplierViewSet, 
    LabTechnicianViewSet,
    
    # New ViewSets
    MedicineViewSet, AppointmentViewSet, MedicalRecordViewSet,
    PrescriptionViewSet, LabTestViewSet
)

# Create router and register ViewSets
router = DefaultRouter()

# Core entities
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'nurses', NurseViewSet, basename='nurse')
router.register(r'admins', AdminViewSet, basename='admin')
router.register(r'pharmacists', PharmacistViewSet, basename='pharmacist')
router.register(r'drug-suppliers', DrugSupplierViewSet, basename='drugsupplier')
router.register(r'lab-technicians', LabTechnicianViewSet, basename='labtechnician')

# New entities
router.register(r'medicines', MedicineViewSet, basename='medicine')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'medical-records', MedicalRecordViewSet, basename='medicalrecord')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')
router.register(r'lab-tests', LabTestViewSet, basename='labtest')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/legacy-login/', LoginView.as_view(), name='legacy_login'),  # Keep for compatibility
    
    # Dashboard and Analytics
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    
    # API endpoints from router
    path('', include(router.urls)),
]

# API Documentation (optional - for development)
from rest_framework.documentation import include_docs_urls

urlpatterns += [
    path('docs/', include_docs_urls(title='Hospital Management API')),
]

# Additional custom endpoints can be added here
custom_patterns = [
    # Custom views that don't fit into ViewSets can be added here
    # Example: path('custom-reports/', CustomReportView.as_view(), name='custom_reports'),
]

urlpatterns += custom_patterns

# API Endpoints Reference:
"""
Authentication:
- POST /api/healthcare/auth/register/ - User registration
- POST /api/healthcare/auth/login/ - Login (JWT token)
- POST /api/healthcare/auth/token/refresh/ - Refresh token

Core Entities:
- /api/healthcare/doctors/ - Doctor CRUD + custom actions
  - GET /api/healthcare/doctors/specializations/ - List specializations
  - GET /api/healthcare/doctors/available_today/ - Available doctors today
  - GET /api/healthcare/doctors/{id}/schedule/ - Doctor schedule
  - POST /api/healthcare/doctors/{id}/toggle_availability/ - Toggle availability

- /api/healthcare/patients/ - Patient CRUD + custom actions
  - GET /api/healthcare/patients/search_by_phone/ - Search by phone
  - GET /api/healthcare/patients/blood_type_stats/ - Blood type statistics
  - GET /api/healthcare/patients/{id}/medical_history/ - Medical history

- /api/healthcare/medicines/ - Medicine CRUD + custom actions
  - GET /api/healthcare/medicines/low_stock/ - Low stock medicines
  - GET /api/healthcare/medicines/expiring_soon/ - Expiring medicines
  - POST /api/healthcare/medicines/bulk_update_stock/ - Bulk stock update
  - POST /api/healthcare/medicines/{id}/adjust_stock/ - Adjust stock

- /api/healthcare/appointments/ - Appointment CRUD + custom actions
  - GET /api/healthcare/appointments/today/ - Today's appointments
  - GET /api/healthcare/appointments/upcoming/ - Upcoming appointments
  - POST /api/healthcare/appointments/{id}/cancel/ - Cancel appointment
  - POST /api/healthcare/appointments/{id}/complete/ - Complete appointment
  - POST /api/healthcare/appointments/bulk_create/ - Bulk create appointments

- /api/healthcare/medical-records/ - Medical Record CRUD + custom actions
  - GET /api/healthcare/medical-records/emergency_cases/ - Emergency cases
  - GET /api/healthcare/medical-records/follow_up_required/ - Follow-up required

- /api/healthcare/prescriptions/ - Prescription CRUD + custom actions
  - POST /api/healthcare/prescriptions/{id}/fill/ - Fill prescription

- /api/healthcare/lab-tests/ - Lab Test CRUD + custom actions
  - POST /api/healthcare/lab-tests/{id}/complete/ - Complete test

Dashboard & Analytics:
- GET /api/healthcare/dashboard/stats/ - Dashboard statistics
- GET /api/healthcare/analytics/ - Analytics data

Query Parameters (available for most endpoints):
- search - Search in relevant fields
- page - Page number for pagination
- page_size - Items per page (max 100)
- ordering - Sort by field (add '-' for descending)
- Various filters specific to each model

Examples:
- GET /api/healthcare/doctors/?search=cardiology&available_only=true
- GET /api/healthcare/patients/?min_age=18&max_age=65
- GET /api/healthcare/medicines/?stock_status=low
- GET /api/healthcare/appointments/?today_only=true&status=scheduled
- GET /api/healthcare/medical-records/?is_emergency=true
"""