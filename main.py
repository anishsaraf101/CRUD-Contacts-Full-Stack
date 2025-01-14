# CRUD functionality (Create, Read, Update, and Delete)

import json
from flask import request, jsonify
from config import app, db
from models import Contact

@app.route("/contacts", methods=["GET"]) # only allow the get method in the "/contacts" URL
def get_contacts(): # used for reading the contacts
    contacts = Contact.query.all() # get all the contacts
    json_contacts = list(map(lambda x: x.to_json(), contacts)) # turn contacts into json type
    return jsonify({"contacts": json_contacts}) # return json set of contacts

@app.route("/create_contact", methods = ["POST"]) # POST method is for creating data
def create_contact():
    first_name = request.json.get("firstName") # get all the JSON data
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email: # make sure we have all info
        return (
            jsonify({"message": "You must include a first name, last name, and email"}),
            400,
        )
    
    new_contact = Contact(first_name = first_name, last_name = last_name, email = email) # create the contact
    try:
        db.session.add(new_contact) # adds contact to staging area
        db.session.commit()         # actually commits changes to database permanently (errors may occur)
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "User created!"}), 201

@app.route("/update_contact/<int:user_id>", methods = ["PATCH"]) # ability to update a contact
def update_contact(user_id): 
    contact = Contact.query.get(user_id) # use URL to get user_id

    if not contact:
        return jsonify({"message": "User not found"}), 404 # make sure contact_id is in database
    
    data = request.json
    contact.first_name = data.get("firstName", contact.first_name)
    contact.last_name = data.get("lastName", contact.last_name)
    contact.email = data.get("email", contact.email)

    db.session.commit()

    return jsonify({"message": "User updated!"}), 200
    
@app.route("/delete_contact/<int:user_id>", methods = ["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return (jsonify({"message": "User not found"}), 404)
    
    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200   # successful delete


if __name__ == "__main__": # added to make sure code is only run when this file is ran; does not automatically run when another file imports this and runs all the code beforehand
    with app.app_context():
        db.create_all()
       
    app.run(debug = True)

