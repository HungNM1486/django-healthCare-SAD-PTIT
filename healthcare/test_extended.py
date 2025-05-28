from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date, datetime, timedelta
from decimal import Decimal

from .models import (
    Doctor, Patient, Nurse, Admin, Pharmacist, DrugSupplier, LabTechnician,
    Medicine, Appointment, MedicalRecord, Prescription, LabTest
)

class BaseExtendedTestCase(APITestCase):
    """Base test case for extended models with authentication setup"""
    
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
        
        # Create test data
        self.create_test_data()
    
    def create_test_data(self):
        """Create basic test data"""
        # Create supplier
        self.supplier = DrugSupplier.objects.create(
            name='Test Supplier',
            contact_person='Test Contact',
            phone='+84-123-456-789',
            email='supplier@test.com',
            address='Test Address'
        )
        
        # Create doctor
        self.doctor = Doctor.objects.create(
            name='Dr. Test Doctor',
            specialization='Cardiology',
            phone='+84-123-456-789',
            email='doctor@test.com',
            license_number='MD001',
            consultation_fee=500000.00
        )
        
        # Create patient
        self.patient = Patient.objects.create(
            name='Test Patient',
            date_of_birth=date(1990, 1, 1),
            phone='+84-987-654-321',
            email='patient@test.com',
            address='Test Address',
            blood_type='A+'
        )
        
        # Create pharmacist
        self.pharmacist = Pharmacist.objects.create(
            name='Test Pharmacist',
            phone='+84-111-222-333',
            email='pharmacist@test.com'
        )
        
        # Create lab technician
        self.lab_tech = LabTechnician.objects.create(
            name='Test Lab Tech',
            phone='+84-333-444-555',
            email='labtech@test.com'
        )

class MedicineModelTestCase(TestCase):
    """Test Medicine model"""
    
    def setUp(self):
        self.supplier = DrugSupplier.objects.create(
            name='Test Supplier',
            contact_person='Test Contact',
            phone='+84-123-456-789',
            email='supplier@test.com',
            address='Test Address'
        )
        
        self.medicine = Medicine.objects.create(
            name='Test Medicine',
            generic_name='Test Generic',
            manufacturer='Test Manufacturer',
            dosage_form='tablet',
            strength='500mg',
            price_per_unit=Decimal('25000.00'),
            stock_quantity=100,
            minimum_stock_level=10,
            expiry_date=date.today() + timedelta(days=365),
            supplier=self.supplier,
            requires_prescription=True
        )
    
    def test_medicine_creation(self):
        """Test medicine creation"""
        self.assertEqual(self.medicine.name, 'Test Medicine')
        self.assertEqual(str(self.medicine), 'Test Medicine - 500mg')
    
    def test_is_low_stock(self):
        """Test low stock detection"""
        self.assertFalse(self.medicine.is_low_stock)
        
        self.medicine.stock_quantity = 5
        self.medicine.save()
        self.assertTrue(self.medicine.is_low_stock)
    
    def test_is_expired(self):
        """Test expiry detection"""
        self.assertFalse(self.medicine.is_expired)
        
        self.medicine.expiry_date = date.today() - timedelta(days=1)
        self.medicine.save()
        self.assertTrue(self.medicine.is_expired)
    
    def test_days_to_expire(self):
        """Test days to expiry calculation"""
        days = self.medicine.days_to_expire
        self.assertIsInstance(days, int)
        self.assertGreater(days, 0)

class AppointmentModelTestCase(TestCase):
    """Test Appointment model"""
    
    def setUp(self):
        self.doctor = Doctor.objects.create(
            name='Dr. Test',
            specialization='Cardiology',
            phone='+84-123-456-789',
            email='doctor@test.com'
        )
        
        self.patient = Patient.objects.create(
            name='Test Patient',
            date_of_birth=date(1990, 1, 1),
            phone='+84-987-654-321',
            email='patient@test.com',
            address='Test Address'
        )
        
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now() + timedelta(days=1),
            appointment_type='consultation',
            chief_complaint='Test complaint'
        )
    
    def test_appointment_creation(self):
        """Test appointment creation"""
        self.assertEqual(self.appointment.patient, self.patient)
        self.assertEqual(self.appointment.doctor, self.doctor)
        self.assertEqual(self.appointment.status, 'scheduled')
    
    def test_is_upcoming(self):
        """Test upcoming appointment detection"""
        self.assertTrue(self.appointment.is_upcoming)
        
        self.appointment.status = 'completed'
        self.appointment.save()
        self.assertFalse(self.appointment.is_upcoming)
    
    def test_can_be_cancelled(self):
        """Test cancellation eligibility"""
        self.assertTrue(self.appointment.can_be_cancelled())
        
        # Appointment too close (less than 2 hours)
        self.appointment.appointment_date = timezone.now() + timedelta(hours=1)
        self.appointment.save()
        self.assertFalse(self.appointment.can_be_cancelled())

class MedicalRecordModelTestCase(TestCase):
    """Test MedicalRecord model"""
    
    def setUp(self):
        self.doctor = Doctor.objects.create(
            name='Dr. Test',
            specialization='Cardiology',
            phone='+84-123-456-789',
            email='doctor@test.com'
        )
        
        self.patient = Patient.objects.create(
            name='Test Patient',
            date_of_birth=date(1990, 1, 1),
            phone='+84-987-654-321',
            email='patient@test.com',
            address='Test Address'
        )
        
        self.medical_record = MedicalRecord.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            symptoms='Test symptoms',
            diagnosis='Test diagnosis',
            treatment_plan='Test treatment',
            height=Decimal('175.0'),
            weight=Decimal('70.0'),
            blood_pressure_systolic=120,
            blood_pressure_diastolic=80
        )
    
    def test_medical_record_creation(self):
        """Test medical record creation"""
        self.assertEqual(self.medical_record.patient, self.patient)
        self.assertEqual(self.medical_record.doctor, self.doctor)
    
    def test_bmi_calculation(self):
        """Test BMI calculation"""
        bmi = self.medical_record.bmi
        self.assertIsNotNone(bmi)
        self.assertAlmostEqual(bmi, 22.86, places=2)
    
    def test_blood_pressure_format(self):
        """Test blood pressure formatting"""
        bp = self.medical_record.blood_pressure
        self.assertEqual(bp, "120/80")

class MedicineAPITestCase(BaseExtendedTestCase):
    """Test Medicine API endpoints"""
    
    def test_get_medicines_list(self):
        """Test getting list of medicines"""
        # Create test medicine
        Medicine.objects.create(
            name='Test Medicine',
            generic_name='Test Generic',
            manufacturer='Test Manufacturer',
            dosage_form='tablet',
            strength='500mg',
            price_per_unit=Decimal('25000.00'),
            stock_quantity=100,
            minimum_stock_level=10,
            expiry_date=date.today() + timedelta(days=365),
            supplier=self.supplier
        )
        
        url = reverse('medicine-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_medicine(self):
        """Test creating a new medicine"""
        url = reverse('medicine-list')
        data = {
            'name': 'New Medicine',
            'generic_name': 'New Generic',
            'manufacturer': 'New Manufacturer',
            'dosage_form': 'tablet',
            'strength': '250mg',
            'price_per_unit': '15000.00',
            'stock_quantity': 50,
            'minimum_stock_level': 5,
            'expiry_date': '2025-12-31',
            'supplier': self.supplier.id,
            'requires_prescription': True
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Medicine.objects.filter(name='New Medicine').exists())
    
    def test_low_stock_medicines(self):
        """Test low stock medicines endpoint"""
        # Create low stock medicine
        Medicine.objects.create(
            name='Low Stock Medicine',
            manufacturer='Test Manufacturer',
            dosage_form='tablet',
            strength='500mg',
            price_per_unit=Decimal('25000.00'),
            stock_quantity=5,
            minimum_stock_level=10,
            expiry_date=date.today() + timedelta(days=365),
            supplier=self.supplier
        )
        
        url = reverse('medicine-low-stock')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_adjust_stock(self):
        """Test stock adjustment"""
        medicine = Medicine.objects.create(
            name='Stock Test Medicine',
            manufacturer='Test Manufacturer',
            dosage_form='tablet',
            strength='500mg',
            price_per_unit=Decimal('25000.00'),
            stock_quantity=100,
            minimum_stock_level=10,
            expiry_date=date.today() + timedelta(days=365),
            supplier=self.supplier
        )
        
        url = reverse('medicine-adjust-stock', kwargs={'pk': medicine.pk})
        data = {
            'adjustment': -20,
            'reason': 'Dispensed to patients'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        medicine.refresh_from_db()
        self.assertEqual(medicine.stock_quantity, 80)

class AppointmentAPITestCase(BaseExtendedTestCase):
    """Test Appointment API endpoints"""
    
    def test_create_appointment(self):
        """Test creating a new appointment"""
        url = reverse('appointment-list')
        future_date = (timezone.now() + timedelta(days=2)).isoformat()
        
        data = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'appointment_date': future_date,
            'appointment_type': 'consultation',
            'chief_complaint': 'Test complaint',
            'duration_minutes': 30
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_today_appointments(self):
        """Test getting today's appointments"""
        # Create today's appointment
        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now().replace(hour=14, minute=0),
            appointment_type='consultation',
            chief_complaint='Today appointment'
        )
        
        url = reverse('appointment-today')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_cancel_appointment(self):
        """Test cancelling an appointment"""
        appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now() + timedelta(days=1),
            appointment_type='consultation',
            chief_complaint='Test complaint'
        )
        
        url = reverse('appointment-cancel', kwargs={'pk': appointment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        appointment.refresh_from_db()
        self.assertEqual(appointment.status, 'cancelled')
    
    def test_appointment_conflict_validation(self):
        """Test appointment conflict validation"""
        appointment_time = timezone.now() + timedelta(days=1)
        
        # Create first appointment
        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=appointment_time,
            appointment_type='consultation',
            chief_complaint='First appointment'
        )
        
        # Try to create conflicting appointment
        url = reverse('appointment-list')
        data = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'appointment_date': appointment_time.isoformat(),
            'appointment_type': 'consultation',
            'chief_complaint': 'Conflicting appointment'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class MedicalRecordAPITestCase(BaseExtendedTestCase):
    """Test Medical Record API endpoints"""
    
    def setUp(self):
        super().setUp()
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now() - timedelta(hours=2),
            appointment_type='consultation',
            status='completed',
            chief_complaint='Test complaint'
        )
    
    def test_create_medical_record(self):
        """Test creating a medical record"""
        url = reverse('medicalrecord-list')
        data = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'appointment': self.appointment.id,
            'temperature': '37.5',
            'blood_pressure_systolic': 130,
            'blood_pressure_diastolic': 85,
            'heart_rate': 80,
            'weight': '70.5',
            'height': '175.0',
            'symptoms': 'Fever and headache',
            'diagnosis': 'Viral infection',
            'treatment_plan': 'Rest and medication',
            'prescription': 'Paracetamol 500mg twice daily'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_emergency_cases(self):
        """Test getting emergency cases"""
        # Create emergency medical record
        MedicalRecord.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            symptoms='Chest pain',
            diagnosis='Acute myocardial infarction',
            treatment_plan='Emergency treatment',
            is_emergency=True
        )
        
        url = reverse('medicalrecord-emergency-cases')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class PrescriptionAPITestCase(BaseExtendedTestCase):
    """Test Prescription API endpoints"""
    
    def setUp(self):
        super().setUp()
        self.medicine = Medicine.objects.create(
            name='Test Medicine',
            manufacturer='Test Manufacturer',
            dosage_form='tablet',
            strength='500mg',
            price_per_unit=Decimal('25000.00'),
            stock_quantity=100,
            minimum_stock_level=10,
            expiry_date=date.today() + timedelta(days=365),
            supplier=self.supplier
        )
        
        self.medical_record = MedicalRecord.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            symptoms='Test symptoms',
            diagnosis='Test diagnosis',
            treatment_plan='Test treatment'
        )
    
    def test_create_prescription(self):
        """Test creating a prescription"""
        url = reverse('prescription-list')
        data = {
            'medical_record': self.medical_record.id,
            'medicine': self.medicine.id,
            'dosage': '1 tablet twice daily',
            'duration_days': 7,
            'quantity': 14,
            'instructions': 'Take with food'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_fill_prescription(self):
        """Test filling a prescription"""
        prescription = Prescription.objects.create(
            medical_record=self.medical_record,
            medicine=self.medicine,
            dosage='1 tablet twice daily',
            duration_days=7,
            quantity=14
        )
        
        url = reverse('prescription-fill', kwargs={'pk': prescription.pk})
        data = {'pharmacist_id': self.pharmacist.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        prescription.refresh_from_db()
        self.assertTrue(prescription.is_filled)
        self.assertEqual(prescription.filled_by, self.pharmacist)

class DashboardStatsAPITestCase(BaseExtendedTestCase):
    """Test Dashboard Statistics API"""
    
    def test_dashboard_stats(self):
        """Test dashboard statistics endpoint"""
        # Create some test data
        Medicine.objects.create(
            name='Test Medicine',
            manufacturer='Test Manufacturer',
            dosage_form='tablet',
            strength='500mg',
            price_per_unit=Decimal('25000.00'),
            stock_quantity=5,  # Low stock
            minimum_stock_level=10,
            expiry_date=date.today() + timedelta(days=10),  # Expiring soon
            supplier=self.supplier
        )
        
        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            appointment_date=timezone.now().replace(hour=14, minute=0),
            appointment_type='consultation',
            chief_complaint='Today appointment'
        )
        
        url = reverse('dashboard_stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_keys = [
            'basic_stats', 'today_stats', 'medicine_stats', 
            'appointment_stats', 'recent_activity'
        ]
        for key in expected_keys:
            self.assertIn(key, response.data)
        
        # Check specific values
        self.assertEqual(response.data['basic_stats']['total_doctors'], 1)
        self.assertEqual(response.data['basic_stats']['total_patients'], 1)
        self.assertEqual(response.data['medicine_stats']['low_stock_medicines'], 1)
        self.assertEqual(response.data['medicine_stats']['expiring_soon_medicines'], 1)

class ValidationTestCase(BaseExtendedTestCase):
    """Test model validations"""
    
    def test_medicine_price_validation(self):
        """Test medicine price validation"""
        url = reverse('medicine-list')
        data = {
            'name': 'Invalid Medicine',
            'manufacturer': 'Test Manufacturer',
            'dosage_form': 'tablet',
            'strength': '500mg',
            'price_per_unit': '-100.00',  # Invalid negative price
            'stock_quantity': 100,
            'minimum_stock_level': 10,
            'expiry_date': '2025-12-31',
            'supplier': self.supplier.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price_per_unit', response.data)
    
    def test_appointment_past_date_validation(self):
        """Test appointment past date validation"""
        url = reverse('appointment-list')
        past_date = (timezone.now() - timedelta(days=1)).isoformat()
        
        data = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'appointment_date': past_date,
            'appointment_type': 'consultation',
            'chief_complaint': 'Test complaint'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_medical_record_temperature_validation(self):
        """Test medical record temperature validation"""
        url = reverse('medicalrecord-list')
        data = {
            'patient': self.patient.id,
            'doctor': self.doctor.id,
            'temperature': '60.0',  # Invalid temperature
            'symptoms': 'Test symptoms',
            'diagnosis': 'Test diagnosis',
            'treatment_plan': 'Test treatment'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('temperature', response.data)

# Run tests with: python manage.py test healthcare.test_extended