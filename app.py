from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import ollama
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = './uploads'

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    # Ensure the upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the uploaded image
    image_path = os.path.join(UPLOAD_FOLDER, 'uploaded_image.jpg')
    file.save(image_path)

    # Get the response from the model
    try:
        res = ollama.chat(
            model="llava",
            messages=[
                {
                    "role": "user",
                    "content": "write down just ingredients without explanation that are clearly shown in the image",
                    "images": [image_path],
                }
            ],
        )
        # Extract and clean the response content
        response_content = res["message"]["content"]
        
        # Assuming response content is a string with the ingredients
        ingredients = extract_ingredients(response_content)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Clean up files
    os.remove(image_path)

    return jsonify({'ingredients': ingredients})

def extract_ingredients(response_content):
    # Process the response content to extract only the ingredients
    # This is a placeholder function. You need to customize this based on the actual format of the response.
    lines = response_content.split('\n')
    ingredients = [line for line in lines if line.strip() and line[0].isdigit()]  # Example filter
    return ingredients

if __name__ == '__main__':
    app.run(port=5000)
