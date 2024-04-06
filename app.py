from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from cryptography.fernet import Fernet

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)

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

if __name__ == "__main__":
    app.run(debug=True)
