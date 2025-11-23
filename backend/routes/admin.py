from flask import Blueprint, request, jsonify
from models import db, User, Doctor, Appointment, Patient
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    import json
    current_user = json.loads(get_jwt_identity())
    if current_user['role'] != 'admin':
        return jsonify({"msg": "Unauthorized"}), 403
        
    doctor_count = Doctor.query.count()
    patient_count = Patient.query.count()
    appointment_count = Appointment.query.count()
    
    return jsonify({
        "doctors": doctor_count,
        "patients": patient_count,
        "appointments": appointment_count
    }), 200

@bp.route('/doctors', methods=['GET', 'POST'])
@bp.route('/doctors/<int:id>', methods=['DELETE'])
@jwt_required()
def manage_doctors(id=None):
    import json
    current_user = json.loads(get_jwt_identity())
    if current_user['role'] != 'admin':
        return jsonify({"msg": "Unauthorized"}), 403

    if request.method == 'GET':
        doctors = Doctor.query.all()
        result = []
        for d in doctors:
            data = d.to_dict()
            data['is_active'] = d.user.is_active
            result.append(data)
        return jsonify(result), 200
        
    if request.method == 'POST':
        data = request.get_json()
        # Create User first
        if User.query.filter_by(username=data['username']).first():
             return jsonify({"msg": "User already exists"}), 400
             
        hashed_password = generate_password_hash(data['password'])
        new_user = User(username=data['username'], email=data['email'], password_hash=hashed_password, role='doctor')
        db.session.add(new_user)
        db.session.flush()
        
        new_doctor = Doctor(
            user_id=new_user.id,
            specialization=data['specialization'],
            description=data.get('description', ''),
            availability=data.get('availability', {})
        )
        db.session.add(new_doctor)
        db.session.commit()
        return jsonify({"msg": "Doctor added successfully"}), 201

@bp.route('/users/<int:id>/block', methods=['PUT'])
@jwt_required()
def block_user(id):
    import json
    from datetime import date
    
    current_user = json.loads(get_jwt_identity())
    if current_user['role'] != 'admin':
        return jsonify({"msg": "Unauthorized"}), 403
        
    user = User.query.get_or_404(id)
    if user.role == 'admin':
        return jsonify({"msg": "Cannot block admin"}), 400
        
    user.is_active = not user.is_active
    
    # If blocking a doctor, cancel future appointments
    if not user.is_active and user.role == 'doctor':
        if user.doctor_profile:
            doctor_id = user.doctor_profile.id
            print(f"Blocking Doctor ID: {doctor_id}")
            
            # Cancel future appointments
            appointments = Appointment.query.filter(
                Appointment.doctor_id == doctor_id,
                Appointment.date >= date.today(),
                Appointment.status == 'Booked'
            ).all()
            
            print(f"Found {len(appointments)} future appointments to cancel.")
            
            for appt in appointments:
                appt.status = 'Cancelled'
                print(f"Cancelled Appointment ID: {appt.id}")
        else:
            print("User is doctor but has no profile.")
    
    db.session.commit()
    
    status = "unblocked" if user.is_active else "blocked"
    return jsonify({"msg": f"User {status}"}), 200

@bp.route('/tasks/reminders', methods=['POST'])
@jwt_required()
def trigger_reminders():
    from tasks import send_daily_reminders
    try:
        result = send_daily_reminders()
        return jsonify({"msg": str(result)}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@bp.route('/tasks/report', methods=['POST'])
@jwt_required()
def trigger_report():
    from tasks import generate_monthly_report
    try:
        result = generate_monthly_report()
        return jsonify({"msg": str(result)}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@bp.route('/tasks/export', methods=['POST'])
@jwt_required()
def trigger_export():
    from tasks import export_treatments_csv
    try:
        result = export_treatments_csv()
        return jsonify({"msg": str(result)}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
