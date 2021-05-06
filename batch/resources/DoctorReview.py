from flask_restful import Resource, reqparse
from batch.models.DoctorReviewModel import DoctorReviewModel


class DoctorReview(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('star_rating',
                        required=True,
                        type=int,
                        help="star_rating cannot be left blank")
    parser.add_argument('reviewer',
                        required=True,
                        type=str,
                        help="reviewer cannot be left blank")
    parser.add_argument('opinion',
                        required=True,
                        type=str,
                        help="opinion cannot be left blank")
    def post(self, doctor_id):
        data = DoctorReview.parser.parse_args()

        if data["star_rating"] not in range(1,6):
            return {"message": "star_rating has to be in range 1 to 5"}, 404

        doctor_review = DoctorReviewModel(doctor_id=doctor_id, star_rating=data["star_rating"],
                                          reviewer=data["reviewer"], opinion=data["opinion"])
        try:
            doctor_review.insert_to_db()
        except:
            return {"message": "An error occurred when inserting doctor."}, 500

        return doctor_review.json(), 201

    def get(self, doctor_id):
        reviews = DoctorReviewModel.query.filter_by(doctor_id=doctor_id).all()

        if reviews:
            return [review.json() for review in reviews], 200

        return [], 200
