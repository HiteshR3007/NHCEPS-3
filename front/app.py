import os
#import cv2
import pytesseract
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

# Config
UPLOAD_FOLDER = 'uploads'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# App setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Preprocessing function
def preprocess_image(path):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(gray)
    resized = cv2.resize(inverted, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    thresh = cv2.threshold(resized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh

# OCR function
def ocr_core(image_path):
    preprocessed = preprocess_image(image_path)
    text = pytesseract.image_to_string(preprocessed, config='--oem 3 --psm 6')
    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            text = ocr_core(file_path)
            return render_template('front.html', ocr_text=text)

    return render_template('front.html', ocr_text=None)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('image')
        if file and file.filename:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            text = "fake OCR result"  # replace with actual OCR
            return render_template('front.html', ocr_text=text)
    return render_template('front.html', ocr_text=None)

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)