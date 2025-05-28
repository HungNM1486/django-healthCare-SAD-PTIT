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
    LabTechnicianViewSet, home, dashboard, doctors, patients, nurses, pharmacists, 
    lab_technicians, drug_suppliers, custom_login, custom_register, user_logout
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
    path('', home, name='home'),
    path('login/', custom_login, name='custom_login'),
    path('register/', custom_register, name='custom_register'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('doctors/', doctors, name='doctors'),
    path('patients/', patients, name='patients'),
    path('nurses/', nurses, name='nurses'),
    path('pharmacists/', pharmacists, name='pharmacists'),
    path('lab-technicians/', lab_technicians, name='lab_technicians'),
    path('drug-suppliers/', drug_suppliers, name='drug_suppliers'),
    # Authentication endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Dashboard
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
    # API endpoints from router
    path('', include(router.urls)),
]
