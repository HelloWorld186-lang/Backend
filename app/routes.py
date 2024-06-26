from flask import Blueprint, request, jsonify
from app import db
from app.models import Contact

main = Blueprint('main', __name__)

@main.route('/contact', methods=['GET'])
def get_contact():
    contacts = Contact.query.all()
    jsonify_contacts = [contact.to_json() for contact in contacts]
    return jsonify({'contacts': jsonify_contacts}), 200

@main.route('/create', methods=['POST'])
def create_contact():
    data = request.json
    if not all(key in data for key in ('firstName', 'lastName', 'email', 'mobile')):
        return jsonify({'message': 'You must fill all the details'}), 400

    new_contact = Contact(
        first_name=data['firstName'],
        last_name=data['lastName'],
        email=data['email'],
        mobile_number=data['mobile']
    )
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as error:
        return jsonify({'message': str(error)}), 500

    return jsonify({'message': 'User created'}), 201

@main.route('/update/<int:user_id>', methods=['PATCH'])
def update_contact(user_id):
    contact = Contact.query.get(user_id)
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404

    data = request.json
    contact.first_name = data.get('firstName', contact.first_name)
    contact.last_name = data.get('lastName', contact.last_name)
    contact.email = data.get('email', contact.email)
    contact.mobile_number = data.get('mobile', contact.mobile_number)

    db.session.commit()
    return jsonify({'message': 'Contact updated'}), 200

@main.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)
    if not contact:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'Contact deleted'}), 200