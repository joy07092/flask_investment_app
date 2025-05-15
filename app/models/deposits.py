from datetime import datetime
from app import db

class Deposits(db.Model):
    __tablename__ = 'deposits'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    month = db.Column(db.String(6), nullable=False)  # Format: YYYYMM
    date = db.Column(db.String(8), nullable=False)   # Format: YYYYMMDD
    amount = db.Column(db.Float, nullable=False)
    comments = db.Column(db.Text, nullable=True)
    file = db.Column(db.String, nullable=True)  # Can be image or document filename/path
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.String, nullable=True)
    updated_by = db.Column(db.String, nullable=True)


'''
CREATE TABLE public.deposits (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients(id),
    month VARCHAR(6) NOT NULL,         -- Format: YYYYMM
    date VARCHAR(8) NOT NULL,          -- Format: YYYYMMDD
    amount DOUBLE PRECISION NOT NULL,
    comments TEXT,
    file VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR,
    updated_by VARCHAR
);

ALTER TABLE public.deposits
    OWNER TO postgres;


'''