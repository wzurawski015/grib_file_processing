#!/usr/bin/env python
# Ścieżka: flask_app/app.py

from flask import Flask, render_template, send_from_directory
import os
import yaml

# Wczytaj konfigurację
with open('/app/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', config=config)

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(config['paths']['image_folder'], filename)

@app.route('/load-image/<int:index>')
def load_image(index):
    images = sorted([f for f in os.listdir(config['paths']['image_folder']) if f.endswith('.png')])
    if index >= len(images):
        index = 0
    image = images[index]
    return f'<img src="/images/{image}" alt="Heatmap">', 200

if __name__ == '__main__':
    app.run(debug=True)
