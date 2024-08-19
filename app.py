from dotenv import load_dotenv
import google.generativeai as genai
import os
from flask import Flask, jsonify
from flask_cors import CORS
import json
from functools import lru_cache

# Load environment variables from .env file
load_dotenv()

# Configure the generative AI API key
genai.configure(api_key=os.getenv("GEMINI_PRO_API_KEY"))

app = Flask(__name__)
CORS(app)

prompt = """
Convert the following sentences into a JSON array with 'heading' and 'description' keys. The 'heading' should be a concise title. 
For the 'description,' provide a short, casual explanation for informal sentences, and a slightly longer, formal explanation for formal sentences. 
Return only the JSON array. The sentences are:
"""

transcript = """
Gathering Requirements
Planning and Scheduling
Design and Development
Testing and Quality Assurance
Deployment and Implementation
Monitoring and Maintenance
"""

# Cache the result of the AI model call to avoid unnecessary repeated API requests
@lru_cache(maxsize=10)
def generate_json_from_ai(prompt, transcript):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt + transcript)
    
    # Clean and parse the JSON response
    return json.loads(response.text.strip())

@app.get("/")
def get():
    try:
        result = generate_json_from_ai(prompt, transcript)
        return jsonify(result)  # Return the result as JSON
    except json.JSONDecodeError:
        return jsonify({"error": "Failed to parse JSON response from AI."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error message as JSON with status code 500

if __name__ == "__main__":
    # Run the app with multiple threads to handle concurrent requests
    app.run(host="0.0.0.0", port=5000, threaded=True)
