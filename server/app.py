from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages' , methods=['GET'])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    messages_list = [message.to_dict() for message in messages]
    return make_response(jsonify(messages_list), 200)


@app.route('/messages/<int:id>' , methods=['GET'])       
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    response = make_response(jsonify(message.t0_dict()))
    return response
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    body = data.get('body')
    username = data.get('username')
    if not body or not username:
        return jsonify({'error': 'Missing required fields'}), 400
    message = Message(body=body, username=username)
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.filter_by(id=id).first()
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    data = request.get_json()
    body = data.get('body')
    if body:
        message.body = body
    db.session.commit()
    return jsonify(message.to_dict()), 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.filter_by(id=id).first()
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted'}), 204





if __name__ == '__main__':
    app.run(port=5555)
