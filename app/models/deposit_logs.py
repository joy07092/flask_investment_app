from datetime import datetime
from app import db

class Deposit_Logs(db.Model):
    __tablename__ = 'deposit_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    month = db.Column(db.String(6), nullable=False)  # Format: YYYYMM
    date = db.Column(db.String(8), nullable=False)   # Format: YYYYMMDD
    amount = db.Column(db.Float, nullable=False)
    comments = db.Column(db.Text, nullable=True)
    action_type = db.Column(db.String(10), nullable=True)  # 'update' or 'delete'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.String, nullable=True)
    updated_by = db.Column(db.String, nullable=True)



'''

CREATE TABLE public.deposit_logs (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients(id),
    month VARCHAR(6) NOT NULL,         -- Format: YYYYMM
    date VARCHAR(8) NOT NULL,          -- Format: YYYYMMDD
    amount DOUBLE PRECISION NOT NULL,
    comments TEXT,
    action_type VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR,
    updated_by VARCHAR
);

ALTER TABLE public.deposit_logs
    OWNER TO postgres;


'''