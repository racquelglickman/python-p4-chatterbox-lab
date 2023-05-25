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

@app.route('/')
def index():
    return '<h1>Chatterbox Lab</h1>'

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    
    if request.method == 'GET':
        
        messages = []
        for message in Message.query.all():
            message_dict = message.to_dict()
            messages.append(message_dict)

        return messages, 200
    
    elif request.method == 'POST':
        new_message = Message(
            body=request.get_json()['body'],
            username=request.get_json()['username'],
        )

        db.session.add(new_message)
        db.session.commit()
        
        message_dict = new_message.to_dict()

        return message_dict, 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):

    message = Message.query.filter(Message.id == id).first()

    if request.method == 'PATCH':
        for attr in request.get_json():
            setattr(message, attr, request.get_json().get(attr))

        db.session.add(message)
        db.session.commit()
        
        message_dict = message.to_dict()

        return message_dict, 200

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Review deleted."    
        }

        return response_body, 200

if __name__ == '__main__':
    app.run(port=5555)
