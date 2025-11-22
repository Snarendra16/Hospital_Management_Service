from flask import Blueprint, request, jsonify
from models import db, Doctor, Appointment, Treatment
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('doctor', __name__, url_prefix='/doctor')

@bp.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    current_user = get_jwt_identity()
    if current_user['role'] != 'doctor':
        return jsonify({"msg": "Unauthorized"}), 403
        
    doctor = Doctor.query.filter_by(user_id=current_user['id']).first()
    if not doctor:
         return jsonify({"msg": "Doctor profile not found"}), 404
         
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    return jsonify([a.to_dict() for a in appointments]), 200

@bp.route('/appointments/<int:id>/complete', methods=['POST'])
@jwt_required()
def complete_appointment(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'doctor':
        return jsonify({"msg": "Unauthorized"}), 403
        
    appointment = Appointment.query.get_or_404(id)
    # Verify ownership
    if appointment.doctor.user_id != current_user['id']:
        return jsonify({"msg": "Unauthorized"}), 403
        
    data = request.get_json()
    
    appointment.status = 'Completed'
    
    # Add Treatment
    treatment = Treatment(
        appointment_id=appointment.id,
        diagnosis=data.get('diagnosis'),
        prescription=data.get('prescription'),
        notes=data.get('notes')
    )
    db.session.add(treatment)
    db.session.commit()
    
    return jsonify({"msg": "Appointment completed"}), 200

@bp.route('/patients', methods=['GET'])
@jwt_required()
def get_patients():
    current_user = get_jwt_identity()
    if current_user['role'] != 'doctor':
        return jsonify({"msg": "Unauthorized"}), 403
        
    # Get patients who have had appointments with this doctor
    doctor = Doctor.query.filter_by(user_id=current_user['id']).first()
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    patient_ids = set([a.patient_id for a in appointments])
    
    # Also include all patients (optional, but requirements say "list of patients assigned")
    # For now let's return all patients the doctor has interacted with
    patients = []
    for pid in patient_ids:
        # Avoid circular import or complex query for now
        # We need to import Patient model if not already
        from models import Patient
        p = Patient.query.get(pid)
        if p:
            patients.append(p.to_dict())
            
    return jsonify(patients), 200

@bp.route('/patients/<int:id>/history', methods=['GET'])
@jwt_required()
def get_patient_history(id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'doctor':
        return jsonify({"msg": "Unauthorized"}), 403
        
    # Get all treatments for this patient
    treatments = Treatment.query.join(Appointment).filter(Appointment.patient_id == id).all()
    
    result = []
    for t in treatments:
        result.append({
            'date': t.appointment.date.isoformat(),
            'doctor': t.appointment.doctor.user.username,
            'diagnosis': t.diagnosis,
            'prescription': t.prescription,
            'notes': t.notes
        })
        
    return jsonify(result), 200

@bp.route('/availability', methods=['GET', 'PUT'])
@jwt_required()
def manage_availability():
    current_user = get_jwt_identity()
    if current_user['role'] != 'doctor':
        return jsonify({"msg": "Unauthorized"}), 403
        
    doctor = Doctor.query.filter_by(user_id=current_user['id']).first()
    
    if request.method == 'GET':
        return jsonify(doctor.availability or {}), 200
        
    if request.method == 'PUT':
        data = request.get_json()
        doctor.availability = data
        db.session.commit()
        return jsonify({"msg": "Availability updated"}), 200
