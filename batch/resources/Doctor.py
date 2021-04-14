from batch.models.DoctorModel import DoctorModel
from flask_restful import Resource

class DoctorList(Resource):
    def get(self):
        doctors = [doctor.json() for doctor in DoctorModel.query.all()]
        return doctors
