import requests
import json
from flask import Flask, jsonify, request, make_response
from flask_restful import Resource, Api
import csv

url = 'http://api.coingecko.com/api/v3/coins/{}/tickers'

app = Flask(__name__)
api = Api(app)
counter = 0
response = {}

class Coins(Resource):
    def post(self):
        global counter        
        counter += 1
        req = request.data.decode()
        header = request.headers['content-type']
        if header == 'application/json':            
            jdata = json.loads(req)
            #print(jdata)
            for coin in jdata["coins"]:
                Coins.coins(coin, req)
        else:
            for coin in req.splitlines()[1:]:
                Coins.coins(coin, req)

    @staticmethod
    def coins(coin, req):
        response["id"] = coin
        response["exchanges"] = []
        response["taskRun"] = counter
        req = requests.get(url.format(coin))
        # Handling too many requests
        if req.status_code == 429:
            #print(response)
            return make_response(jsonify(response), 200)
        #print(req.status_code)
        dic = req.json()
        # Handling {"error":"Could not find coin with the given id"}
        if "error" not in dic.keys():                   
            #print(dic)
            for item in dic["tickers"]:
                response["exchanges"].append(item["market"]["identifier"])
            #print(response)
            return make_response(jsonify(response), 200)

api.add_resource(Coins, '/coins')

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')