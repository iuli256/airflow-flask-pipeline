from flask import Flask
from flask import jsonify
from flask import request
import pymongo

app = Flask(__name__)


@app.route('/search', methods=['POST'])
def search_address():
  myclient = pymongo.MongoClient("mongodb://root:example@mongo:27017/")
  mydb = myclient["spanish_address"]
  mycol = mydb["posts"]
  if request.is_json:

    # Parse the JSON into a Python dictionary
    req = request.get_json()

    mydoc = mycol.find(req)

    output = []
    for rs in mydoc:
      output.append({'lon': rs['lon'], 'lat': rs['lat'], 'number': rs['number'], 'street': rs['street'],
                     'unit': rs['unit'], 'city': rs['city'], 'district': rs['district'], 'region': rs['region'],
                     'postcode': rs['postcode'], 'id': rs['id'], 'hash': rs['hash']})
    if not mydoc:
      output = "No such name"

    return jsonify({'result' : output})

  else:

    return "Request was not JSON", 400


if __name__ == '__main__':
    app.run(debug=True)