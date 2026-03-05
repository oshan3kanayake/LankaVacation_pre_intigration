from app import create_app
from extensions import db
from models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    admin_email = "admin@example.com"
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        new_admin = User(
            name="Admin",
            email=admin_email,
            password_hash=generate_password_hash("admin123"),
            role="admin"
        )
        db.session.add(new_admin)
        db.session.commit()
        print(f"Admin user '{admin_email}' created successfully.")
    else:
        print(f"Admin user '{admin_email}' already exists.")
