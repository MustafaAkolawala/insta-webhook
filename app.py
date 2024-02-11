from flask import Flask, request , jsonify

app = Flask(__name__)

VERIFY_TOKEN = "qwerty"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403
    elif request.method == "POST":
        payload = request.json
        process_event(payload)  # Custom function to process the event
        return "Event received", 200

def process_event(payload):
    if payload.get("object") == "page":  # Ensure the event is from Instagram Messaging
        for entry in payload.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                if "message" in messaging_event:
                    handle_message(messaging_event)  # Process the incoming message

def handle_message(message_event):
    sender_id = message_event["sender"]["id"]
    message_text = message_event["message"]["text"]
    print(f"Received message from sender {sender_id}: {message_text}")

if __name__ == "__main__":
    app.run(port=5000)