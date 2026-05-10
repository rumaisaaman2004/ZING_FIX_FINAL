import os
import httpx
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_AVAILABLE = bool(GROQ_API_KEY)
print(f"✅ Groq AI Ready - Key: {GROQ_API_KEY[:10] if GROQ_API_KEY else 'NOT FOUND'}")

class Chatbot:
    def __init__(self):
        self.legal_qa = {
            'divorce': 'In Pakistan, divorce can be through Talaq, Khula, or court decree.',
            'hello': "Hello! I'm Zing AI Legal Assistant.",
            'hi': 'Hi! Need legal assistance?',
        }
        self.greetings = ['hello', 'hi', 'hey', 'assalam', 'salam']

    def _get_groq_response(self, message, user_type):
        if not GROQ_AVAILABLE:
            return "API key not found"
        try:
            with httpx.Client(timeout=15) as client:
                response = client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                    json={"model": "llama-3.1-8b-instant", "messages": [{"role": "system", "content": "You are Zing AI Legal Assistant for Pakistan laws."}, {"role": "user", "content": message}], "max_tokens": 200, "temperature": 0.3}
                )
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content'].strip()
            else:
                print(f"Groq Error: {response.status_code} - {response.text}")
                return f"API Error: {response.status_code}"
        except Exception as e:
            print(f"Exception: {e}")
            return f"Error: {e}"

    def get_response(self, user_message, user_type, db=None):
        msg = user_message.lower().strip()
        if any(g in msg for g in self.greetings):
            return "Hello! I'm Zing AI Legal Assistant. How can I help you?"
        if msg in self.legal_qa:
            return self.legal_qa[msg]
        return self._get_groq_response(user_message, user_type)

chatbot = Chatbot()

def get_response(user_message, user_type, db=None):
    return chatbot.get_response(user_message, user_type, db)
