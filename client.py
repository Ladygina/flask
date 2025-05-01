import requests
from flask import jsonify

# response = requests.post('http://127.0.0.1:5000/api/advertisements', json={'header':'C++', 'description':'C++ for kids','owner':'Ivan' })
# print(response.status_code, response.text)

response = requests.get('http://127.0.0.1:5000/api/advertisements/1')
print(response.status_code, response.text)
#
# # response = requests.delete('http://127.0.0.1:5000/api/advertisements/3')
# response = requests.post('http://127.0.0.1:5000/api/advertisements', json={'header':'house','description':'Ivanjh mnj gh'})
# print(response.status_code)
