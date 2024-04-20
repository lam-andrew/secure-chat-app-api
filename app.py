import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO,emit
from flask_cors import CORS, cross_origin
from cryptography.fernet import Fernet

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

# Generate a key and instantiate a Fernet object
# Note: Figure out a way to rotate them (extra features)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route("/flask/test")
@cross_origin()
def test():
    return {"items": ["This is from Flask", "Successfully hit the Flask backend", "Don't forget to deal with CORS"]}

@app.route("/flask/echo", methods=['POST'])
@cross_origin()
def echo():
    data = request.json
    user_message = data.get('message')
    if user_message:
        # Encrypt the message
        encrypted_message = cipher_suite.encrypt(user_message.encode('utf-8'))

        # Decrypt the message
        decrypted_message = cipher_suite.decrypt(encrypted_message).decode('utf-8')

        # Making sure it works by printing them out
        return jsonify({"encrypted": encrypted_message.decode('utf-8'), "decrypted": decrypted_message})
    else:
        return jsonify({"response": "No message received."}), 400

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

# Socket Routes
@app.route("/http-call")
def http_call():
    """return JSON with string data as the value"""
    data = {'data':'This text was fetched using an HTTP call to server on render.'}
    return jsonify(data)

# @socketio.on("connect")
# def connected():
#     """event listener when client connects to the server"""
#     print(request.sid)
#     print("client has connected")
#     emit("connect",{"data":f"id: {request.sid} is connected"})

@socketio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ",str(data))
    emit("data",{'data':data,'id':request.sid},broadcast=True)

# @socketio.on("disconnect")
# def disconnected():
#     """event listener when client disconnects to the server"""
#     print("user disconnected")
#     emit("disconnect",f"user {request.sid} disconnected",broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)
