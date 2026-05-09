from flask import Flask, request, jsonify
from flask_cors import CORS
import chatbot_logic
import firebase_admin
from firebase_admin import credentials, firestore
import os
import time

app = Flask(__name__)
CORS(app)

# Firebase init
try:
    cred = credentials.Certificate("path/to/your/firebase-credentials.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase connected successfully")
except:
    print("⚠️ Firebase not connected. Using mock data.")
    db = None


@app.route('/')
def home():
    return "Zakoota Chatbot Backend is Running!"


@app.route('/chat', methods=['POST'])
def chat():
    try:
        start_time = time.time()

        data = request.json
        user_message = data.get('message', '')
        user_type = data.get('user_type', 'client')

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        response = chatbot_logic.get_response(user_message, user_type, db)

        end_time = time.time()
        response_time = end_time - start_time

        return jsonify({
            "response": response,
            "status": "success",
            "response_time": f"{response_time:.3f}s"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_lawyers', methods=['GET'])
def get_lawyers():
    try:
        if db:
            lawyers_ref = db.collection('lawyers')
            docs = lawyers_ref.stream()

            lawyers = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                lawyers.append(data)

            return jsonify({"lawyers": lawyers})

        else:
            return jsonify({
                "lawyers": [
                    {"name": "Ali Khan", "specialization": "Family Law", "rating": 4.5},
                    {"name": "Sara Ahmed", "specialization": "Criminal Law", "rating": 4.8}
                ]
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500