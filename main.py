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
        print(type(data), data)
        school = data['school']
        user = data['username']
        pswd = data['password']
        auth = kamar_api.getauthkey(school, user, pswd)
        return auth


class get_posts_test(Resource):
    def get(self, num):
        r = requests.get('https://jsonplaceholder.typicode.com/posts')
        return json.loads(r.text)


api.add_resource(authkey, '/api/v1')
api.add_resource(get_posts_test, '/getpoststest/<int:num>')

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
