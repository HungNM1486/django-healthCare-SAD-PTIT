from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from healthcare.models import Doctor, Patient, Nurse, Admin, Pharmacist, DrugSupplier, LabTechnician
from datetime import date

class Command(BaseCommand):
    help = 'Setup initial data for the hospital management system'

    def handle(self, *args, **options):
        self.stdout.write('Creating initial data...')

        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@hospital.com',
                password='admin123',
                first_name='System',
                last_name='Administrator'
            )
            self.stdout.write('✅ Superuser created: admin/admin123')

        # Create sample doctors
        doctors_data = [
            {
                'name': 'Dr. Nguyễn Văn Nam',
                'specialization': 'Cardiology',
                'phone': '+84-123-456-789',
                'email': 'nam.nguyen@hospital.com'
            },
            {
                'name': 'Dr. Trần Thị Mai',
                'specialization': 'Pediatrics',
                'phone': '+84-123-456-790',
                'email': 'mai.tran@hospital.com'
            }
        ]

        for doctor_data in doctors_data:
            doctor, created = Doctor.objects.get_or_create(
                email=doctor_data['email'],
                defaults=doctor_data
            )
            if created:
                self.stdout.write(f'✅ Created doctor: {doctor.name}')

        # Create sample patients
        patients_data = [
            {
                'name': 'Nguyễn Văn An',
                'date_of_birth': date(1985, 3, 15),
                'phone': '+84-987-654-321',
                'email': 'an.nguyen@email.com',
                'address': '123 Đường ABC, Quận 1, TP.HCM'
            },
            {
                'name': 'Trần Thị Bình',
                'date_of_birth': date(1990, 7, 22),
                'phone': '+84-987-654-322',
                'email': 'binh.tran@email.com',
                'address': '456 Đường XYZ, Quận 2, TP.HCM'
            }
        ]

        for patient_data in patients_data:
            patient, created = Patient.objects.get_or_create(
                email=patient_data['email'],
                defaults=patient_data
            )
            if created:
                self.stdout.write(f'✅ Created patient: {patient.name}')

        # Create other staff
        Nurse.objects.get_or_create(
            email='nurse@hospital.com',
            defaults={'name': 'Y tá Nguyễn Thị Lan', 'phone': '+84-111-222-333'}
        )

        Pharmacist.objects.get_or_create(
            email='pharmacist@hospital.com',
            defaults={'name': 'Dược sĩ Lê Thị Hương', 'phone': '+84-222-333-444'}
        )

        LabTechnician.objects.get_or_create(
            email='labtech@hospital.com',
            defaults={'name': 'KTV Phạm Văn Đức', 'phone': '+84-333-444-555'}
        )

        DrugSupplier.objects.get_or_create(
            email='supplier@company.com',
            defaults={
                'name': 'Công ty Dược phẩm ABC',
                'contact_person': 'Nguyễn Văn Kinh',
                'phone': '+84-444-555-666',
                'address': '100 Đường Công nghiệp, Quận 9, TP.HCM'
            }
        )

        Admin.objects.get_or_create(
            email='admin.staff@hospital.com',
            defaults={'name': 'Quản trị viên Lê Văn Quản', 'phone': '+84-555-666-777'}
        )

        self.stdout.write(
            self.style.SUCCESS('🎉 Initial data setup completed successfully!')
        )
