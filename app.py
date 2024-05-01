import eventlet
eventlet.monkey_patch()

from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO,emit
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

users = {}

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

# Socket Routes 
@socketio.on('register')
def handle_register(data):
    """Receive and store user data upon connection."""
    users[request.sid] = data
    print(f"User registered: {data['username']}")
    emit('userConnected', {'username': data['username'], 'profilePicUrl': data['profilePicUrl']}, broadcast=True)

@socketio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    emit("data",{'data': data["text"],'sid': request.sid, 'username': data["username"], 'profilePicUrl': data["profilePicUrl"]},broadcast=True)

@socketio.on("connect")
def connected():
    """Event listener when client connects to the server."""
    print(f"client {request.sid} has connected")

@socketio.on("disconnect")
def disconnected():
    """Event listener when client disconnects from the server."""
    user_info = users.pop(request.sid, {})  # Remove user info
    username = user_info.get('username', 'A user')
    print(f"user {request.sid} ({username}) disconnected")
    emit("userDisconnected", {'username': username}, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)