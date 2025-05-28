from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date

from .models import Doctor, Patient, Nurse, Admin, Pharmacist, DrugSupplier, LabTechnician

class BaseAPITestCase(APITestCase):
    """Base test case with authentication setup"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com'
        )
        self.client = APIClient()
        
        # Get JWT token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Set authentication header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

class AuthenticationTestCase(APITestCase):
    """Test authentication endpoints"""
    
    def test_user_registration(self):
        """Test user registration"""
        url = reverse('register')
        data = {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'newuser@test.com',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_jwt_token_obtain(self):
        """Test JWT token generation"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class DoctorAPITestCase(BaseAPITestCase):
    """Test Doctor API endpoints"""
    
    def setUp(self):
        super().setUp()
        self.doctor_data = {
            'name': 'Dr. Test Doctor',
            'specialization': 'Cardiology',
            'phone': '+84-123-456-789',
            'email': 'doctor@test.com'
        }
        self.doctor = Doctor.objects.create(**self.doctor_data)

    def test_get_doctors_list(self):
        """Test getting list of doctors"""
        url = reverse('doctor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_doctor(self):
        """Test creating a new doctor"""
        url = reverse('doctor-list')
        new_doctor_data = {
            'name': 'Dr. New Doctor',
            'specialization': 'Pediatrics',
            'phone': '+84-123-456-790',
            'email': 'newdoctor@test.com'
        }
        response = self.client.post(url, new_doctor_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Doctor.objects.filter(email=new_doctor_data['email']).exists())

    def test_get_doctor_detail(self):
        """Test getting doctor detail"""
        url = reverse('doctor-detail', kwargs={'pk': self.doctor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.doctor.name)

    def test_update_doctor(self):
        """Test updating doctor information"""
        url = reverse('doctor-detail', kwargs={'pk': self.doctor.pk})
        updated_data = {
            'name': 'Dr. Updated Doctor',
            'specialization': 'Neurology',
            'phone': self.doctor.phone,
            'email': self.doctor.email
        }
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.name, updated_data['name'])

    def test_delete_doctor(self):
        """Test deleting doctor"""
        url = reverse('doctor-detail', kwargs={'pk': self.doctor.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Doctor.objects.filter(pk=self.doctor.pk).exists())

    def test_search_doctors(self):
        """Test searching doctors"""
        url = reverse('doctor-list')
        response = self.client.get(url, {'search': 'Cardiology'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_filter_doctors_by_specialization(self):
        """Test filtering doctors by specialization"""
        url = reverse('doctor-list')
        response = self.client.get(url, {'specialization': 'Cardiology'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_get_specializations(self):
        """Test getting list of specializations"""
        url = reverse('doctor-specializations')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Cardiology', response.data['specializations'])

class PatientAPITestCase(BaseAPITestCase):
    """Test Patient API endpoints"""
    
    def setUp(self):
        super().setUp()
        self.patient_data = {
            'name': 'Test Patient',
            'date_of_birth': date(1990, 1, 1),
            'phone': '+84-987-654-321',
            'email': 'patient@test.com',
            'address': 'Test Address'
        }
        self.patient = Patient.objects.create(**self.patient_data)

    def test_get_patients_list(self):
        """Test getting list of patients"""
        url = reverse('patient-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_patient(self):
        """Test creating a new patient"""
        url = reverse('patient-list')
        new_patient_data = {
            'name': 'New Patient',
            'date_of_birth': '1985-05-15',
            'phone': '+84-987-654-322',
            'email': 'newpatient@test.com',
            'address': 'New Address'
        }
        response = self.client.post(url, new_patient_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Patient.objects.filter(email=new_patient_data['email']).exists())

    def test_patient_age_calculation(self):
        """Test patient age calculation in serializer"""
        url = reverse('patient-detail', kwargs={'pk': self.patient.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Patient born in 1990, so age should be around 34-35 (depending on current date)
        self.assertGreaterEqual(response.data['age'], 30)

    def test_search_patient_by_phone(self):
        """Test searching patient by phone number"""
        url = reverse('patient-search-by-phone')
        response = self.client.get(url, {'phone': '987-654-321'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_invalid_date_of_birth(self):
        """Test validation for future date of birth"""
        url = reverse('patient-list')
        invalid_data = {
            'name': 'Invalid Patient',
            'date_of_birth': '2030-01-01',  # Future date
            'phone': '+84-987-654-323',
            'email': 'invalid@test.com',
            'address': 'Test Address'
        }
        response = self.client.post(url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class NurseAPITestCase(BaseAPITestCase):
    """Test Nurse API endpoints"""
    
    def setUp(self):
        super().setUp()
        self.nurse_data = {
            'name': 'Test Nurse',
            'phone': '+84-111-222-333',
            'email': 'nurse@test.com'
        }
        self.nurse = Nurse.objects.create(**self.nurse_data)

    def test_get_nurses_list(self):
        """Test getting list of nurses"""
        url = reverse('nurse-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_nurse(self):
        """Test creating a new nurse"""
        url = reverse('nurse-list')
        new_nurse_data = {
            'name': 'New Nurse',
            'phone': '+84-111-222-334',
            'email': 'newnurse@test.com'
        }
        response = self.client.post(url, new_nurse_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class EmailValidationTestCase(BaseAPITestCase):
    """Test email validation across all models"""
    
    def test_duplicate_doctor_email(self):
        """Test that duplicate doctor email is rejected"""
        Doctor.objects.create(
            name='First Doctor',
            specialization='Cardiology',
            phone='+84-123-456-789',
            email='duplicate@test.com'
        )
        
        url = reverse('doctor-list')
        data = {
            'name': 'Second Doctor',
            'specialization': 'Pediatrics',
            'phone': '+84-123-456-790',
            'email': 'duplicate@test.com'  # Same email
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

class DashboardStatsTestCase(BaseAPITestCase):
    """Test dashboard statistics endpoint"""
    
    def setUp(self):
        super().setUp()
        # Create sample data
        Doctor.objects.create(name='Dr. Test', specialization='Cardiology', phone='+84-123-456-789', email='doctor@test.com')
        Patient.objects.create(name='Test Patient', date_of_birth=date(1990, 1, 1), phone='+84-987-654-321', email='patient@test.com', address='Test Address')
        Nurse.objects.create(name='Test Nurse', phone='+84-111-222-333', email='nurse@test.com')

    def test_dashboard_stats(self):
        """Test dashboard statistics"""
        url = reverse('dashboard_stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_keys = [
            'total_doctors', 'total_patients', 'total_nurses',
            'total_pharmacists', 'total_lab_technicians', 
            'total_drug_suppliers', 'specializations_count'
        ]
        
        for key in expected_keys:
            self.assertIn(key, response.data)
        
        self.assertEqual(response.data['total_doctors'], 1)
        self.assertEqual(response.data['total_patients'], 1)
        self.assertEqual(response.data['total_nurses'], 1)

class APIAuthenticationTestCase(APITestCase):
    """Test API authentication requirements"""
    
    def test_unauthenticated_access_denied(self):
        """Test that unauthenticated requests are denied"""
        url = reverse('doctor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_access_allowed(self):
        """Test that authenticated requests are allowed"""
        user = User.objects.create_user(username='testuser', password='testpass123')
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url = reverse('doctor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# Run tests with: python manage.py test healthcare.tests