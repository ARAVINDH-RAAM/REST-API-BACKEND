from flask import Flask, request, jsonify
import logging
import re
import base64
import mimetypes

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

def handle_file(file_b64):
    try:
        file_data = base64.b64decode(file_b64)
        file_size_kb = len(file_data) // 1024  

        mime_type = mimetypes.guess_type(file_b64)[0]

        if mime_type:
            return True, mime_type, file_size_kb
        else:
            return False, None, None

    except Exception as e:
        logging.error(f"File processing error: {e}")
        return False, None, None

@app.route('/bfhl', methods=['POST'])
def process_request():
    try:
        data = request.get_json()
        logging.info(f"Received data: {data}")

        full_name = "john_doe"
        dob = "17091999"
        email = "john@xyz.com"
        roll_number = "ABCD123"
        user_id = f"{full_name}_{dob}"

        data_list = data.get("data", [])
        
        file_b64 = data.get("file_b64")
        file_valid = False
        file_mime_type = None
        file_size_kb = None

        if file_b64:
            file_valid, file_mime_type, file_size_kb = handle_file(file_b64)

        numbers = [item for item in data_list if item.isdigit()]
        alphabets = [item for item in data_list if item.isalpha()]

        lowercase_alphabets = [char for char in alphabets if char.islower()]
        highest_lowercase_alphabet = max(lowercase_alphabets) if lowercase_alphabets else None

        response = {
            "is_success": True,
            "user_id": user_id,
            "email": email,
            "roll_number": roll_number,
            "numbers": numbers,
            "alphabets": alphabets,
            "highest_lowercase_alphabet": [highest_lowercase_alphabet] if highest_lowercase_alphabet else [],
            "file_valid": file_valid,
            "file_mime_type": file_mime_type,
            "file_size_kb": file_size_kb
        }

        logging.info(f"Response to send: {response}")
        return jsonify(response), 200

    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({"is_success": False, "error": str(e)}), 400

@app.route('/bfhl', methods=['GET'])
def operation_code():
    return jsonify({"operation_code": 1}), 200

if __name__ == '__main__':
    app.run(debug=True)
