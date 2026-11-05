from flask import Flask, request, jsonify
from functools import wraps
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_employee_api_key_2026'

# Mock Database for Users and Roles
USERS = {
    "admin": {"password": "adminpassword", "role": "Administrator"},
    "john": {"password": "empassword", "role": "Employee"}
}

# Mock Database for Employee Records
EMPLOYEES = [
    {"id": 1, "name": "Alice Smith", "department": "HR", "salary": 50000},
    {"id": 2, "name": "Bob Jones", "department": "Engineering", "salary": 75000}
]

# Token Required Decorator (Authentication)
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # Check if token is passed in headers (Authorization: Bearer <token>)
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"status": "error", "message": "Invalid token format. Use 'Bearer <token>'"}), 401

        if not token:
            return jsonify({"status": "error", "message": "Authentication Token is missing!"}), 401

        try:
            # Decode token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
            current_role = data['role']
        except jwt.ExpiredSignatureError:
            return jsonify({"status": "error", "message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"status": "error", "message": "Invalid Token!"}), 401

        return f(current_user, current_role, *args, **kwargs)
    return decorator

# Role Required Decorator (Authorization)
def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def wrapped(current_user, current_role, *args, **kwargs):
            if current_role != required_role and current_role != "Administrator":
                return jsonify({
                    "status": "error", 
                    "message": f"Authorization Error: Role '{current_role}' is not authorized for this operation. Requires '{required_role}'."
                }), 403
            return f(current_user, current_role, *args, **kwargs)
        return wrapped
    return decorator

# 1. Login Route (Generates JWT Token)
@app.route('/login', methods=['POST'])
def login():
    auth_data = request.get_json()

    if not auth_data or 'username' not in auth_data or 'password' not in auth_data:
        return jsonify({"status": "error", "message": "Missing username or password!"}), 400

    username = auth_data['username']
    password = auth_data['password']

    if username not in USERS or USERS[username]['password'] != password:
        return jsonify({"status": "error", "message": "Invalid credentials!"}), 401

    # Generate Token valid for 30 minutes
    token = jwt.encode({
        'username': username,
        'role': USERS[username]['role'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({
        "status": "success",
        "message": f"Welcome back, {username}!",
        "role": USERS[username]['role'],
        "token": token
    }), 200

# 2. View Employee Records (Accessible by Employee & Administrator)
@app.route('/employees', methods=['GET'])
@token_required
def get_employees(current_user, current_role):
    return jsonify({
        "status": "success",
        "logged_in_as": current_user,
        "role": current_role,
        "employees": EMPLOYEES
    }), 200

# 3. Add Employee Record (Administrator Only)
@app.route('/employees', methods=['POST'])
@token_required
@role_required("Administrator")
def add_employee(current_user, current_role):
    data = request.get_json()
    if not data or 'name' not in data or 'department' not in data or 'salary' not in data:
        return jsonify({"status": "error", "message": "Missing required employee fields (name, department, salary)!"}), 400

    new_employee = {
        "id": len(EMPLOYEES) + 1,
        "name": data['name'],
        "department": data['department'],
        "salary": data['salary']
    }
    EMPLOYEES.append(new_employee)
    return jsonify({
        "status": "success",
        "message": "Employee added successfully!",
        "employee": new_employee
    }), 201

# 4. Update Employee Record (Administrator Only)
@app.route('/employees/<int:emp_id>', methods=['PUT'])
@token_required
@role_required("Administrator")
def update_employee(current_user, current_role, emp_id):
    emp = next((e for e in EMPLOYEES if e['id'] == emp_id), None)
    if not emp:
        return jsonify({"status": "error", "message": "Employee not found!"}), 404

    data = request.get_json()
    emp['name'] = data.get('name', emp['name'])
    emp['department'] = data.get('department', emp['department'])
    emp['salary'] = data.get('salary', emp['salary'])

    return jsonify({
        "status": "success",
        "message": f"Employee {emp_id} updated successfully!",
        "employee": emp
    }), 200

# 5. Delete Employee Record (Administrator Only)
@app.route('/employees/<int:emp_id>', methods=['DELETE'])
@token_required
@role_required("Administrator")
def delete_employee(current_user, current_role, emp_id):
    global EMPLOYEES
    emp = next((e for e in EMPLOYEES if e['id'] == emp_id), None)
    if not emp:
        return jsonify({"status": "error", "message": "Employee not found!"}), 404

    EMPLOYEES = [e for e in EMPLOYEES if e['id'] != emp_id]
    return jsonify({
        "status": "success",
        "message": f"Employee {emp_id} deleted successfully!"
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
