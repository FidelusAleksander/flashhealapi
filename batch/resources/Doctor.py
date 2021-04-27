from batch.models.DoctorModel import DoctorModel
from flask_restful import Resource, reqparse


class DoctorList(Resource):
    def get(self):
        doctors = [doctor.json() for doctor in DoctorModel.query.all()]
        return doctors


class Doctor(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        required=True,
                        type=str,
                        help="first_name cannot be left blank")
    parser.add_argument('last_name',
                        required=True,
                        type=str,
                        help="last_name cannot be left blank")
    parser.add_argument('specialty',
                        required=True,
                        type=str,
                        help="specialty cannot be left blank")
    parser.add_argument('latitude',
                        required=True,
                        type=float,
                        help="latitude cannot be left blank")
    parser.add_argument('longtitude',
                        required=True,
                        type=float,
                        help="longtitude cannot be left blank")

    def post(self):
        data = Doctor.parser.parse_args()
        doctor = DoctorModel(**data)
        try:
            doctor.insert_to_db()
        except:
            return {"message": "An error occurred when inserting doctor."}, 500

        return doctor.json(), 201
