from dotenv import load_dotenv
import google.generativeai as genai
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# Load environment variables from a .env file
load_dotenv()

# Configure API key for Google Generative AI
genai.configure(api_key=os.getenv("GEMINI_PRO_API_KEY"))

# Initialize Flask app with CORS support
app = Flask(__name__)
CORS(app)

# Define endpoint to generate JSON from sentences
@app.route("/generate", methods=["PO"])
def generate_json():
    try:
        # Get the list of sentences from the request
        sentences = request.json

        # Validate input format
        if not isinstance(sentences, list):
            return jsonify({"error": "Invalid input format. Expected a list of sentences."}), 400

        # Convert sentences to strings and join them for the prompt
        formatted_sentences = "\n".join([str(sentence) for sentence in sentences])
        
        # Construct the prompt for the model
        prompt = f"""
        Convert the following sentences into a JSON array, where each item is a dictionary with 'heading' and 'description' keys. 
        The 'heading' should be a concise title based on the sentence, using it directly if it's already suitable. 
        For the 'description,' provide a short, casual explanation if the sentence is informal; if the sentence is formal, create 
        a slightly longer and more formal description that clearly explains the heading. Return only the JSON array with no extra 
        text or formatting. The sentences are:
        {formatted_sentences}
        """

        # Generate content using the model
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)

        # Parse and return the result as JSON
        result = json.loads(response.text.strip())
        
        return jsonify(result)

    except json.JSONDecodeError
        return jsonify({"error": "Failed to parse JSON response from AI."}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Start the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
