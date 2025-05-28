#!/usr/bin/env python3
"""
Script to create and apply migrations for the extended models
Run this after updating the models.py file
"""

import os
import sys
import subprocess

def run_command(command, description=""):
    """Run a shell command and print the result"""
    print(f"\n{'='*50}")
    print(f"🔄 {description or command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        print(f"✅ {description or command} - COMPLETED")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def main():
    print("🏥 Hospital Management System - Migration Setup")
    print("=" * 50)
    
    # Check if manage.py exists
    if not os.path.exists('manage.py'):
        print("❌ ERROR: manage.py not found. Please run from Django project root.")
        sys.exit(1)
    
    print("📦 Creating migrations for extended models...")
    
    # Create migrations
    success = run_command(
        "python manage.py makemigrations healthcare --name extended_models",
        "Creating migrations for extended models"
    )
    
    if not success:
        print("❌ Failed to create migrations")
        sys.exit(1)
    
    # Show migration plan
    run_command(
        "python manage.py showmigrations healthcare",
        "Showing migration status"
    )
    
    # Apply migrations
    success = run_command(
        "python manage.py migrate",
        "Applying migrations to database"
    )
    
    if not success:
        print("❌ Failed to apply migrations")
        sys.exit(1)
    
    # Create extended data
    success = run_command(
        "python manage.py setup_extended_data",
        "Setting up extended sample data"
    )
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 MIGRATION SETUP COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("\nNext steps:")
        print("1. Run development server:")
        print("   python manage.py runserver")
        print("\n2. Test the new endpoints:")
        print("   http://127.0.0.1:8000/api/healthcare/medicines/")
        print("   http://127.0.0.1:8000/api/healthcare/appointments/")
        print("   http://127.0.0.1:8000/api/healthcare/medical-records/")
        print("\n3. Check dashboard:")
        print("   http://127.0.0.1:8000/api/healthcare/dashboard/stats/")
    else:
        print("⚠️  Migration completed but data setup failed. You can run manually:")
        print("python manage.py setup_extended_data")

if __name__ == "__main__":
    main()