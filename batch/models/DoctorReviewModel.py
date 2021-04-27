from batch.db import db
from datetime import datetime

class DoctorReviewModel(db.Model):

    __tablename__ = 'doctor_reviews'
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'))
    review_id = db.Column(db.Integer, primary_key=True)
    creation_time = db.Column(db.DateTime, default=datetime.utcnow)
    star_rating = db.Column(db.Integer, nullable=False)
    reviewer = db.Column(db.String(255), nullable=False)
    opinion = db.Column(db.String(1024), nullable=True)

    def __init__(self, doctor_id, star_rating, reviewer, opinion):
        self.doctor_id = doctor_id
        self.star_rating = star_rating
        self.reviewer = reviewer
        self.opinion = opinion

    def json(self):
        return {"doctor_id": self.doctor_id,
                "review_id": self.review_id,
                "creation_time": str(self.creation_time),
                "star_rating": self.star_rating,
                "reviewer": self.reviewer,
                "opinion": self.opinion}

    def insert_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_doctor_id(cls, doctor_id):
        return cls.query.filter_by(doctor_id=doctor_id).all()