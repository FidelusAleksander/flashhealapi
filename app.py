from flask import Flask
import simplejson as json
from SqlReader import SqlReader

with open('config.json') as config_file:
    conf_str = config_file.read()
    conf = json.loads(conf_str)

app = Flask(__name__)

reader = SqlReader(conf['SQL_DATABASE'])


@app.route('/doctors/', defaults={'specialty': 'all'})
@app.route('/doctors/<string:specialty>', methods=['GET'])
def doctors_all_or_by_specialty(specialty):
    try:
        results = reader.fetch_doctors(specialty)
        return json.dumps(results, use_decimal=True)
    except Exception as e:
        return {"Failed, message:": str(e)}


@app.route('/doctorDetails/<int:doctor_id>', methods=['GET'])
def doctor_details_by_id(doctor_id):
    try:
        results = reader.fetch_doctor_details(doctor_id)
        return json.dumps(results, use_decimal=True)
    except Exception as e:
        return {"Failed, message:": str(e)}


@app.route('/')
def index():
    return "Flashhealapi main page"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
