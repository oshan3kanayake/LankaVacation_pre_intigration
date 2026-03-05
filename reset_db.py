from app import create_app
from extensions import db

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    from models import User
    from werkzeug.security import generate_password_hash
    admin = User(name="Admin", email="admin@example.com", password_hash=generate_password_hash("admin123"), role="admin")
    db.session.add(admin)
    db.session.commit()
    print("Database tables dropped and recreated, and admin user seeded successfully.")