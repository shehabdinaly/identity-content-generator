from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-branded-caption', methods=['POST'])
def generate_branded_caption_route():
    try:
        text_input = request.form.get('text_input', '')
        style = request.form.get('style', 'default')
        
        if not text_input:
            text_input = "Generate a general branded content piece"
        
        versions = generate_branded_caption(text_input, style)
        
        if versions is None:
            return jsonify({"error": "Failed to generate captions"}), 500

        return jsonify({
            "caption1": versions[0],
            "caption2": versions[1],
            "caption3": versions[2]
        })
    
    except Exception as e:
        print(f"Error in generate_branded_caption: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Add your other routes here...

if __name__ == '__main__':
    app.run()
