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

# Return list of users to frontend
@app.route('/users')
def list_users():
    """Endpoint to return a list of connected users."""
    # Create a list of user details from the users dictionary
    user_list = [{"sid": sid, "username": user_data['username'], "profilePicUrl": user_data['profilePicUrl']} for sid, user_data in users.items()]
    return jsonify(user_list)

# Return list of messages to frontend
@app.route('/messages')
def list_messages():
    """Endpoint to return a list of all messages."""
    # Flatten the messages dictionary into a list of messages with session IDs
    all_messages = []
    for sid, msgs in messages.items():
        for msg in msgs:
            all_messages.append({
                "sid": sid,
                "googleId": msg["googleId"],
                "username": msg["username"],
                "profilePicUrl": msg["profilePicUrl"],
                "text": msg["text"],
                "from": msg["from"],
                "timestamp": msg["timestamp"]
            })
    return jsonify(all_messages)

# Socket Routes 
@socketio.on('register')
def handle_register(data):
    """Receive and store user data upon connection."""
    users[request.sid] = data
    print(f"User registered: {data['username']}")
    emit('userConnected', {'username': data['username'], 'profilePicUrl': data['profilePicUrl'], 'googleId': data['googleId']}, broadcast=True)

# Listen to client that send messages through the socket and broadcast message to all other clients
@socketio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    if request.sid not in messages:
        messages[request.sid] = []
    messages[request.sid].append(data)
    emit("data",{'data': data["text"],'sid': request.sid, 'username': data["username"], 'googleId': data["googleId"], 'profilePicUrl': data["profilePicUrl"], 'from': data["from"], 'timestamp': data["timestamp"]},broadcast=True)

# Listen to clients that connect to the socket
@socketio.on("connect")
def connected():
    """Event listener when client connects to the server."""
    print(f"client {request.sid} has connected")

# Listen to clients that disconnect from the socket
@socketio.on("disconnect")
def disconnected():
    """Event listener when client disconnects from the server."""
    user_info = users.pop(request.sid, {})  # Remove user info
    username = user_info.get('username', 'A user')
    googleId = user_info.get('googleId')
    print(f"user {request.sid} ({username}, {googleId}) disconnected")
    emit("userDisconnected", {'username': username, 'googleId': googleId}, broadcast=True)

    # If there are no more users connected, clear the messages
    if not users:  # Check if the users dictionary is empty
        messages.clear()  # Empty the messages dictionary
        print("All users have disconnected, clearing all messages.")


if __name__ == "__main__":
    socketio.run(app, debug=True)