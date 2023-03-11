from io import BytesIO
import os
from flask import Flask, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
import requests

app = Flask(__name__)

URL = 'https://dry-ocean-81907.herokuapp.com/'
S3_URL = 'https://image-api-bucket2.s3.amazonaws.com'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        file.filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        files = [('file', (file.file.filename, open(filepath, 'rb'), 'image/jpeg'))]
        response = requsets.post(url=URL+'/images', files=files)
        image_name = response.json()['filename']
        return redirect(f'/image/{image_name}')
    response = requests.get(url=URL+'/images')
    images = response.json()['data']
    return render_template('index.jinja', S3_URL=S3_URL, images=images)

@app.route('/image/<image_name>')
def image(image_name):
    return render_template('image.jinja', image_name = image_name)

@app.route('/resize', methods=['POST'])
def resize():
    if request.method == 'POST':
        date ={'filename': request.form['filename'], 'width': request.form['width'], 'height': request.form['height']}
        response = request.post(url=URL+'/actions/resize', json=data, headers={'Content-Type': 'application/json'})
        return send_file(BytesIO(response.content), mimetype='image/jpeg', as_attachment=True, download_name=f'resized_{request.form["filename"]}')
