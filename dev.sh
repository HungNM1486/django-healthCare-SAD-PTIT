#!/bin/bash
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
