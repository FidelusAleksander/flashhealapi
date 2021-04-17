from batch.models.DoctorModel import DoctorModel
from flask_restful import Resource, reqparse


class DoctorList(Resource):
    def get(self):
        doctors = [doctor.json() for doctor in DoctorModel.query.all()]
        return doctors


class Doctor(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('doctor_id',
                        required=True,
                        type=int,
                        help="doctor_id cannot be left blank")

    def get(self):
        data = Doctor.parser.parse_args()
        doctor = DoctorModel.find_by_id(data['doctor_id'])
        if not doctor:
            return {"message": f"Doctor with doctor_id={data['doctor_id']} does not exist."}

        return doctor.json()
