from datetime import datetime
from app import db

class Clients(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    name = db.Column(db.String(100), nullable=False)  
    mobile = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    nid = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    emergency_contact = db.Column(db.String(20), nullable=True)
    present_address = db.Column(db.Text, nullable=True)
    permanent_address = db.Column(db.Text, nullable=True)
    nominee_name = db.Column(db.String(100), nullable=True)
    nominee_nid = db.Column(db.String(20), nullable=True)
    nominee_mobile = db.Column(db.String(20), nullable=True)
    status = db.Column(db.Enum('Active', 'Inactive', name='user_status'), default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.String(100), nullable=True)
    updated_by = db.Column(db.String(100), nullable=True)




    '''
    
CREATE TYPE client_status AS ENUM ('Active', 'Inactive');


CREATE TABLE public.clients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    mobile VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    nid VARCHAR(20) NOT NULL,
    image VARCHAR(255),
    emergency_contact VARCHAR(20),
    present_address TEXT,
    permanent_address TEXT,
    nominee_name VARCHAR(100),
    nominee_nid VARCHAR(20),
    nominee_mobile VARCHAR(20),
    status client_status DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    updated_by VARCHAR(100)
);

ALTER TABLE IF EXISTS public.clients
    OWNER TO postgres;


    
    '''
