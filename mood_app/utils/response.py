from flask import jsonify


def success_response(data=None):
    response = {
        'success': True,
        'message': '成功',
        'data': data
    }
    return jsonify(response)


def error_response(message):
    response = {
        'success': False,
        'message': message,
    }
    return jsonify(response)