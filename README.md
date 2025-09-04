# Healthcare Backend

A Django-based healthcare management system with JWT authentication, patient and doctor management, and patient-doctor mapping capabilities.

## Features

- **User Authentication**: JWT-based authentication system
- **Patient Management**: CRUD operations for patient records
- **Doctor Management**: CRUD operations for doctor records  
- **Patient-Doctor Mapping**: Assign and manage doctor-patient relationships
- **Secure API**: All endpoints protected with JWT authentication
- **PostgreSQL Database**: Robust data storage

## Requirements

- Python 3.8+
- PostgreSQL
- Django 5.2+
- Django REST Framework 3.14+

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd healthcare_backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   # Edit .env with your actual values
   ```

5. **Set up PostgreSQL database**
   ```bash
   # Create database
   createdb healthcare_db
   ```

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Patients
- `POST /api/patients/` - Create patient (authenticated)
- `GET /api/patients/` - List user's patients (authenticated)
- `GET /api/patients/{id}/` - Get patient details (authenticated)
- `PUT /api/patients/{id}/` - Update patient (authenticated)
- `DELETE /api/patients/{id}/` - Delete patient (authenticated)

### Doctors
- `POST /api/doctors/` - Create doctor (authenticated)
- `GET /api/doctors/` - List all doctors (authenticated)
- `GET /api/doctors/{id}/` - Get doctor details (authenticated)
- `PUT /api/doctors/{id}/` - Update doctor (authenticated)
- `DELETE /api/doctors/{id}/` - Delete doctor (authenticated)

### Mappings
- `POST /api/mappings/` - Assign doctor to patient (authenticated)
- `GET /api/mappings/` - List all mappings (authenticated)
- `GET /api/mappings/{patient_id}/doctors/` - Get doctors for patient (authenticated)
- `DELETE /api/mappings/{id}/` - Remove doctor from patient (authenticated)

## Testing

Test the API endpoints using Postman or any API client:

1. **Register a user**: `POST /api/auth/register/`
2. **Login**: `POST /api/auth/login/`
3. **Use the access token** in Authorization header: `Bearer <token>`
4. **Test other endpoints** with the token

## Project Structure

```
healthcare_backend/
├── accounts/          # User authentication
├── patients/          # Patient management
├── doctors/           # Doctor management
├── mappings/          # Patient-doctor relationships
├── healthcare_backend/ # Main project settings
├── requirements.txt   # Dependencies
└── manage.py         # Django management
```

## Security Features

- JWT authentication for all protected endpoints
- User ownership validation for patient records
- Input validation and sanitization
- Environment variable configuration for sensitive data
