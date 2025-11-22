from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = User.query.filter_by(role='admin').first()
    if admin:
        print(f"Found admin user: {admin.username}")
        admin.password_hash = generate_password_hash('admin123')
        db.session.commit()
        print("Admin password reset to 'admin123'")
    else:
        print("Admin user not found, creating one...")
        admin = User(username='admin', email='admin@hms.com', password_hash=generate_password_hash('admin123'), role='admin')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created with password 'admin123'")
