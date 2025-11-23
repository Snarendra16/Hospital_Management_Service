from flask import Blueprint, request, jsonify
from models import db, User, Patient
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password_hash, password):
        if not user.is_active:
            return jsonify({"msg": "Account is blocked"}), 403
            
        import json
        identity_str = json.dumps({'id': user.id, 'role': user.role, 'username': user.username})
        access_token = create_access_token(identity=identity_str)
        return jsonify(access_token=access_token, role=user.role), 200
    
    return jsonify({"msg": "Bad username or password"}), 401

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400
        
    # Create User
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password, role='patient')
    db.session.add(new_user)
    db.session.flush() # Get ID
    
    # Create Patient Profile
    new_patient = Patient(user_id=new_user.id)
    # Add extra fields if provided in data
    if 'date_of_birth' in data:
        # Parse date
        pass 
    
    db.session.add(new_patient)
    db.session.commit()
    
    return jsonify({"msg": "User registered successfully"}), 201

@bp.route('/register-doctor', methods=['POST'])
def register_doctor():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    specialization = data.get('specialization')
    
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400
        
    # Create User
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password, role='doctor')
    db.session.add(new_user)
    db.session.flush()
    
    # Create Doctor Profile
    from models import Doctor
    new_doctor = Doctor(user_id=new_user.id, specialization=specialization, availability={})
    db.session.add(new_doctor)
    db.session.commit()
    
    return jsonify({"msg": "Doctor registered successfully"}), 201
