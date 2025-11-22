from app import celery, app
from models import db, Appointment, Treatment, User
import csv
import os
from datetime import datetime, timedelta

@celery.task
def send_daily_reminders():
    with app.app_context():
        print("Sending daily reminders...")
        tomorrow = datetime.now().date() + timedelta(days=1)
        appointments = Appointment.query.filter_by(date=tomorrow, status='Booked').all()
        
        count = 0
        for appt in appointments:
            # In a real app, use Flask-Mail or similar
            print(f"Reminder: Dear {appt.patient.user.username}, you have an appointment with Dr. {appt.doctor.user.username} tomorrow at {appt.time}.")
            count += 1
        return f"Sent {count} reminders"

@celery.task
def generate_monthly_report():
    with app.app_context():
        print("Generating monthly report...")
        total_appointments = Appointment.query.count()
        completed_appointments = Appointment.query.filter_by(status='Completed').count()
        
        report = f"Monthly Report - {datetime.now().strftime('%B %Y')}\n"
        report += f"Total Appointments: {total_appointments}\n"
        report += f"Completed: {completed_appointments}\n"
        
        # Save to file in the backend directory
        report_path = os.path.join(os.path.dirname(__file__), 'monthly_report.txt')
        with open(report_path, 'w') as f:
            f.write(report)
            
        return f"Report generated at {report_path}"

@celery.task
def export_treatments_csv():
    with app.app_context():
        print("Exporting treatments...")
        treatments = Treatment.query.all()
        filename = os.path.join(os.path.dirname(__file__), 'treatments_export.csv')
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Date', 'Doctor', 'Patient', 'Diagnosis', 'Prescription']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for t in treatments:
                writer.writerow({
                    'Date': t.appointment.date,
                    'Doctor': t.appointment.doctor.user.username,
                    'Patient': t.appointment.patient.user.username,
                    'Diagnosis': t.diagnosis,
                    'Prescription': t.prescription
                })
        return f"Exported {len(treatments)} treatments to {filename}"
