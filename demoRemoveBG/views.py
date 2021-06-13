"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,send_file,send_from_directory, request
from demoRemoveBG import app
from rembg.bg import remove
import numpy as np
import io
import os
from PIL import ImageFile, Image
ImageFile.LOAD_TRUNCATED_IMAGES = True
# Create a directory in a known location to save files to.
uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir,mode=0, exist_ok=True)
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/upload', methods=['POST'])
def upload():
    imagefile = request.files['imagefile']
    f = imagefile.read()
    #    print(f)
    npimg = np.fromstring(f,np.uint8)
    removeBG(npimg)
    return send_from_directory(directory=os.path.join(uploads_dir, ''), path='output.png')
    
def removeBG(data):
    result = remove(data)
    img = Image.open(io.BytesIO(result)).convert("RGBA")
    img.save(os.path.join(uploads_dir, 'output.png'))
@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
