from config import db
import enum
from sqlalchemy.dialects.postgresql import ENUM

# Enums
class SkillEnum(enum.Enum):
    web_development = "Web Development"
    mobile_development = "Mobile Development"
    graphic_design = "Graphic Design"
    writing = "Writing"
    translation = "Translation"
    marketing = "Marketing"
    data_entry = "Data Entry"
    accounting = "Accounting"
    seo = "SEO"
    video_editing = "Video Editing"

class RoleEnum(enum.Enum):
    freelancer = "freelancer"
    client = "client"
    admin = "admin"

class ProjectStatusEnum(enum.Enum):
    open = "open"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class ProposalStatusEnum(enum.Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class ContractStatusEnum(enum.Enum):
    active = "active"
    completed = "completed"
    disputed = "disputed"

class PaymentStatusEnum(enum.Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"

# User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(RoleEnum), default=RoleEnum.freelancer, nullable=False)

    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    languages = db.Column(db.ARRAY(db.String))
    hourly_rate = db.Column(db.Float)
    experience = db.Column(db.String(255))
    photo = db.Column(db.String)
    skills = db.Column(db.ARRAY(db.Enum(SkillEnum)))
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role.value,
            "bio": self.bio,
            "location": self.location,
            "languages": self.languages,
            "hourlyRate": self.hourly_rate,
            "experience": self.experience,
            "photo": self.photo,
            "skills": [skill.value for skill in self.skills] if self.skills else [],
            "isVerified": self.is_verified,
            "createdAt": self.created_at.isoformat() if self.created_at else None
        }

# Project
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    budget = db.Column(db.Float)
    duration = db.Column(db.String(100))
    status = db.Column(db.Enum(ProjectStatusEnum), default=ProjectStatusEnum.open)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client = db.relationship('User', foreign_keys=[client_id])

# Proposal
class Proposal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    freelancer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cover_letter = db.Column(db.Text)
    proposed_rate = db.Column(db.Float)
    status = db.Column(db.Enum(ProposalStatusEnum), default=ProposalStatusEnum.pending)
    submitted_at = db.Column(db.DateTime, server_default=db.func.now())

    project = db.relationship('Project', backref='proposals')
    freelancer = db.relationship('User', foreign_keys=[freelancer_id])

# Contract
class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    freelancer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    agreed_rate = db.Column(db.Float)
    status = db.Column(db.Enum(ContractStatusEnum), default=ContractStatusEnum.active)
    started_at = db.Column(db.DateTime, server_default=db.func.now())
    ended_at = db.Column(db.DateTime)

    project = db.relationship('Project')
    client = db.relationship('User', foreign_keys=[client_id])
    freelancer = db.relationship('User', foreign_keys=[freelancer_id])

# Payment
class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'))
    amount = db.Column(db.Float)
    method = db.Column(db.String(50))
    status = db.Column(db.Enum(PaymentStatusEnum), default=PaymentStatusEnum.pending)
    paid_at = db.Column(db.DateTime)

    contract = db.relationship('Contract')

# Message (Chat System)
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.Text)
    sent_at = db.Column(db.DateTime, server_default=db.func.now())

    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])

# Admin (optional)
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    permissions = db.Column(db.ARRAY(db.String), default=[])