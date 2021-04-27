from flask import Flask
from flask_restful import Api
from batch.db import db
from batch.resources.Doctor import DoctorList, Doctor
from batch.utils.utils import get_database_connection_string
from batch.resources.DoctorReview import DoctorReview


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_connection_string()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def index():
    return "Flashhealapi main page"


api.add_resource(Doctor, '/doctor')
api.add_resource(DoctorList, '/doctors')
api.add_resource(DoctorReview, '/doctor-review/<int:doctor_id>')

if __name__ == "__main__":
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000)
