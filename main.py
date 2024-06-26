from flask import request, jsonify
from config import db, app
from models import Contact

@app.route('/contact', methods=['GET'])
def get_contact():
    contacts = Contact.query.all()
    jsonify_contacts = [contact.to_json() for contact in contacts]
    return jsonify({'contacts': jsonify_contacts}), 200  # 200 for OK

@app.route('/create', methods=['POST'])
def create_contact():
    first_name = request.json.get('firstName')
    last_name = request.json.get('lastName')
    email = request.json.get('email')
    mobile_number = request.json.get('mobile')

    if not first_name or not last_name or not email or not mobile_number:
        return jsonify({'message': 'You must fill all the details'}), 400  # 400 for Bad Request

    new_contact = Contact(first_name=first_name, last_name=last_name, email=email, mobile_number=mobile_number)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as error:
        return jsonify({'message': str(error)}), 500  # 500 for Internal Server Error
    
    return jsonify({'message': 'User created'}), 201  # 201 for Created

@app.route('/update/<int:user_id>', methods=['PATCH'])
def update_contact(user_id):
    contact = Contact.query.get(user_id)
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404  # 404 for Not Found

    data = request.json
    contact.first_name = data.get('firstName', contact.first_name)
    contact.last_name = data.get('lastName', contact.last_name)
    contact.email = data.get('email', contact.email)
    contact.mobile_number = data.get('mobile', contact.mobile_number)

    db.session.commit()

    return jsonify({'message': 'Contact updated'}), 200  # 200 for OK

@app.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)
    if not contact:
        return jsonify({'message': 'User not found'}), 404  # 404 for Not Found

    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'Contact deleted'}), 200  # 200 for OK

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)