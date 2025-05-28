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
