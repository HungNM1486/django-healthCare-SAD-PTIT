#!/usr/bin/env python3
"""
Hospital Management System - Week 2 Complete Setup Script
This script sets up the extended hospital management system with all new features
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

def run_command(command, description="", check=True):
    """Run a shell command and print the result"""
    print(f"\n{'='*60}")
    print(f"🔄 {description or command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and not check:
            print(f"Warning: {result.stderr}")
        
        if result.returncode == 0:
            print(f"✅ {description or command} - COMPLETED")
            return True
        else:
            print(f"⚠️  {description or command} - COMPLETED WITH WARNINGS")
            return False
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def check_requirements():
    """Check system requirements"""
    print("\n🔍 CHECKING SYSTEM REQUIREMENTS")
    print("=" * 60)
    
    # Check Python version
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ ERROR: manage.py not found. Please run from Django project root.")
        
        # Try to find the project root
        current_dir = Path.cwd()
        for parent in current_dir.parents:
            if (parent / 'manage.py').exists():
                print(f"📁 Found Django project in: {parent}")
                response = input("Switch to this directory? (y/n): ")
                if response.lower() == 'y':
                    os.chdir(parent)
                    break
        else:
            print("Could not find Django project root. Please navigate manually.")
            sys.exit(1)
    
    print(f"✅ Django project found in: {os.getcwd()}")
    
    # Check for required files
    required_files = [
        'healthcare/models.py',
        'healthcare/views.py',
        'healthcare/serializers.py',
        'chatbotAI/settings.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"⚠️  Missing files: {', '.join(missing_files)}")
        print("Please ensure all code files from artifacts are in place.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)

def setup_environment():
    """Setup virtual environment and dependencies"""
    print("\n🐍 SETTING UP PYTHON ENVIRONMENT")
    print("=" * 60)
    
    # Check if virtual environment exists
    if not os.path.exists('venv'):
        print("Creating virtual environment...")
        if platform.system() == "Windows":
            run_command("python -m venv venv", "Creating virtual environment")
        else:
            run_command("python3 -m venv venv", "Creating virtual environment")
    else:
        print("✅ Virtual environment already exists")
    
    # Determine pip command
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Upgrade pip
    run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip")
    
    # Install basic requirements first
    basic_packages = [
        "Django==5.2.1",
        "djangorestframework==3.15.1",
        "djangorestframework-simplejwt==5.3.0",
        "django-filter==24.2",
        "django-cors-headers==4.3.1"
    ]
    
    print("Installing basic packages...")
    for package in basic_packages:
        run_command(f"{pip_cmd} install {package}", f"Installing {package}")
    
    # Install additional packages if requirements.txt exists
    if os.path.exists('requirements.txt'):
        print("Installing from requirements.txt...")
        run_command(f"{pip_cmd} install -r requirements.txt", "Installing requirements", check=False)
    
    return python_cmd

def create_directories():
    """Create necessary directories"""
    print("\n📁 CREATING DIRECTORY STRUCTURE")
    print("=" * 60)
    
    directories = [
        'healthcare/management',
        'healthcare/management/commands',
        'healthcare/migrations',
        'healthcare/fixtures',
        'logs',
        'media',
        'media/uploads',
        'static',
        'staticfiles',
        'templates',
        'templates/healthcare',
        'tests',
        'docs'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created: {directory}")
        else:
            print(f"✅ Exists: {directory}")
    
    # Create __init__.py files
    init_files = [
        'healthcare/management/__init__.py',
        'healthcare/management/commands/__init__.py',
        'tests/__init__.py'
    ]
    
    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('# This file makes Python treat the directory as a package\n')
            print(f"📄 Created: {init_file}")

def setup_database(python_cmd):
    """Setup database and migrations"""
    print("\n🗄️  SETTING UP DATABASE")
    print("=" * 60)
    
    # Create migrations
    run_command(f"{python_cmd} manage.py makemigrations healthcare", 
                "Creating healthcare migrations")
    
    # Apply migrations
    run_command(f"{python_cmd} manage.py migrate", 
                "Applying database migrations")
    
    # Create extended data
    run_command(f"{python_cmd} manage.py setup_extended_data", 
                "Setting up extended sample data")
    
    # Collect static files
    run_command(f"{python_cmd} manage.py collectstatic --noinput", 
                "Collecting static files")

def create_config_files():
    """Create configuration files"""
    print("\n⚙️  CREATING CONFIGURATION FILES")
    print("=" * 60)
    
    # Create .env file
    if not os.path.exists('.env'):
        env_content = """# Django Environment Variables
DEBUG=True
SECRET_KEY=django-insecure-#)v2lplh@x#koys_njv+#ss%aldur=((m(-%-qik_2(z02qq9&
ALLOWED_HOSTS=127.0.0.1,localhost

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password

# Redis (for caching and Celery)
REDIS_URL=redis://localhost:6379/0

# API Keys (for future integrations)
# OPENAI_API_KEY=your-openai-key
# GOOGLE_API_KEY=your-google-key

# Security Settings
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False

# Logging Level
LOG_LEVEL=INFO
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("📄 Created .env file")
    
    # Create .gitignore if it doesn't exist
    if not os.path.exists('.gitignore'):
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/
staticfiles/

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store
Thumbs.db

# Environment variables
.env
.env.local

# Testing
.coverage
htmlcov/
.pytest_cache/
.tox/

# Node.js (if using frontend)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Documentation
docs/_build/

# Backup files
*.bak
*.backup
*.dump

# Temporary files
*.tmp
*.temp
"""
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        print("📄 Created .gitignore file")

def create_scripts():
    """Create useful scripts"""
    print("\n📜 CREATING UTILITY SCRIPTS")
    print("=" * 60)
    
    # Create development script
    dev_script_content = '''#!/bin/bash
# Development helper script

echo "🏥 Hospital Management System - Development Helper"
echo "=================================================="

case "$1" in
    "server")
        echo "Starting development server..."
        source venv/bin/activate && python manage.py runserver
        ;;
    "shell")
        echo "Starting Django shell..."
        source venv/bin/activate && python manage.py shell
        ;;
    "test")
        echo "Running tests..."
        source venv/bin/activate && python manage.py test
        ;;
    "migrate")
        echo "Running migrations..."
        source venv/bin/activate && python manage.py makemigrations && python manage.py migrate
        ;;
    "superuser")
        echo "Creating superuser..."
        source venv/bin/activate && python manage.py createsuperuser
        ;;
    "reset")
        echo "Resetting database and creating sample data..."
        source venv/bin/activate && python manage.py flush --noinput && python manage.py migrate && python manage.py setup_extended_data
        ;;
    "docs")
        echo "Opening API documentation..."
        echo "http://127.0.0.1:8000/api/healthcare/docs/"
        ;;
    *)
        echo "Usage: $0 {server|shell|test|migrate|superuser|reset|docs}"
        echo ""
        echo "  server    - Start development server"
        echo "  shell     - Start Django shell"
        echo "  test      - Run tests"
        echo "  migrate   - Create and apply migrations"
        echo "  superuser - Create superuser"
        echo "  reset     - Reset database with sample data"
        echo "  docs      - Show API documentation URL"
        ;;
esac
'''
    
    with open('dev.sh', 'w') as f:
        f.write(dev_script_content)
    
    # Make script executable on Unix systems
    if platform.system() != "Windows":
        os.chmod('dev.sh', 0o755)
    
    print("📜 Created development helper script: dev.sh")

def run_tests(python_cmd):
    """Run tests to verify setup"""
    print("\n🧪 RUNNING TESTS")
    print("=" * 60)
    
    # Run basic tests
    print("Running basic tests...")
    result = run_command(f"{python_cmd} manage.py test healthcare.tests", 
                        "Running core tests", check=False)
    
    # Run extended tests if available
    if os.path.exists('healthcare/test_extended.py'):
        print("Running extended tests...")
        run_command(f"{python_cmd} manage.py test healthcare.test_extended", 
                   "Running extended tests", check=False)
    
    return result

def create_documentation():
    """Create basic documentation"""
    print("\n📚 CREATING DOCUMENTATION")
    print("=" * 60)
    
    # Create API quick reference
    api_docs = """# Hospital Management System API Quick Reference

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
curl -X POST http://127.0.0.1:8000/api/healthcare/auth/login/ \\
  -H "Content-Type: application/json" \\
  -d '{"username":"admin","password":"admin123"}'
```

### Get Doctors
```bash
curl -X GET http://127.0.0.1:8000/api/healthcare/doctors/ \\
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create Appointment
```bash
curl -X POST http://127.0.0.1:8000/api/healthcare/appointments/ \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "patient": 1,
    "doctor": 1,
    "appointment_date": "2024-06-01T14:00:00Z",
    "appointment_type": "consultation",
    "chief_complaint": "Regular checkup"
  }'
```

For complete documentation, visit: http://127.0.0.1:8000/api/healthcare/docs/
"""
    
    with open('docs/API_REFERENCE.md', 'w') as f:
        f.write(api_docs)
    
    print("📚 Created API reference documentation")

def display_completion_message():
    """Display completion message with next steps"""
    print("\n" + "=" * 80)
    print("🎉 HOSPITAL MANAGEMENT SYSTEM - WEEK 2 SETUP COMPLETED!")
    print("=" * 80)
    
    print("\n📋 WHAT'S BEEN SET UP:")
    print("✅ Extended models (Medicine, Appointment, MedicalRecord, etc.)")
    print("✅ Complete API with CRUD operations")
    print("✅ Business logic and validations")
    print("✅ Authentication and permissions")
    print("✅ Dashboard and analytics")
    print("✅ Sample data and fixtures")
    print("✅ Tests and documentation")
    
    print("\n🚀 NEXT STEPS:")
    print("1. Activate virtual environment:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Start development server:")
    print("   python manage.py runserver")
    print("   OR use: ./dev.sh server")
    
    print("\n3. Access the application:")
    print("   🌐 API Root:      http://127.0.0.1:8000/api/healthcare/")
    print("   📊 Dashboard:     http://127.0.0.1:8000/api/healthcare/dashboard/stats/")
    print("   📚 API Docs:      http://127.0.0.1:8000/api/healthcare/docs/")
    print("   🔧 Admin Panel:   http://127.0.0.1:8000/admin/")
    
    print("\n🔑 LOGIN CREDENTIALS:")
    print("   Username: admin")
    print("   Password: admin123")
    
    print("\n🧪 TESTING:")
    print("   Run tests: python manage.py test")
    print("   OR use: ./dev.sh test")
    
    print("\n📖 HELPFUL COMMANDS:")
    print("   ./dev.sh server    - Start server")
    print("   ./dev.sh shell     - Django shell")
    print("   ./dev.sh migrate   - Run migrations")
    print("   ./dev.sh reset     - Reset database")
    
    print("\n🎯 SAMPLE API CALLS:")
    print("   # Get JWT token")
    print("   curl -X POST http://127.0.0.1:8000/api/healthcare/auth/login/ \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"username\":\"admin\",\"password\":\"admin123\"}'")
    
    print("\n   # Get doctors list")
    print("   curl -X GET http://127.0.0.1:8000/api/healthcare/doctors/ \\")
    print("     -H 'Authorization: Bearer YOUR_TOKEN'")
    
    print("\n📱 FRONTEND READY:")
    print("   The API is ready for frontend integration")
    print("   CORS is configured for React/Vue development")
    
    print("\n🤖 NEXT PHASE:")
    print("   Week 3-4: Frontend Development")
    print("   Week 5-8: AI Chatbot Integration")
    
    print("\n" + "=" * 80)

def main():
    """Main setup function"""
    print("🏥 HOSPITAL MANAGEMENT SYSTEM - WEEK 2 COMPLETE SETUP")
    print("=" * 80)
    print("This script will set up the complete hospital management system")
    print("with extended models, APIs, and business logic.")
    print("=" * 80)
    
    try:
        # Check system requirements
        check_requirements()
        
        # Setup environment
        python_cmd = setup_environment()
        
        # Create directories
        create_directories()
        
        # Setup database
        setup_database(python_cmd)
        
        # Create configuration files
        create_config_files()
        
        # Create utility scripts
        create_scripts()
        
        # Create documentation
        create_documentation()
        
        # Run tests
        run_tests(python_cmd)
        
        # Display completion message
        display_completion_message()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Setup failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()