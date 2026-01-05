from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(50))
    linkedin = db.Column(db.String(200))
    github = db.Column(db.String(200))
    summary = db.Column(db.Text)
    skills = db.Column(db.Text)  # Stored as JSON string
    education = db.Column(db.Text)  # Stored as JSON string
    experience = db.Column(db.Text)  # Stored as JSON string
    projects = db.Column(db.Text)  # Stored as JSON string
    certifications = db.Column(db.Text)  # Stored as JSON string

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'linkedin': self.linkedin,
            'github': self.github,
            'summary': self.summary,
            'skills': json.loads(self.skills) if self.skills else [],
            'education': json.loads(self.education) if self.education else [],
            'experience': json.loads(self.experience) if self.experience else [],
            'projects': json.loads(self.projects) if self.projects else [],
            'certifications': json.loads(self.certifications) if self.certifications else []
        }
