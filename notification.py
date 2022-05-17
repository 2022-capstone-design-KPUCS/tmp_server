from flask import jsonify, request
from flask_restx import Resource, Namespace

Notification = Namespace('Notification')

@Notification.route('/token/')
@Notification.route('/token/<string:token>')
class Token:  
    def get(self):
        return self.token

    def post(self, token):
        content = request.get_json()
        self.token = ""
        if content['data']:
            self.token = content['data']

        return self.token
