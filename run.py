from waitress import serve
from server import app  # или из твоего файла импортируй объект Flask

serve(app, host='127.0.0.1', port=5000)