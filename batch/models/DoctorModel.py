from batch.db import db


class DoctorModel(db.Model):
    __tablename__ = 'doctors'
    doctor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    specialty = db.Column(db.String(255), nullable=True)
    latitude = db.Column(db.Float(precision=6), nullable=True)
    longtitude = db.Column(db.Float(precision=6), nullable=True)

    def __init__(self, first_name, last_name, specialty, latitude, longtitude):
        self.first_name = first_name
        self.last_name = last_name
        self.specialty = specialty
        self.latitude = latitude
        self.longtitude = longtitude

    def json(self):
        return {"doctor_id": self.doctor_id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "specialty": self.specialty,
                "latitude": self.latitude,
                "longtitude": self.longtitude}

    @classmethod
    def find_by_id(cls, doctor_id):
        return cls.query.filter_by(doctor_id=doctor_id).first()
