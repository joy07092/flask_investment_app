from app import db
from datetime import datetime
from flask_login import UserMixin
from app import login_manager

class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_type = db.Column(db.Enum('Client', 'Admin', name='user_type_enum'), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String, nullable=False)
    status = db.Column(db.Enum('Active', 'Inactive', name='user_status'), default='Active')
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.String, nullable=True)
    updated_by = db.Column(db.String, nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


'''
-- Define the ENUM types first
CREATE TYPE user_type_enum AS ENUM ('Client', 'Admin');
CREATE TYPE user_status AS ENUM ('Active', 'Inactive');

-- Create the users table
CREATE TABLE public.users (
    id SERIAL PRIMARY KEY,
    user_type user_type_enum NOT NULL,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    mobile_number VARCHAR(20),
    password TEXT NOT NULL,
    status user_status DEFAULT 'Active',
    client_id INTEGER REFERENCES clients(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    updated_by TEXT
);

-- Set the table owner (optional)
ALTER TABLE IF EXISTS public.users
    OWNER TO postgres;


'''