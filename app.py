"""
Basic Encryption & Decryption Using Caesar Cipher
---------------------------------------------------
A simple Flask web application demonstrating the fundamentals of
classical (symmetric substitution) encryption using the Caesar Cipher.

This project is for educational purposes only and demonstrates the
underlying logic of the Caesar Cipher. It intentionally avoids any
external cryptography libraries so that the shift-based math is visible.
"""

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# ---------------------------------------------------------------------------
# CORE CAESAR CIPHER LOGIC
# ---------------------------------------------------------------------------

def caesar_encrypt(text, shift):
    """
    Encrypts the given text using the Caesar Cipher formula:
        E(x) = (x + n) % 26

    - Preserves uppercase and lowercase letters.
    - Leaves spaces, numbers, punctuation, and special characters unchanged.
    """
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26
            result.append(chr(shifted + base))
        else:
            # Numbers, spaces, punctuation, special characters stay the same
            result.append(char)
    return "".join(result)


def caesar_decrypt(text, shift):
    """
    Decrypts the given text using the reverse Caesar Cipher formula:
        D(x) = (x - n) % 26

    Uses the same shift key that was used for encryption.
    """
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base - shift) % 26
            result.append(chr(shifted + base))
        else:
            result.append(char)
    return "".join(result)


def validate_shift(shift_value):
    """
    Validates that the provided shift value is a valid integer.
    Returns (is_valid, shift_int_or_None, error_message_or_None)
    """
    try:
        shift_int = int(shift_value)
        return True, shift_int, None
    except (TypeError, ValueError):
        return False, None, "Shift key must be a valid whole number (e.g., 3)."


def validate_text(text_value):
    """
    Validates that text input is present and not empty/whitespace-only.
    Returns (is_valid, error_message_or_None)
    """
    if text_value is None or text_value.strip() == "":
        return False, "Text field cannot be empty. Please enter some text."
    return True, None


# ---------------------------------------------------------------------------
# FLASK ROUTES
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Render the main dashboard page."""
    return render_template("index.html")


@app.route("/encrypt", methods=["POST"])
def encrypt_route():
    """
    Handles encryption requests.
    Expects JSON: { "text": "...", "shift": "..." }
    Returns JSON: { "success": bool, "result": "...", "error": "..." }
    """
    try:
        data = request.get_json(silent=True) or {}
        text = data.get("text", "")
        shift_raw = data.get("shift", "")

        text_valid, text_error = validate_text(text)
        if not text_valid:
            return jsonify({"success": False, "error": text_error}), 400

        shift_valid, shift_int, shift_error = validate_shift(shift_raw)
        if not shift_valid:
            return jsonify({"success": False, "error": shift_error}), 400

        # Normalize shift to a 0-25 range for consistency
        normalized_shift = shift_int % 26

        encrypted_text = caesar_encrypt(text, normalized_shift)

        # Self-verification: decrypting the result should return the original
        decrypted_check = caesar_decrypt(encrypted_text, normalized_shift)
        verified = (decrypted_check == text)

        return jsonify({
            "success": True,
            "original": text,
            "shift": shift_int,
            "result": encrypted_text,
            "verified": verified
        })

    except Exception as exc:  # Friendly fallback for unexpected server errors
        return jsonify({
            "success": False,
            "error": f"An unexpected server error occurred: {str(exc)}"
        }), 500


@app.route("/decrypt", methods=["POST"])
def decrypt_route():
    """
    Handles decryption requests.
    Expects JSON: { "text": "...", "shift": "..." }
    Returns JSON: { "success": bool, "result": "...", "error": "..." }
    """
    try:
        data = request.get_json(silent=True) or {}
        text = data.get("text", "")
        shift_raw = data.get("shift", "")

        text_valid, text_error = validate_text(text)
        if not text_valid:
            return jsonify({"success": False, "error": text_error}), 400

        shift_valid, shift_int, shift_error = validate_shift(shift_raw)
        if not shift_valid:
            return jsonify({"success": False, "error": shift_error}), 400

        normalized_shift = shift_int % 26

        decrypted_text = caesar_decrypt(text, normalized_shift)

        return jsonify({
            "success": True,
            "original": text,
            "shift": shift_int,
            "result": decrypted_text
        })

    except Exception as exc:
        return jsonify({
            "success": False,
            "error": f"An unexpected server error occurred: {str(exc)}"
        }), 500


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)
