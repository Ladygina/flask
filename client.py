import requests
from flask import jsonify
from models import Advertisement, Users, Session


session = Session()
session.query(Advertisement).delete()  # удаление если нужно
session.query(Users).delete()
session.commit()

'''POST'''
# # Проверка пользователя
Ivan = session.query(Users).filter(Users.id == 10).first()
if not Ivan:
    Ivan = Users(id=10, username='Ivan')
    session.add(Ivan)
    session.commit()

adv = Advertisement(id=2, header='C++',description='C++ for kids', user_id= Ivan.id)
Ivan.advertisements.append(adv)

response = requests.post('http://127.0.0.1:5000/api/advertisements', json={'id':2, 'header':'C++', 'description':'C++ for kids', 'user_id':Ivan.id})
print(response.status_code, response.text)
session.add(adv)

'''GET'''
response = requests.get('http://127.0.0.1:5000/api/advertisements/2')
print(response.status_code, response.text)


'''PATCH'''
response = requests.patch('http://127.0.0.1:5000/api/advertisements/2', json={'description':'C++ for teenagers'})
print(response.status_code, response.text)


'''DELETE'''
response = requests.delete('http://127.0.0.1:5000/api/advertisements/2')
print(response.status_code)
