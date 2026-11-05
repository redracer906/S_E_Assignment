# Task 3: Authentication and Authorization in a Flask API

This project implements a secure Employee Management API featuring JWT-based Authentication and Role-Based Authorization (Employee vs. Administrator).

## User Credentials for Testing
1. **Administrator:**
   - Username: `admin`
   - Password: `adminpassword`
   - Permissions: Can View, Add, Update, and Delete employees.
2. **Employee:**
   - Username: `john`
   - Password: `empassword`
   - Permissions: Can only View employees.

---

## Installation & Running

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python app.py
   ```

---

## cURL Testing Commands (Command Prompt / CMD)

### Step 1: Login to get JWT Token
* **Login as Admin:**
  ```bash
  curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d "{"username": "admin", "password": "adminpassword"}"
  ```
* **Login as Employee:**
  ```bash
  curl -X POST http://127.0.0.1:5000/login -H "Content-Type: application/json" -d "{"username": "john", "password": "empassword"}"
  ```
*(Copy the generated `"token"` string from the response to use below)*

### Step 2: View Employees (Both Admin and Employee can do this)
```bash
curl -X GET http://127.0.0.1:5000/employees -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Step 3: Add Employee (Admin Only - Authorized)
```bash
curl -X POST http://127.0.0.1:5000/employees -H "Content-Type: application/json" -H "Authorization: Bearer ADMIN_TOKEN_HERE" -d "{"name": "Sara Khan", "department": "Finance", "salary": 80000}"
```

### Step 4: Authorization Failure Test (Employee trying to Add Employee)
If an **Employee** token is used to add an employee, it will reject with `403 Forbidden`:
```bash
curl -X POST http://127.0.0.1:5000/employees -H "Content-Type: application/json" -H "Authorization: Bearer EMPLOYEE_TOKEN_HERE" -d "{"name": "Test User", "department": "IT", "salary": 60000}"
```

### Step 5: Authentication Failure Test (Invalid/Missing Token)
```bash
curl -X GET http://127.0.0.1:5000/employees -H "Authorization: Bearer invalid_token_xyz"
```
