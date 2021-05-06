from batch.models.DoctorModel import DoctorModel
from batch.models.DoctorReviewModel import DoctorReviewModel
from flask_restful import Resource
from batch.db import db
from sqlalchemy.types import Float


class DoctorSummary(Resource):
    def get(self):
        try:
            reviews = db.session.query(DoctorReviewModel.doctor_id,
                                       db.func.round(db.func.avg(db.func.cast(DoctorReviewModel.star_rating, Float)), 1).label('avg_review'),
                                       db.func.count(DoctorReviewModel.star_rating).label('review_count'),
                                       ).group_by(DoctorReviewModel.doctor_id).subquery()
            results = db.session.query(DoctorModel, reviews).outerjoin(reviews, DoctorModel.doctor_id == reviews.c.doctor_id).all()
        except:
            return {"message": "An error occurred while retrieving DoctorSummaries."}, 500

        summaries = [self.combine(result.DoctorModel, result.avg_review, result.review_count) for result in results]

        return summaries, 200



    def combine(self, doctor, avg_review, review_count):
        summary = doctor.json()
        summary['avg_review'] = avg_review if avg_review else 0
        summary['review_count'] = review_count if review_count else 0
        return summary
