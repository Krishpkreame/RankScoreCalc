from kamarapi import *
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import requests
import json

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


class authkey(Resource):
    def get(self):
        return {'unknown': 'use POST method to get auth key'}

    def post(self):
        data = request.get_json()
        auth = kamar_api.getauthkey(
            data['school'], data['username'], data['password'])
        return auth


class kamarresults(Resource):
    def get(self):
        return {'invalid auth': 'no auth key provided / invalid auth key'}

    def post(self):
        data = request.get_json()
        results = kamar_api.getresults(
            data['school'], data['id'], data['key'])
        return results


api.add_resource(authkey, '/api/v1/auth')
api.add_resource(kamarresults, '/api/v1/results')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)


"""

results = k.getresults()
print("-----------\n", results, "\n-------------")
print(k.student_id, " :\n", len(results))

filterObj = filter_kamar(open("uestandards.json").read())
 sortedKamar = filterObj.filter_results(results)
  # print(sortedKamar)
  sum = 0
   for i in sortedKamar.values():
        print(i, "\n\n")
        for x in i.keys():
            if x == "subject_credits_earned":
                continue
            sum += i[x][2]
    print("rankscore: ", sum)

    return "rankscore: " + str(sum)


"""
