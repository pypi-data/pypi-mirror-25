from flask import request
from flask_restful import Resource as FlaskResource


class Resource(FlaskResource):
    endpoint = ''
    serializer = None

    def __init__(self):
        self._serializer = self.serializer()

    def post(self):
        return self._serializer.create(request.json), 201

    def put(self, id):
        return self._serializer.update(id, request.json)

    def delete(self, id):
        return self._serializer.delete(id), 204

    def get(self, id=None):
        return self._serializer.read(id) if id else self._serializer.list(
            request.args.to_dict()
        )
