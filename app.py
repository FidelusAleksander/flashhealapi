from flask import Flask
from flask_restful import Api
import simplejson as json
# from SqlReader import SqlReader


# with open('db_config.json') as config_file:
#     conf_str = config_file.read()
#     db_config = json.loads(conf_str)

app = Flask(__name__)
# api = Api(app)

# reader = SqlReader(db_config)


@app.route('/doctors/', defaults={'specialty': 'all'})
@app.route('/doctors/<string:specialty>',methods = ['GET'])
def doctors_all_or_by_specialty(specialty):
    return {"results" : specialty}
    # result = reader.fetch(specialty)
    # return json.dumps(result, use_decimal=True)


if __name__ == "__main__":
    app.run()
