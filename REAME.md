# 🏥 Hospital Management System with AI Chatbot

A comprehensive hospital management system built with Django REST Framework, featuring an intelligent AI chatbot for medical assistance.

## 📋 Features

### Core Hospital Management
- **Multi-role User Management**: Doctors, Patients, Nurses, Admins, Pharmacists, Lab Technicians, Drug Suppliers
- **RESTful API**: Complete CRUD operations for all entities
- **Authentication**: JWT token-based authentication
- **Search & Filtering**: Advanced search and filtering capabilities
- **Pagination**: Efficient data pagination
- **Dashboard**: Statistics and overview dashboard

### AI Chatbot (In Development)
- **Symptom Analysis**: AI-powered symptom checker
- **Medical Recommendations**: Treatment and medicine suggestions
- **Natural Language Processing**: Conversational interface
- **Integration**: Seamless integration with hospital management system

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package installer)
- Git

### Automated Setup
1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd chatbotAI
   ```

2. **Run setup script**
   ```bash
   python setup.py
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Start the development server**
   ```bash
   python manage.py runserver
   ```

### Manual Setup
If you prefer manual setup:

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create directories**
   ```bash
   mkdir -p healthcare/management/commands logs media static templates
   ```

4. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create initial data**
   ```bash
   python manage.py setup_initial_data
   ```

6. **Run server**
   ```bash
   python manage.py runserver
   ```

## 🔐 Default Login Credentials

- **Username**: `admin`
- **Password**: `admin123`

## 📡 API Endpoints

### Authentication
- `POST /api/healthcare/auth/register/` - User registration
- `POST /api/healthcare/auth/login/` - Login (JWT token)
- `POST /api/healthcare/auth/token/refresh/` - Refresh token

### Core Entities
- `GET|POST /api/healthcare/doctors/` - Doctors list/create
- `GET|PUT|DELETE /api/healthcare/doctors/{id}/` - Doctor detail
- `GET|POST /api/healthcare/patients/` - Patients list/create
- `GET|PUT|DELETE /api/healthcare/patients/{id}/` - Patient detail
- `GET|POST /api/healthcare/nurses/` - Nurses list/create
- `GET|POST /api/healthcare/pharmacists/` - Pharmacists list/create
- `GET|POST /api/healthcare/lab-technicians/` - Lab technicians list/create
- `GET|POST /api/healthcare/drug-suppliers/` - Drug suppliers list/create

### Special Endpoints
- `GET /api/healthcare/doctors/specializations/` - List of specializations
- `GET /api/healthcare/patients/search_by_phone/?phone=123` - Search by phone
- `GET /api/healthcare/dashboard/stats/` - Dashboard statistics

### Query Parameters
All list endpoints support:
- `search` - Search in relevant fields
- `page` - Page number for pagination
- `page_size` - Items per page (max 100)
- `ordering` - Sort by field (add `-` for descending)

**Examples:**
```bash
# Search doctors by name or specialization
GET /api/healthcare/doctors/?search=cardiology

# Filter doctors by specialization
GET /api/healthcare/doctors/?specialization=Cardiology

# Get patients with pagination
GET /api/healthcare/patients/?page=2&page_size=20

# Sort doctors by name (ascending)
GET /api/healthcare/doctors/?ordering=name

# Sort doctors by name (descending)
GET /api/healthcare/doctors/?ordering=-name
```

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test healthcare.tests

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

## 📊 API Usage Examples

### Create a Doctor
```bash
curl -X POST http://127.0.0.1:8000/api/healthcare/doctors/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. John Doe",
    "specialization": "Cardiology",
    "phone": "+84-123-456-789",
    "email": "john.doe@hospital.com"
  }'
```

### Get Patient List
```bash
curl -X GET "http://127.0.0.1:8000/api/healthcare/patients/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Search Doctors
```bash
curl -X GET "http://127.0.0.1:8000/api/healthcare/doctors/?search=cardiology" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🏗️ Project Structure

```
chatbotAI/
├── chatbotAI/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── healthcare/
│   ├── management/
│   │   └── commands/
│   │       └── setup_initial_data.py
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── chatbot/  # Future AI chatbot app
├── logs/
├── media/
├── static/
├── templates/
├── venv/
├── .env
├── .gitignore
├── manage.py
├── requirements.txt
├── setup.py
└── README.md
```

## 🔧 Development

### Adding New Features
1. Create new models in `healthcare/models.py`
2. Create serializers in `healthcare/serializers.py`
3. Create views in `healthcare/views.py`
4. Add URL patterns in `healthcare/urls.py`
5. Write tests in `healthcare/tests.py`
6. Run migrations: `python manage.py makemigrations && python manage.py migrate`

### Code Quality
```bash
# Format code
black .

# Check code style
flake8

# Sort imports
isort .
```

## 🌐 Frontend Integration

The API is designed to work with any frontend framework. CORS is configured for common development ports:
- React: http://localhost:3000
- Vue.js: http://localhost:8080

Example frontend integration:
```javascript
// Login and get token
const response = await fetch('http://127.0.0.1:8000/api/healthcare/auth/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'admin',
    password: 'admin123'
  })
});

const { access, refresh } = await response.json();

// Use token for API calls
const doctorsResponse = await fetch('http://127.0.0.1:8000/api/healthcare/doctors/', {
  headers: {
    'Authorization': `Bearer ${access}`,
    'Content-Type': 'application/json',
  }
});

const doctors = await doctorsResponse.json();
```

## 🤖 AI Chatbot Development Plan

### Phase 1: Basic Chatbot (Current)
- Symptom checker based on existing PDF code
- Simple rule-based responses
- Integration with hospital system

### Phase 2: Advanced NLP
- Natural language understanding
- Context-aware conversations
- Multi-turn dialogues

### Phase 3: Machine Learning
- Personalized recommendations
- Learning from interactions
- Advanced medical knowledge base

## 🚀 Deployment

### Development
```bash
python manage.py runserver
```

### Production
1. Set `DEBUG=False` in settings
2. Configure PostgreSQL database
3. Set up Gunicorn + Nginx
4. Use environment variables for secrets
5. Enable HTTPS

Example production deployment:
```bash
# Install production dependencies
pip install gunicorn psycopg2-binary

# Collect static files
python manage.py collectstatic

# Run with Gunicorn
gunicorn chatbotAI.wsgi:application --bind 0.0.0.0:8000
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

If you have any questions or issues, please:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed description

## 🔄 Next Steps

1. **Week 1-2**: Complete hospital management API
2. **Week 3-4**: Develop frontend interface
3. **Week 5-8**: Implement AI chatbot
4. **Week 9-12**: Advanced features and optimization
5. **Week 13-16**: Testing and deployment

---

Made with ❤️ for better healthcare management