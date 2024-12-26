from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__, 
    template_folder='../templates',  # Add this line
    static_folder='../static'        # Add this line
)

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-branded-caption', methods=['POST'])
def generate_branded_caption_route():
    # Your existing code here
    pass

@app.route('/generate-news-content', methods=['POST'])
def generate_news_content_route():
    # Your existing code here
    pass

@app.route('/upload', methods=['POST'])
def upload_file():
    # Your existing code here
    pass

# Add this for Vercel
if __name__ == '__main__':
    app.run()
