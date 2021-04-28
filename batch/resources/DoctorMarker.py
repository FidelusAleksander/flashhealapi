from batch.models.DoctorModel import DoctorModel
from batch.models.DoctorReviewModel import DoctorReviewModel
from flask_restful import Resource
from batch.db import db
from sqlalchemy.types import Float


class DoctorMarkerList(Resource):
    def get(self):
        try:
            reviews = db.session.query(DoctorReviewModel.doctor_id,
                                       db.func.round(db.func.avg(db.func.cast(DoctorReviewModel.star_rating, Float)), 1).label('avg_review'),
                                       db.func.count(DoctorReviewModel.star_rating).label('review_count'),
                                       )\
                .group_by(DoctorReviewModel.doctor_id).subquery()
            results = db.session.query(DoctorModel, reviews).outerjoin(reviews, DoctorModel.doctor_id == reviews.c.doctor_id).all()
            markers = []
            for marker in results:
                new_marker = marker.DoctorModel.json()
                new_marker['avg_review'] = marker.avg_review if marker.avg_review else 0
                new_marker['review_count'] = marker.review_count if marker.review_count else 0
                markers.append(new_marker)

            return markers, 200

        except:
            return {"message": "An error occurred while retrieving DoctorMarkers."}, 500
