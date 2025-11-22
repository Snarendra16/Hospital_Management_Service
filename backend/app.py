from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import Config
from models import db, User
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.from_object(Config)

# Extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)
jwt = JWTManager(app)
celery = make_celery(app)

from routes import auth, admin, doctor, patient

app.register_blueprint(auth.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(doctor.bp)
app.register_blueprint(patient.bp)

@app.route('/')
def index():
    return "Hospital Management System API is running!"

from werkzeug.security import generate_password_hash

# Create DB and Admin if not exists
def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(role='admin').first():
            print("Creating Admin User...")
            hashed_password = generate_password_hash('admin123')
            admin = User(username='admin', email='admin@hms.com', password_hash=hashed_password, role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin User Created.")

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
