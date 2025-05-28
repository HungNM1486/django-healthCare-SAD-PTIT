# Hospital Management System API Quick Reference

## Authentication
- POST /api/healthcare/auth/login/ - Get JWT token
- POST /api/healthcare/auth/refresh/ - Refresh token

## Core Entities
- GET|POST /api/healthcare/doctors/
- GET|POST /api/healthcare/patients/
- GET|POST /api/healthcare/medicines/
- GET|POST /api/healthcare/appointments/
- GET|POST /api/healthcare/medical-records/

## Dashboard
- GET /api/healthcare/dashboard/stats/
- GET /api/healthcare/analytics/

## Example Usage

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/healthcare/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Get Doctors
```bash
curl -X GET http://127.0.0.1:8000/api/healthcare/doctors/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create Appointment
```bash
curl -X POST http://127.0.0.1:8000/api/healthcare/appointments/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient": 1,
    "doctor": 1,
    "appointment_date": "2024-06-01T14:00:00Z",
    "appointment_type": "consultation",
    "chief_complaint": "Regular checkup"
  }'
```

For complete documentation, visit: http://127.0.0.1:8000/api/healthcare/docs/
