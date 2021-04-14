from flask import Flask
from flask_restful import Api
from batch.db import db
from batch.resources.Doctor import DoctorList
from batch.utils.utils import get_database_connection_string

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_connection_string()


@app.route('/')
def index():
    return "Flashhealapi main page"


api.add_resource(DoctorList, '/doctors')

if __name__ == "__main__":
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000)
