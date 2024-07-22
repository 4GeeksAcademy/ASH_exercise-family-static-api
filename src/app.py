"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# aca aranco a editar el ejercicio
# @app.route('/members', methods=['GET'])
# def handle_hello():

#     # this is how you can use the Family datastructure by calling its methods
#     members = jackson_family.get_all_members()
#     response_body = {
#         "hello": "world",
#         "family": members
#     }


#     return jsonify(response_body), 200

# GET ALL MEMBER
@app.route('/members', methods=['GET'])
def get_all_mems():

    members = jackson_family.get_all_members()
   
    return jsonify(members), 200

# GET MEMBER
@app.route('/member/<int:member_id>', methods=['GET'])
def get_mem(member_id):

    member = jackson_family.get_member(member_id)
    response_body = {
        'member': member
    }
    # response_body = {
    #     "name": member['first_name'],
    #     "id": member['id'],
    #     "age": member['age'],
    #     "lucky_numbers": member['lucky_numbers']
    # }

    return jsonify(response_body), 200

# ADD NEW MEMBER
@app.route('/member', methods=['POST'])
def add_mem():
    request_data = request.get_json()
    new_member_id = jackson_family._generateId()

    new_member = {
        'id': new_member_id,
        'first_name': request_data.get('first_name', ''),
        'age': request_data.get('age', None),
        'lucky_numbers': request_data.get('lucky_numbers', [])
        }

    jackson_family.add_member(new_member)

    response_body = {
        "member": new_member
    }

    return jsonify(response_body), 200

# DELETE MEMBER
@app.route('/member/<int:member_id>', methods=['DELETE'])
def del_mem(member_id):
    jackson_family.delete_member(member_id)

    response_body = {
        "done": True
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
