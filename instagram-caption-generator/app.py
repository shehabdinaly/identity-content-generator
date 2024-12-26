from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

@app.route('/generate-news-content', methods=['POST'])
def generate_news_content_route():
    try:
        text_input = request.form.get('text_input', '')
        
        if not text_input:
            text_input = "Generate a general news piece"
        
        versions = generate_news_content(text_input)
        
        if versions is None:
            return jsonify({"error": "Failed to generate news content"}), 500

        return jsonify({
            "caption1": versions[0],
            "caption2": versions[1],
            "caption3": versions[2]
        })
    
    except Exception as e:
        print(f"Error in generate_news_content: {str(e)}")
        return jsonify({"error": str(e)}), 500

def generate_news_content(prompt):
    base_instruction = """
    Generate 3 different versions of formal news content in English. For each version:
    1. Start with a CAPITALIZED, bold headline using HTML <strong> tags
    2. Follow with a 50-70 word news content (unless input is shorter or cannot be expanded)
    3. Write in a formal, unbiased tone
    4. Be informative without glorifying or undermining
    5. Don't include any sales language or hashtags
    6. Focus on facts and clear information
    7. Format: 
       <strong>HEADLINE HERE</strong>
       
       News content here...

    Separate versions with "---"
    """
    
    try:
        response = model.generate_content(
            f"{base_instruction}\n\nNews content to rewrite: {prompt}"
        )
        
        content = response.text.strip()
        versions = [v.strip() for v in content.split('---')]
        
        while len(versions) < 3:
            versions.append("Content generation incomplete. Please try again.")
        
        return versions[:3]
    
    except Exception as e:
        print(f"Error generating news content: {str(e)}")
        return None

def generate_branded_caption(prompt, style):
    style_guides = {
        "default": "Identity Magazine's signature style: professional yet approachable, informative with a touch of sophistication",
        "professional": "Formal and business-oriented tone, focusing on expertise and authority",
        "casual": "Fun, friendly, and conversational tone with emojis and casual language",
        "motivational": "Inspiring and encouraging tone with powerful calls to action",
        "minimal": "Concise and clean with essential information only",
        "storytelling": "Narrative-driven with engaging story elements",
        "luxury": "Elegant, sophisticated tone with emphasis on exclusivity and premium quality"
    }

    base_instruction = """
    Generate 3 different branded content versions. For each version:
    1. Include ALL points mentioned in the brief
    2. Format the content with proper styling:
       - Use <strong> for emphasis on important points
       - Use line breaks for better readability
       - Place all hashtags at the end, separated from the main content by two line breaks
    3. Use ONLY the hashtags provided in the brief (don't create new ones)
    4. Minimum length of 80 words for the main content (excluding hashtags)
    5. Maintain the style selected while covering all brief points
    6. Format:
       Main content with <strong>emphasized points</strong>...
       
       
       #hashtag1 #hashtag2 #hashtag3

    Separate versions with "---"
    """
    
    try:
        response = model.generate_content(
            f"{base_instruction}\n\nStyle: {style_guides.get(style, style_guides['default'])}\n\nBrief: {prompt}"
        )
        
        content = response.text.strip()
        versions = [v.strip() for v in content.split('---')]
        
        while len(versions) < 3:
            versions.append("Content generation incomplete. Please try again.")
        
        return versions[:3]
    
    except Exception as e:
        print(f"Error generating branded caption: {str(e)}")
        return None

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            # Read the file content based on file type
            if file.filename.endswith('.txt'):
                content = file.read().decode('utf-8')
            elif file.filename.endswith('.pdf'):
                # Add PDF processing here
                from PyPDF2 import PdfReader
                reader = PdfReader(file)
                content = ""
                for page in reader.pages:
                    content += page.extract_text()
            elif file.filename.endswith('.docx'):
                # Add DOCX processing here
                import docx
                doc = docx.Document(file)
                content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            else:
                return jsonify({'error': 'Unsupported file type'}), 400
                
            return jsonify({'text_content': content}), 200
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
