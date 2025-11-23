from flask import Blueprint, request, jsonify
from models import db, Patient, Doctor, Appointment
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

bp = Blueprint('patient', __name__, url_prefix='/patient')

@bp.route('/doctors', methods=['GET'])
@jwt_required()
def search_doctors():
    # Allow filtering by specialization
    specialization = request.args.get('specialization')
    if specialization:
        doctors = Doctor.query.filter(Doctor.specialization.ilike(f'%{specialization}%')).all()
    else:
        doctors = Doctor.query.all()
    return jsonify([d.to_dict() for d in doctors]), 200

@bp.route('/appointments', methods=['GET', 'POST'])
@jwt_required()
def manage_appointments():
    import json
    current_user = json.loads(get_jwt_identity())
    if current_user['role'] != 'patient':
        return jsonify({"msg": "Unauthorized"}), 403
        
    patient = Patient.query.filter_by(user_id=current_user['id']).first()
    
    if request.method == 'GET':
        appointments = Appointment.query.filter_by(patient_id=patient.id).all()
        return jsonify([a.to_dict() for a in appointments]), 200
        
    if request.method == 'POST':
        data = request.get_json()
        doctor_id = data.get('doctor_id')
        date_str = data.get('date')
        time_str = data.get('time')
        
        # Validate availability (Simplified for now)
        # Check if slot is taken
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_obj = datetime.strptime(time_str, '%H:%M').time()
        
        existing = Appointment.query.filter_by(doctor_id=doctor_id, date=date_obj, time=time_obj).first()
        if existing and existing.status != 'Cancelled':
            return jsonify({"msg": "Slot already booked"}), 400
            
        new_appointment = Appointment(
            doctor_id=doctor_id,
            patient_id=patient.id,
            date=date_obj,
            time=time_obj,
            status='Booked'
        )
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({"msg": "Appointment booked successfully"}), 201

@bp.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def manage_profile():
    import json
    current_user = json.loads(get_jwt_identity())
    if current_user['role'] != 'patient':
        return jsonify({"msg": "Unauthorized"}), 403
        
    patient = Patient.query.filter_by(user_id=current_user['id']).first()
    
    if request.method == 'GET':
        return jsonify(patient.to_dict()), 200
        
    if request.method == 'PUT':
        data = request.get_json()
        
        if 'contact_number' in data:
            patient.contact_number = data['contact_number']
        if 'address' in data:
            patient.address = data['address']
        if 'date_of_birth' in data:
            try:
                patient.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            except ValueError:
                pass # Ignore invalid date format
                
        db.session.commit()
        return jsonify({"msg": "Profile updated"}), 200
