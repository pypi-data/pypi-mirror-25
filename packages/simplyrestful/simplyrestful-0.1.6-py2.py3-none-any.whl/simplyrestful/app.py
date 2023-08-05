from flask import Flask, jsonify
from flask_restful import Api
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
api = Api(app)

app.url_map.strict_slashes = False


@app.errorhandler(IntegrityError)
def integrity_error(e):
    return jsonify(dict(message='Integrity error', detail=str(e))), 409


@app.errorhandler(Exception)
def unknown_error(e):
    return jsonify(dict(message='Unknown error', detail=str(e))), 500


@app.teardown_appcontext
def shutdown_session(exception=None):
    from database import session
    session.close()
