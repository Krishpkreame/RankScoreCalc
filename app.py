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
        print("AUTHKEY -\npost request received")
        print("data :\n", data)
        auth = kamar_api.getauthkey(
            data['school'], data['username'], data['password'])
        print("--------------------------\n",
              "Returning :\n", auth)
        return auth


class kamarresults(Resource):
    def get(self):
        return {'invalid auth': 'no auth key provided / invalid auth key'}

    def post(self):
        data = request.get_json()
        print("RESULTS -\npost request received")
        print("data :\n", data)
        results = kamar_api.getresults(
            data['school'], data['id'], data['key'])
        print("--------------------------\n",
              "Returning :\n", results)
        return results


api.add_resource(authkey, '/api/v1/auth')
api.add_resource(kamarresults, '/api/v1/results')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
