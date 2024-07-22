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
    if members:
        return jsonify(members), 200
    return jsonify({"error": "Members not found"}), 400

# GET MEMBER
@app.route('/member/<int:id>', methods=['GET'])
def get_mem(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 400

# ADD NEW MEMBER
@app.route('/member', methods=['POST'])
def add_mem():
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "no data provided"}), 400
    
    new_id = request_data.get('id', None)
    new_name = request_data.get('first_name', '')
    new_age = request_data.get('age', None)
    new_lucky_numbers= request_data.get('lucky_numbers', [])

    if not isinstance(new_name, str):
        return jsonify({"error": "'first_name' must be a string"}), 400
    if not isinstance(new_age, int) or new_age <= 0:
        return jsonify({"error": "'age' must be an integer >0"}), 400
    if not isinstance(new_lucky_numbers, list) or not all(isinstance(num, int) for num in new_lucky_numbers):
        return jsonify({"error": "'lucky_numbers' must be a list of integers"}), 400
    if new_id:
        new_member_id = new_id
    else: 
        new_member_id = jackson_family._generateId()
        
    new_member = {
        'id': new_member_id,
        'first_name': new_name,
        'age': new_age,
        'lucky_numbers': new_lucky_numbers
        }

    jackson_family.add_member(new_member)
    
    return jsonify(new_member), 200

# DELETE MEMBER
@app.route('/member/<int:id>', methods=['DELETE'])
def del_mem(id):
    # member = jackson_family.get_member(id)
    # if member is None:
    #     return jsonify({"error": "Member not found"}), 400


    jackson_family.delete_member(id)

    response_body = {
        "done": True
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
