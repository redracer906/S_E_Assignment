from flask import Flask, request, jsonify

app = Flask(__name__)

# Three valid API keys for 3 different consumers/testers
VALID_API_KEYS = {
    "key_consumer_1": "Tester 1 (Alpha)",
    "key_consumer_2": "Tester 2 (Beta)",
    "key_consumer_3": "Tester 3 (Gamma)"
}

@app.route('/process', methods=['POST'])
def process_text():
    # Retrieve X-API-Key from HTTP request header
    api_key = request.headers.get('X-API-Key')

    # Validate the API key
    if not api_key:
        return jsonify({
            "status": "error",
            "message": "API Key Missing! Please provide 'X-API-Key' in the HTTP header."
        }), 401

    if api_key not in VALID_API_KEYS:
        return jsonify({
            "status": "error",
            "message": "Invalid API Key! Access denied."
        }), 403

    # Parse JSON body
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({
            "status": "error",
            "message": "Invalid payload! 'text' field is required in JSON."
        }), 400

    input_text = data['text']
    processed_text = input_text.upper()

    return jsonify({
        "status": "success",
        "consumer": VALID_API_KEYS[api_key],
        "original_text": input_text,
        "processed_text": processed_text
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
