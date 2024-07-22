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

@app.route('/messages', methods=['GET'])
def messages():
    
    message_list = []
    for m in Message.query.order_by((Message.created_at)).all():
        message_dict = {
            "id": m.id,
            "body": m.body,
            "username": m.username,
            "created_at": m.created_at,
            "updated_at": m.updated_at,
        }
        message_list.append(message_dict)

    response = make_response(
        jsonify(message_list),
        200
    )

    return response

@app.route('/messages', methods=['GET', 'POST'])
def post_message():

    if request.method == 'GET':
       
        for m in Message.query.all():
            message_dict = {
            "id": m.id,
            "body": m.body,
            "username": m.username,
            "created_at": m.created_at,
            "updated_at": m.updated_at,
        }
        

        response = make_response(
            jsonify(message_dict),
            200
        )

        return response

    elif request.method == 'POST':
        
        grab = request.get_json()
        
        username = grab.get("username")
        body = grab.get("body")
        
        new_message = Message(
            body=body,
            username=username
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        new_message_dict = new_message.to_dict()

        response = make_response(
            jsonify(new_message_dict),
            200
        )

        return response

@app.route('/messages/<int:id>')
def messages_by_id(id):

    message = Message.query.filter(Message.id == id).first()
    
    message_dict = message.to_dict()

    response = make_response(
        message_dict,
        200
    )

    return response

@app.route('/messages/<int:id>',  methods=['GET', 'PATCH', 'DELETE'])
def update_message(id):
    
    message = Message.query.filter(Message.id == id).first()

    if message == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)

        return response

    else:
        if request.method == 'GET':
            message_dict = message.to_dict()

            response = make_response(
                message_dict,
                200
            )

            return response

        elif request.method == 'PATCH':
            
            grab = request.get_json()

            body = grab.get("body")  

            up_message = Message(
            body=body,
            )      
               
            db.session.add(up_message)
            db.session.commit()

            updated_message_dict = up_message.to_dict()

            response = make_response(
                updated_message_dict,
                200
            )

            return response

        elif request.method == 'DELETE':
            db.session.delete(message)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Message deleted."
            }

            response = make_response(
                response_body,
                200
            )

            return response

if __name__ == '__main__':
    app.run(port=5555)
