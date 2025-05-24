import datetime

import requests
from flask import Flask, jsonify,request
#from requests import request
from flask.views import MethodView
from models import Advertisement, Session
from sqlalchemy.exc import IntegrityError
from flask_debugtoolbar import DebugToolbarExtension
from errors import HttpError
import pydantic
from schema import *

app = Flask('app')

@app.errorhandler(HttpError)
def http_handler(err:HttpError):
    http_response = jsonify({'error':err.message})
    http_response.status_code = err.status_code
    return http_response

def get_advertisement(advertisement_id):
    adv = request.session.get(Advertisement,advertisement_id)
    if adv is None:
        raise HttpError('404', 'advertisement not found')
    return adv

@app.before_request
def before_request():
    session = Session()
    request.session = session

@app.after_request
def after_request(response):
    request.session.commit()
    request.session.close()
    return response
def add_advertisement(advertisement):
    request.session.add(advertisement)
    try:
        request.session.commit()
    except IntegrityError:
        response = jsonify({'error': 'advertisement already exists'})
        response.status_code = 409
        return response

class SitesView(MethodView):
    def get(self, advertisement_id:int):
        print('Get received')

        advertisement = get_advertisement(advertisement_id)
        return jsonify(advertisement.dict)

    def post(self):
        print("Received POST request")
        data = request.json
        print('data', data, type(data))
        data = validate_json(request.json, CreateAdvertisement)
        print("Validated data:", data)
        advertisement = Advertisement(id=data['id'],
                                      header=data['header'],
                                      description=data['description'],
                                      user_id=data['user_id'],
                                      registration_time= datetime.datetime.now())
        add_advertisement(advertisement)
        return jsonify(advertisement.dict)


    def patch(self, advertisement_id: int):
        advertisement = get_advertisement(advertisement_id)
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Обновляем поля, которые пришли в PATCH
        if 'description' in data:
            advertisement.description = data['description']
        if 'header' in data:
            advertisement.header = data['header']
        # и так далее для других полей, если нужно

        request.session.commit()
        return jsonify(advertisement.dict)


    def delete(self,advertisement_id:int):
            advertisement = get_advertisement(advertisement_id)
            request.session.delete(advertisement)
            request.session.commit()
            return jsonify({'message':'advertisement deleted'})

sites_view = SitesView.as_view('sites_view')
app.add_url_rule("/api/advertisements/<int:advertisement_id>", view_func=sites_view, methods=['GET','PATCH','DELETE'])
app.add_url_rule("/api/advertisements", view_func=sites_view, methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True)
