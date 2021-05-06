from flask import Flask, send_from_directory
from flask_restful import Api
from batch.db import db
from batch.resources.Doctor import Doctor
from batch.utils.utils import get_database_connection_string
from batch.resources.DoctorReview import DoctorReview
from batch.resources.DoctorMarker import DoctorMarkerList
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_connection_string()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/')
def index():
    return "FlashHeal API main page"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


SWAGGER_URL = '/api'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "FlashHeal API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

api.add_resource(Doctor, '/doctors', '/doctors/<int:doctor_id>')
api.add_resource(DoctorReview, '/doctor-reviews/<int:doctor_id>')
api.add_resource(DoctorMarkerList, '/doctor-markers')

if __name__ == "__main__":
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000)
