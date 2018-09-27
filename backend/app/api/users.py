from flask import jsonify, abort, request, url_for
from . import api
from backend.app.api.errors import bad_request
from backend.app.email import send_email
from backend.app.models.auth import User


@api.route('/users', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.json.get('email')
        return (
            jsonify({
                'message': f'Received request for {email} registration!',
                'url': 'todo'
            }),
            201,
        )
    else:
        users = User.objects()
        users_list = []
        for user in users:
            users_list.append(user.to_json())
        return (
            jsonify({
                'users': users_list
            }),
            201,
        )


@api.route('/users/<string:id>')
def get_user(id):
    user = User.objects.get_or_404(id=id)
    return jsonify(user.to_json())
