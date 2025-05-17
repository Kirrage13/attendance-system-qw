# Attendance System for University

This is a Django-based web application designed to help university teachers manage student attendance efficiently and securely. 
The system supports user registration for students and teachers, lecture creation, attendance tracking with access keys, and announcement sharing.

## Features

- User authentication (students and teachers)
- Registration
- Role-based interface:
  - Students: view announcements, check in to lectures
  - Teachers: create lectures, generate access keys, post announcements, see student attendency
- Attendance verification with time-limited keys
- Admin interface for managing users and attendance
- Basic security measures implemented (CSRF, session control, etc.)

## Tech Stack

- Python 3
- Django
- SQLite (for development)
- Bootstrap (UI styling)
- Git for version control

- ## Setup Instructions

1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt
3. Apply database migrations:
   python manage.py migrate
4. Create a superuser (optional, for admin access):
   python manage.py createsuperuser
5. Run the development server:
   python manage.py runserver
6. Access the app:
   Visit http://127.0.0.1:8000/ in your browser.
   
!The SQLite database file (db.sqlite3) is intentionally excluded from the repository to avoid exposing local data. It will be created automatically when running migrations!

This system was developed as part of a diploma project. 
Django and related technologies were studied independently in the process. 
The aim was to create a practical tool to address common problems with manual attendance tracking and improve reliability, efficiency, and fairness in educational environments.

This project is provided for educational purposes. Feel free to fork or adapt for non-commercial use
