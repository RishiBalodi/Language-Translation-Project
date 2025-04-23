import os
import requests
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get API key from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("Missing GEMINI_API_KEY in environment variables.")

def call_gemini_api(text, target_language, source_language='auto'):
    """
    Calls the Google Gemini API to process the text.
    
    Args:
        text (str): Input text to process.
        target_language (str): Target language code.
        source_language (str): Source language code, or 'auto' for automatic detection.
    
    Returns:
        dict: Response from the Gemini API.
    """
    url = "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateText"

    payload = {
        "prompt": {
            "text": f"Translate the following text from {source_language} to {target_language}: {text}"
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, params={"key": GEMINI_API_KEY}, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP issues

        result = response.json()

        # Extracting the response (adjust based on the actual API response structure)
        if "candidates" in result:
            translated_text = result["candidates"][0]["output"]
            return {
                'success': True,
                'translated_text': translated_text
            }
        else:
            return {'success': False, 'error': 'Unexpected API response format'}

    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    
    if not data or 'text' not in data or 'target_language' not in data:
        return jsonify({'success': False, 'error': 'Missing required parameters'}), 400
    
    text = data['text']
    target_language = data['target_language']
    source_language = data.get('source_language', 'auto')
    
    result = call_gemini_api(text, target_language, source_language)
    return jsonify(result)

@app.route('/available_languages', methods=['GET'])
def get_available_languages():
    languages = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese (Simplified)',
        'zh-TW': 'Chinese (Traditional)',
        'ar': 'Arabic',
        'hi': 'Hindi',
        'ru': 'Russian',
        'pt': 'Portuguese',
        'tr': 'Turkish'
    }
    
    return jsonify({'success': True, 'languages': languages})

if __name__ == '__main__':
    app.run(debug=False) 
