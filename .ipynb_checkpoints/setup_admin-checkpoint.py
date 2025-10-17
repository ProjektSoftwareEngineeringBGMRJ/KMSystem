from controller import app, db
from models.admin import Admin

with app.app_context():
    if not Admin.query.filter_by(email="admin@example.org").first():
        admin = Admin(name="Admin", email="admin@example.org", passwort="admin123")
        db.session.add(admin)
        db.session.commit()
        print("Admin erstellt.")
    else:
        print("Admin existiert bereits.")