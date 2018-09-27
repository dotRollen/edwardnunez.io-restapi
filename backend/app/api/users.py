from flask import jsonify, abort, request, url_for
from . import api
from backend.app.api.errors import bad_request
from backend.app.email import send_email
from backend.app.models.auth import User


@api.route('/users/', methods=['GET', 'POST'])
def register():
    email = request.json.get('email')
    username = request.json.get('username')
    password = request.json.get('password')
    if email is None or username is None or password is None:
        abort(400)    # missing arguments
    if User.objects(email=email).first() is not None:
        abort(400)    # existing user
    user = User(
        email=email,
        username=username)
    user.password = password
    token = user.generate_confirmation_token()
    send_email(user.email, 'Confirm Your Account',
               'auth/email/confirm', user=user, token=token)
    return (jsonify({'username': user.username}), 201,
            {'Location': url_for('get_user', id=user.id, _external=True)})


@api.route('/users/<string:id>')
def get_user(id):
    user = User.objects.get_or_404(id=id)
    return jsonify(user.to_json())
