import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify, request, send_from_directory
from flask_socketio import SocketIO,emit
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

users = {}
messages = {}

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/users')
def list_users():
    """Endpoint to return a list of connected users."""
    # Create a list of user details from the users dictionary
    user_list = [{"sid": sid, "username": user_data['username'], "profilePicUrl": user_data['profilePicUrl']} for sid, user_data in users.items()]
    return jsonify(user_list)

@app.route('/messages')
def list_messages():
    """Endpoint to return a list of all messages."""
    # Flatten the messages dictionary into a list of messages with session IDs
    all_messages = []
    for sid, msgs in messages.items():
        for msg in msgs:
            all_messages.append({
                "sid": sid,
                "username": msg["username"],
                "profilePicUrl": msg["profilePicUrl"],
                "text": msg["text"]
            })
    return jsonify(all_messages)

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
    if request.sid not in messages:
        messages[request.sid] = []
    messages[request.sid].append(data)
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

    # If there are no more users connected, clear the messages
    if not users:  # Check if the users dictionary is empty
        messages.clear()  # Empty the messages dictionary
        print("All users have disconnected, clearing all messages.")


if __name__ == "__main__":
    socketio.run(app, debug=True)