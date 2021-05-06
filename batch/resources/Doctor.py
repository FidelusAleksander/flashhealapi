from batch.models.DoctorModel import DoctorModel
from flask_restful import Resource, reqparse


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

    def get(self, doctor_id=None):
        """
        Retrieves DoctorModel objects in json form from the database.
        :param doctor_id: id of the doctor to retrieve (will retrieve list of all doctors if None)
        :return: single/list of json DoctorModel objects
        """

        if doctor_id:
            try:
                doctor = DoctorModel.query.filter_by(doctor_id=doctor_id).first()
            except:
                return {"message": "An error occurred when retrieving doctor."}, 500

            if not doctor:
                return {"message": f"There isn't a doctor with id = {doctor_id}"}, 404

            return doctor.json(), 200

        else:
            try:
                doctors = [doctor.json() for doctor in DoctorModel.query.all()]
            except:
                return {"message": "An error occurred when retrieving doctors."}, 500

            return doctors, 200
