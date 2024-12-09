# Flask Authentication API

This project is a Flask-based API for user authentication, registration, and user management. It includes JWT-based authentication and Swagger UI for API documentation.

---

## **Features**

- User registration with hashed passwords.
- Login with JWT token generation.
- Protected routes using JWT.
- Role-based user management (e.g., customer, administrator).
- Swagger UI for API documentation.

---

## **Technologies Used**

- **Flask**: Lightweight web framework.
- **Flask-JWT-Extended**: JWT-based authentication.
- **Flask-SQLAlchemy**: ORM for database operations.
- **SQLite**: Database for local development.
- **Swagger UI**: API documentation.
- **dotenv**: Manage environment variables.

---

## **Getting Started**

### **Prerequisites**

Make sure you have the following installed:
- Python 3.9 or later
- pip (Python package manager)

---

### **Setup Instructions**

#### **Step 1: Clone the Repository**
```bash
git clone https://github.com/Nwoko-Repo/swe242025-team3.git
cd swe242025-team3

#### **Step 2: Set up a virtual Environment**
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
flask db upgrade
flask run


The app will start on http://localhost:5000.
Swagger UI is available at http://localhost:5000/swagger.

