from flask import Flask, render_template, request
from PIL import Image
import base64
import io
import numpy as np
import easyocr

def preprocess_image(image):
    # Convert to grayscale
    image = image.convert('L')
    return image

def recognize_text(image):
    reader = easyocr.Reader(['en'])
    # Convert PIL Image to numpy array
    image_np = np.array(image)
    results = reader.readtext(image_np)
    return results

app = Flask(__name__)

@app.template_filter('b64encode')
def base64_encode(image):
    buffered = io.BytesIO()
    image.save(buffered, format='PNG')
    base64_data = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return base64_data

@app.route('/', methods=['GET', 'POST'])
def index1():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_type = file.filename.split('.')[-1]
            if file_type == 'pdf':
                return render_template('index.html', error_message='Invalid file type. Please select a JPG, or PNG file.')


            elif file_type in ['jpg', 'jpeg', 'png']:
                image = Image.open(file)
                processed_image = preprocess_image(image)
                # Use EasyOCR to recognize text in the image
                results = recognize_text(processed_image)
                image_list = [image]
                text_list = [results]
            else:
                return render_template('index1.html', error_message='Invalid file type. Please select a PDF, JPG, or PNG file.')

            return render_template('index1.html', image_list=image_list, text_list=text_list)

    return render_template('index1.html')

if __name__ == "__main__":
    app.run(debug=True)
