import sys
import os
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Users



def seed_users():
    if not Users.query.filter_by(username='Admin1').first():
        admin_user = Users(
            user_type='Admin',
            username='Admin1',
            email='admin1@gmail.com',
            mobile_number=None,
            password=generate_password_hash('12345'),
            status='Active',
            client_id=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            created_by=None,
            updated_by=None
        )
        db.session.add(admin_user)
        print("Admin1 user created successfully!")
    else:
        print("Admin1 user already exists!")

    
    if not Users.query.filter_by(username='User1').first():
        normal_user = Users(
            user_type='User',
            username='User1',
            email='user1@gmail.com',
            mobile_number=None,
            password=generate_password_hash('12345'),
            status='Active',
            client_id=None,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            created_by=None,
            updated_by=None
        )
        db.session.add(normal_user)
        print("User1 user created successfully!")
    else:
        print("User1 user already exists!")

    db.session.commit()


