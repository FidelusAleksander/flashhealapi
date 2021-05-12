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
            return {"message": "star_rating has to be in range 1 to 5"}, 400

        doctor_review = DoctorReviewModel(doctor_id=doctor_id, **data)
        try:
            doctor_review.insert_to_db()
            return doctor_review.json(), 201

        except:
            return {"message": "An error occurred when inserting doctor."}, 500

    def get(self, doctor_id, review_id=None):
        reviews = DoctorReviewModel.query.filter_by(doctor_id=doctor_id)

        # Single review
        if review_id:
            try:
                review = reviews.filter_by(review_id=review_id).first()
                if review:
                    return review.json(), 200
                else:
                    return {"message": f"There isn't a review with id = {review_id}"}, 404
            except:
                return {"message": "An error occurred when retrieving review."}, 500

        # All reviews
        else:
            try:
                reviews = reviews.all()
                if reviews:
                    return [review.json() for review in reviews], 200
                else:
                    return [], 200
            except:
                return {"message": "An error occurred when retrieving reviews."}, 500

    def delete(self, doctor_id, review_id):
        review = DoctorReviewModel.query.filter_by(doctor_id=doctor_id).filter_by(review_id=review_id).first()
        if review:
            try:
                review.remove_from_db()
                return {"message": "Successfully deleted review."}, 200
            except:
                return {"message": "An error occurred when deleting review."}, 500
        else:
            return {"message": f"There isn't a review with id = {review_id}"}, 404

    def put(self, doctor_id, review_id):
        review = DoctorReviewModel.query.filter_by(doctor_id=doctor_id).filter_by(review_id=review_id).first()

        if review:
            data = DoctorReview.parser.parse_args()
            if data["star_rating"] not in range(1, 6):
                return {"message": "star_rating has to be in range 1 to 5"}, 400
            try:
                review.update(**data)
                return review.json(), 200
            except:
                return {"message": "An error occurred when updating review."}, 500
        else:
            return {"message": f"There isn't a review with id = {review_id}"}, 404

