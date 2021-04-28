from batch.models.DoctorModel import DoctorModel
from batch.models.DoctorReviewModel import DoctorReviewModel
from flask_restful import Resource
from batch.db import db
from sqlalchemy.types import Float


class DoctorMarkerList(Resource):
    def get(self):
        reviews = db.session.query(DoctorReviewModel.doctor_id,
                                   db.func.round(db.func.avg(db.func.cast(DoctorReviewModel.star_rating, Float)), 1).label('avg_review'),
                                   db.func.count(DoctorReviewModel.star_rating).label('review_count'),
                                   )\
            .group_by(DoctorReviewModel.doctor_id).subquery()
        # markers = DoctorModel.query.join(reviews, DoctorModel.doctor_id == reviews.c.doctor_id).all()
        markers = db.session.query(DoctorModel,
                                   reviews).outerjoin(reviews, DoctorModel.doctor_id == reviews.c.doctor_id).all()
        for r in markers:
            doctor_id = r[0]
        return []
