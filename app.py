from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time
import httpx

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
print(f"Key loaded: {GROQ_API_KEY[:15] if GROQ_API_KEY else 'NOT FOUND'}")

@app.route('/')
def home():
    return "Zakoota Chatbot Backend is Running!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '')
    user_type = data.get('user_type', 'client')
    
    try:
        with httpx.Client(timeout=15) as client:
            response = client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json={"model": "llama-3.1-8b-instant", "messages": [{"role": "system", "content": "You are Zing AI Legal Assistant for Pakistan laws."}, {"role": "user", "content": message}], "max_tokens": 200}
            )
        if response.status_code == 200:
            answer = response.json()['choices'][0]['message']['content'].strip()
        else:
            answer = f"API Error: {response.status_code}"
    except Exception as e:
        answer = f"Error: {e}"
    
    return jsonify({"response": answer, "status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5005)))
