from app import app, db
from models import User

with app.app_context():
    users = User.query.all()
    print(f"{'ID':<5} {'Username':<15} {'Role':<10} {'Is Active':<10}")
    print("-" * 45)
    for u in users:
        print(f"{u.id:<5} {u.username:<15} {u.role:<10} {u.is_active:<10}")
