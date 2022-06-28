from flask import Flask

#uuid is for session tokens

app = Flask(__name__)
from endpoints import client, client_session, restaurant, restaurant_session, menu

