from flask import request, Response, Blueprint
from mongoengine import *
from werkzeug.security import check_password_hash, generate_password_hash
import json

bp = Blueprint('auth', __name__, url_prefix='/auth')

connect('users')

@bp.route("/register", methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'username required'
        elif not password:
            error = 'password required'
        elif len(UserInfo.objects(username=username)) is not 0:
            error = 'username is already registered'

        if error is None:
            result = UserInfo(username=username, password=generate_password_hash(password))
            result.save()
            print('One post: {0}:{1}'.format(result.username, result.password))
            return json.dumps({'username': username})
        return Response(error, status=500)

    return Response('Please use a POST request', status=500)

@bp.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        
        user = UserInfo.objects(username=username)

        if len(user) is 0:
            error = 'incorrect username'
        elif not check_password_hash(user[0]['password'], password):
            error = 'incorrect password'

        if error is None:
            return json.dumps({'username': username})
        return Response(error, status=500)

    return Response('Please use a POST request', status=500)

class UserInfo(Document):
    username = StringField(required = True)
    password = StringField(required = True)
