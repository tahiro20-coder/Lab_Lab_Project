from flask import Flask, send_from_directory,current_app,jsonify,request,render_template
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
from api.main import Chat
import os
import sys
from api.main import main

app = Flask(__name__, static_url_path='', static_folder='fronted/build')
CORS(app, origins=['https://smart-recycle.onrender.com'], methods=['GET', 'POST'], support_credentials=True)#comment this on deployment
api = Api(app)



@app.route("/", defaults={'path':''})
def serve(path):
    print(app.static_folder)
    
    return send_from_directory(app.static_folder,'index.html')

@app.errorhandler(500)
def internal_server_error(error):
    # Handle internal server errors and include the CORS header in the response
    response = jsonify({'error': 'Internal Server Error'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 500

api.add_resource(Chat, '/chat')
# api.add_resource(Recycle, '/recycle')
app.register_blueprint(main) 