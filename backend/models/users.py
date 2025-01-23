from app import db
from datetime import datetime
import pytz
from enum import Enum

# Set Manila timezone
MANILA_TZ = pytz.timezone("Asia/Manila")

class RoleEnum(Enum):
    ADMIN = "admin"
    STAFF = "staff"

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.STAFF)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(MANILA_TZ))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(MANILA_TZ), onupdate=lambda: datetime.now(MANILA_TZ))

    def __repr__(self):
        return f"<User {self.username}>"

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role.value, 
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

