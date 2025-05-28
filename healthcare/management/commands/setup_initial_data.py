from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta, datetime
from healthcare.models import (
    Doctor, Patient, Nurse, Admin, Pharmacist, DrugSupplier, LabTechnician,
    Medicine, Appointment, MedicalRecord, Prescription, LabTest
)

class Command(BaseCommand):
    help = 'Setup extended data for the hospital management system (Week 2 models)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing extended data before creating new data',
        )
        parser.add_argument(
            '--skip-basic',
            action='store_true',
            help='Skip creating basic entities (doctors, patients, etc.)',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing extended data...')
            LabTest.objects.all().delete()
            Prescription.objects.all().delete()
            MedicalRecord.objects.all().delete()
            Appointment.objects.all().delete()
            Medicine.objects.all().delete()
            self.stdout.write(self.style.WARNING('✓ Extended data cleared'))

        if not options['skip_basic']:
            self.create_basic_entities()
        
        self.create_medicines()
        self.create_appointments()
        self.create_medical_records()
        self.create_prescriptions()
        self.create_lab_tests()
        
        self.stdout.write(
            self.style.SUCCESS('\n🎉 Extended data setup completed successfully!')
        )

    def create_basic_entities(self):
        """Create basic entities if they don't exist"""
        self.stdout.write('\n📋 Setting up basic entities...')
        
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@hospital.com',
                password='admin123',
                first_name='System',
                last_name='Administrator'
            )
            self.stdout.write('✓ Superuser created: admin/admin123')

        # Create doctors
        doctors_data = [
            {
                'name': 'Dr. Nguyễn Văn Nam',
                'specialization': 'Cardiology',
                'phone': '+84-123-456-789',
                'email': 'nam.nguyen@hospital.com',
                'license_number': 'MD001',
                'years_of_experience': 15,
                'consultation_fee': 500000.00
            },
            {
                'name': 'Dr. Trần Thị Mai',
                'specialization': 'Pediatrics',
                'phone': '+84-123-456-790',
                'email': 'mai.tran@hospital.com',
                'license_number': 'MD002',
                'years_of_experience': 12,
                'consultation_fee': 400000.00
            },
            {
                'name': 'Dr. Lê Minh Tuấn',
                'specialization': 'Orthopedics',
                'phone': '+84-123-456-791',
                'email': 'tuan.le@hospital.com',
                'license_number': 'MD003',
                'years_of_experience': 18,
                'consultation_fee': 600000.00
            },
        ]

        for doctor_data in doctors_data:
            doctor, created = Doctor.objects.get_or_create(
                email=doctor_data['email'],
                defaults=doctor_data
            )
            if created:
                self.stdout.write(f'✓ Created doctor: {doctor.name}')

        # Create patients
        patients_data = [
            {
                'name': 'Nguyễn Văn An',
                'date_of_birth': date(1985, 3, 15),
                'phone': '+84-987-654-321',
                'email': 'an.nguyen@email.com',
                'address': '123 Đường ABC, Quận 1, TP.HCM',
                'blood_type': 'A+',
                'allergies': 'Penicillin',
                'emergency_contact_name': 'Nguyễn Thị Bình',
                'emergency_contact_phone': '+84-987-654-322'
            },
            {
                'name': 'Trần Thị Bình',
                'date_of_birth': date(1990, 7, 22),
                'phone': '+84-987-654-323',
                'email': 'binh.tran@email.com',
                'address': '456 Đường XYZ, Quận 2, TP.HCM',
                'blood_type': 'B+',
                'emergency_contact_name': 'Trần Văn Cường',
                'emergency_contact_phone': '+84-987-654-324'
            },
            {
                'name': 'Lê Văn Cường',
                'date_of_birth': date(1978, 12, 10),
                'phone': '+84-987-654-325',
                'email': 'cuong.le@email.com',
                'address': '789 Đường DEF, Quận 3, TP.HCM',
                'blood_type': 'O+',
                'allergies': 'Aspirin, Shellfish',
                'emergency_contact_name': 'Lê Thị Dung',
                'emergency_contact_phone': '+84-987-654-326'
            },
        ]

        for patient_data in patients_data:
            patient, created = Patient.objects.get_or_create(
                email=patient_data['email'],
                defaults=patient_data
            )
            if created:
                self.stdout.write(f'✓ Created patient: {patient.name}')

        # Create other staff
        nurse_data = {
            'name': 'Y tá Nguyễn Thị Lan',
            'phone': '+84-111-222-333',
            'email': 'lan.nurse@hospital.com',
            'license_number': 'RN001',
            'department': 'Emergency',
            'shift_type': 'morning'
        }
        nurse, created = Nurse.objects.get_or_create(
            email=nurse_data['email'],
            defaults=nurse_data
        )
        if created:
            self.stdout.write(f'✓ Created nurse: {nurse.name}')

        pharmacist_data = {
            'name': 'Dược sĩ Lê Thị Hương',
            'phone': '+84-222-333-444',
            'email': 'huong.pharmacist@hospital.com',
            'license_number': 'RPh001'
        }
        pharmacist, created = Pharmacist.objects.get_or_create(
            email=pharmacist_data['email'],
            defaults=pharmacist_data
        )
        if created:
            self.stdout.write(f'✓ Created pharmacist: {pharmacist.name}')

        lab_tech_data = {
            'name': 'KTV Phạm Văn Đức',
            'phone': '+84-333-444-555',
            'email': 'duc.labtech@hospital.com',
            'license_number': 'LT001',
            'specialization': 'Hematology'
        }
        lab_tech, created = LabTechnician.objects.get_or_create(
            email=lab_tech_data['email'],
            defaults=lab_tech_data
        )
        if created:
            self.stdout.write(f'✓ Created lab technician: {lab_tech.name}')

        # Create drug supplier
        supplier_data = {
            'name': 'Công ty Dược phẩm ABC',
            'contact_person': 'Nguyễn Văn Kinh',
            'phone': '+84-444-555-666',
            'email': 'abc.pharma@company.com',
            'address': '100 Đường Công nghiệp, Quận 9, TP.HCM',
            'license_number': 'DS001'
        }
        supplier, created = DrugSupplier.objects.get_or_create(
            email=supplier_data['email'],
            defaults=supplier_data
        )
        if created:
            self.stdout.write(f'✓ Created drug supplier: {supplier.name}')

    def create_medicines(self):
        """Create sample medicines"""
        self.stdout.write('\n💊 Creating medicines...')
        
        supplier = DrugSupplier.objects.first()
        if not supplier:
            self.stdout.write(self.style.ERROR('No drug supplier found. Creating one...'))
            supplier = DrugSupplier.objects.create(
                name='Default Supplier',
                contact_person='Contact Person',
                phone='+84-000-000-000',
                email='default@supplier.com',
                address='Default Address'
            )
        
        medicines_data = [
            {
                'name': 'Paracetamol',
                'generic_name': 'Acetaminophen',
                'manufacturer': 'Pharma Company A',
                'description': 'Pain reliever and fever reducer',
                'dosage_form': 'tablet',
                'strength': '500mg',
                'price_per_unit': 2000.00,
                'stock_quantity': 1000,
                'minimum_stock_level': 100,
                'expiry_date': date.today() + timedelta(days=365),
                'supplier': supplier,
                'requires_prescription': False,
                'side_effects': 'Rare: skin rash, nausea',
                'storage_instructions': 'Store in cool, dry place'
            },
            {
                'name': 'Amoxicillin',
                'generic_name': 'Amoxicillin',
                'manufacturer': 'Pharma Company B',
                'description': 'Antibiotic for bacterial infections',
                'dosage_form': 'capsule',
                'strength': '250mg',
                'price_per_unit': 15000.00,
                'stock_quantity': 500,
                'minimum_stock_level': 50,
                'expiry_date': date.today() + timedelta(days=730),
                'supplier': supplier,
                'requires_prescription': True,
                'side_effects': 'Nausea, diarrhea, allergic reactions',
                'contraindications': 'Penicillin allergy',
                'storage_instructions': 'Store below 25°C'
            },
            {
                'name': 'Omeprazole',
                'generic_name': 'Omeprazole',
                'manufacturer': 'Pharma Company C',
                'description': 'Proton pump inhibitor for acid reflux',
                'dosage_form': 'capsule',
                'strength': '20mg',
                'price_per_unit': 25000.00,
                'stock_quantity': 200,
                'minimum_stock_level': 30,
                'expiry_date': date.today() + timedelta(days=500),
                'supplier': supplier,
                'requires_prescription': True,
                'side_effects': 'Headache, stomach pain',
                'storage_instructions': 'Store in original container'
            },
            {
                'name': 'Vitamin D3',
                'generic_name': 'Cholecalciferol',
                'manufacturer': 'Vitamin Company',
                'description': 'Vitamin D supplement',
                'dosage_form': 'tablet',
                'strength': '1000 IU',
                'price_per_unit': 8000.00,
                'stock_quantity': 300,
                'minimum_stock_level': 50,
                'expiry_date': date.today() + timedelta(days=800),
                'supplier': supplier,
                'requires_prescription': False,
                'storage_instructions': 'Store away from light'
            },
            {
                'name': 'Insulin',
                'generic_name': 'Human Insulin',
                'manufacturer': 'Diabetes Care Inc',
                'description': 'Injectable insulin for diabetes',
                'dosage_form': 'injection',
                'strength': '100 units/ml',
                'price_per_unit': 350000.00,
                'stock_quantity': 50,
                'minimum_stock_level': 10,
                'expiry_date': date.today() + timedelta(days=365),
                'supplier': supplier,
                'requires_prescription': True,
                'side_effects': 'Hypoglycemia, injection site reactions',
                'storage_instructions': 'Refrigerate at 2-8°C'
            }
        ]

        for medicine_data in medicines_data:
            medicine, created = Medicine.objects.get_or_create(
                name=medicine_data['name'],
                strength=medicine_data['strength'],
                defaults=medicine_data
            )
            if created:
                self.stdout.write(f'✓ Created medicine: {medicine.name} - {medicine.strength}')

    def create_appointments(self):
        """Create sample appointments"""
        self.stdout.write('\n📅 Creating appointments...')
        
        doctors = list(Doctor.objects.all())
        patients = list(Patient.objects.all())
        
        if not doctors or not patients:
            self.stdout.write(self.style.ERROR('Need doctors and patients to create appointments'))
            return
        
        # Create appointments for different dates
        base_date = timezone.now().replace(hour=9, minute=0, second=0, microsecond=0)
        
        appointments_data = [
            {
                'patient': patients[0],
                'doctor': doctors[0],
                'appointment_date': base_date + timedelta(days=1),
                'appointment_type': 'consultation',
                'status': 'scheduled',
                'duration_minutes': 30,
                'chief_complaint': 'Chest pain and shortness of breath'
            },
            {
                'patient': patients[1],
                'doctor': doctors[1],
                'appointment_date': base_date + timedelta(days=1, hours=2),
                'appointment_type': 'routine_checkup',
                'status': 'scheduled',
                'duration_minutes': 45,
                'chief_complaint': 'Annual pediatric checkup'
            },
            {
                'patient': patients[2],
                'doctor': doctors[2],
                'appointment_date': base_date + timedelta(days=2),
                'appointment_type': 'follow_up',
                'status': 'confirmed',
                'duration_minutes': 30,
                'chief_complaint': 'Follow-up for knee surgery'
            },
            {
                'patient': patients[0],
                'doctor': doctors[0],
                'appointment_date': base_date - timedelta(days=7),
                'appointment_type': 'consultation',
                'status': 'completed',
                'duration_minutes': 45,
                'chief_complaint': 'Hypertension follow-up',
                'notes': 'Blood pressure stable, continue medication'
            },
            {
                'patient': patients[1],
                'doctor': doctors[0],
                'appointment_date': base_date - timedelta(days=3),
                'appointment_type': 'emergency',
                'status': 'completed',
                'duration_minutes': 60,
                'chief_complaint': 'Severe headache',
                'notes': 'Migraine episode, prescribed medication'
            }
        ]

        for appointment_data in appointments_data:
            appointment = Appointment.objects.create(**appointment_data)
            self.stdout.write(f'✓ Created appointment: {appointment.patient.name} - {appointment.doctor.name} - {appointment.appointment_date.strftime("%Y-%m-%d %H:%M")}')

    def create_medical_records(self):
        """Create sample medical records"""
        self.stdout.write('\n📋 Creating medical records...')
        
        completed_appointments = Appointment.objects.filter(status='completed')
        
        if not completed_appointments.exists():
            self.stdout.write(self.style.WARNING('No completed appointments found. Skipping medical records.'))
            return
        
        for appointment in completed_appointments:
            medical_record_data = {
                'patient': appointment.patient,
                'doctor': appointment.doctor,
                'appointment': appointment,
                'temperature': 37.2,
                'blood_pressure_systolic': 120,
                'blood_pressure_diastolic': 80,
                'heart_rate': 72,
                'respiratory_rate': 16,
                'weight': 70.5,
                'height': 175.0,
            }
            
            if 'chest pain' in appointment.chief_complaint.lower():
                medical_record_data.update({
                    'symptoms': 'Chest pain, shortness of breath, fatigue',
                    'diagnosis': 'Angina pectoris - stable',
                    'treatment_plan': 'Lifestyle modification, medication therapy',
                    'prescription': 'Metoprolol 50mg twice daily, Aspirin 81mg daily',
                    'follow_up_instructions': 'Return in 2 weeks, monitor blood pressure',
                    'next_appointment_recommended': date.today() + timedelta(days=14),
                    'requires_follow_up': True,
                    'blood_pressure_systolic': 145,
                    'blood_pressure_diastolic': 90
                })
            elif 'headache' in appointment.chief_complaint.lower():
                medical_record_data.update({
                    'symptoms': 'Severe headache, nausea, sensitivity to light',
                    'diagnosis': 'Migraine without aura',
                    'treatment_plan': 'Acute treatment with triptans, preventive measures',
                    'prescription': 'Sumatriptan 50mg as needed, Paracetamol 500mg',
                    'follow_up_instructions': 'Keep headache diary, avoid triggers',
                    'requires_follow_up': True,
                    'is_emergency': True
                })
            elif 'knee' in appointment.chief_complaint.lower():
                medical_record_data.update({
                    'symptoms': 'Knee pain, stiffness, limited range of motion',
                    'diagnosis': 'Post-surgical knee rehabilitation - good progress',
                    'treatment_plan': 'Continue physiotherapy, gradual activity increase',
                    'lab_tests_ordered': 'X-ray knee joint - follow up',
                    'follow_up_instructions': 'Continue exercises, return in 4 weeks',
                    'next_appointment_recommended': date.today() + timedelta(days=28),
                    'requires_follow_up': True
                })
            else:
                medical_record_data.update({
                    'symptoms': 'General checkup requested',
                    'diagnosis': 'Healthy - no acute findings',
                    'treatment_plan': 'Continue healthy lifestyle',
                    'follow_up_instructions': 'Annual checkup recommended',
                    'next_appointment_recommended': date.today() + timedelta(days=365)
                })
            
            medical_record = MedicalRecord.objects.create(**medical_record_data)
            self.stdout.write(f'✓ Created medical record for: {appointment.patient.name}')

    def create_prescriptions(self):
        """Create sample prescriptions"""
        self.stdout.write('\n💊 Creating prescriptions...')
        
        medical_records = MedicalRecord.objects.all()
        medicines = list(Medicine.objects.all())
        pharmacist = Pharmacist.objects.first()
        
        if not medical_records.exists() or not medicines:
            self.stdout.write(self.style.WARNING('Need medical records and medicines to create prescriptions'))
            return
        
        prescriptions_data = [
            {
                'medical_record': medical_records.filter(diagnosis__icontains='angina').first(),
                'medicine': Medicine.objects.filter(name='Paracetamol').first(),
                'dosage': '1 tablet twice daily after meals',
                'duration_days': 7,
                'quantity': 14,
                'instructions': 'Take with food to avoid stomach upset'
            },
            {
                'medical_record': medical_records.filter(diagnosis__icontains='migraine').first(),
                'medicine': Medicine.objects.filter(name='Paracetamol').first(),
                'dosage': '1-2 tablets as needed for headache',
                'duration_days': 30,
                'quantity': 20,
                'instructions': 'Do not exceed 8 tablets per day'
            },
        ]
        
        # Filter out None values
        prescriptions_data = [p for p in prescriptions_data if p['medical_record'] and p['medicine']]
        
        for prescription_data in prescriptions_data:
            prescription = Prescription.objects.create(**prescription_data)
            
            # Mark some prescriptions as filled
            if prescription.medical_record.diagnosis and 'migraine' in prescription.medical_record.diagnosis.lower():
                if pharmacist:
                    prescription.mark_as_filled(pharmacist)
            
            self.stdout.write(f'✓ Created prescription: {prescription.medicine.name} for {prescription.medical_record.patient.name}')

    def create_lab_tests(self):
        """Create sample lab tests"""
        self.stdout.write('\n🔬 Creating lab tests...')
        
        medical_records = MedicalRecord.objects.all()
        doctors = list(Doctor.objects.all())
        lab_tech = LabTechnician.objects.first()
        
        if not medical_records.exists() or not doctors:
            self.stdout.write(self.style.WARNING('Need medical records and doctors to create lab tests'))
            return
        
        lab_tests_data = [
            {
                'medical_record': medical_records.filter(diagnosis__icontains='angina').first(),
                'test_name': 'Lipid Profile',
                'test_type': 'blood',
                'status': 'completed',
                'ordered_by': doctors[0],
                'assigned_technician': lab_tech,
                'results': 'Total Cholesterol: 240 mg/dL (High), LDL: 160 mg/dL (High), HDL: 35 mg/dL (Low)',
                'normal_range': 'Total Cholesterol: <200 mg/dL, LDL: <100 mg/dL, HDL: >40 mg/dL',
                'is_abnormal': True,
                'cost': 150000.00,
                'completed_date': timezone.now() - timedelta(days=1)
            },
            {
                'medical_record': medical_records.filter(lab_tests_ordered__icontains='X-ray').first(),
                'test_name': 'Knee X-Ray',
                'test_type': 'xray',
                'status': 'scheduled',
                'ordered_by': doctors[2] if len(doctors) > 2 else doctors[0],
                'cost': 200000.00,
                'scheduled_date': timezone.now() + timedelta(days=3)
            },
            {
                'medical_record': medical_records.first(),
                'test_name': 'Complete Blood Count',
                'test_type': 'blood',
                'status': 'completed',
                'ordered_by': doctors[0],
                'assigned_technician': lab_tech,
                'results': 'WBC: 7.2 K/uL, RBC: 4.5 M/uL, Hemoglobin: 14.2 g/dL, Platelets: 250 K/uL',
                'normal_range': 'WBC: 4.0-11.0 K/uL, RBC: 4.2-5.4 M/uL, Hemoglobin: 12.0-15.5 g/dL',
                'is_abnormal': False,
                'cost': 100000.00,
                'completed_date': timezone.now() - timedelta(days=2)
            }
        ]
        
        # Filter out None values
        lab_tests_data = [t for t in lab_tests_data if t['medical_record'] and t['ordered_by']]
        
        for lab_test_data in lab_tests_data:
            lab_test = LabTest.objects.create(**lab_test_data)
            self.stdout.write(f'✓ Created lab test: {lab_test.test_name} for {lab_test.medical_record.patient.name}')

        self.stdout.write(
            self.style.SUCCESS(f'\n📊 Created {len(lab_tests_data)} lab tests')
        )