import requests
from flask import jsonify
from models import Advertisement, Users


# response = requests.post('http://127.0.0.1:5000/api/advertisements', json={'header':'C++', 'description':'C++ for kids','user':'Ivan' })
# print(response.status_code, response.text)


response = requests.get('http://127.0.0.1:5000/api/advertisements/2')
print(response.status_code, response.text)
# #
# # response = requests.delete('http://127.0.0.1:5000/api/advertisements/3')
# response = requests.post('http://127.0.0.1:5000/api/advertisements', json={'header':'house','description':'Ivanjh mnj gh'})
# print(response.status_code)
