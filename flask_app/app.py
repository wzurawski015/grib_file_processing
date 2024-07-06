"""
Ścieżka: /home/wz/grib_file_processing/flask_app/app.py
"""

from flask import Flask, render_template, send_from_directory, abort
import os
import yaml

app = Flask(__name__)

# Wczytanie konfiguracji z pliku config.yaml
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Konfiguracja ścieżki do katalogu z obrazami
image_folder = os.path.abspath(os.path.join(os.path.dirname(config_path), config['target_directory']))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load-image/<int:index>')
def load_image(index):
    try:
        images = sorted([img for img in os.listdir(image_folder) if img.endswith('.png')])
        if not images:
            return "No images found in the directory.", 404
        if index >= len(images):
            index = 0
        image_name = images[index]
        return render_template('image.html', image_name=image_name, next_index=index + 1)
    except Exception as e:
        app.logger.error(f"Error loading images: {e}")
        return str(e), 500

@app.route('/images/<image_name>')
def images(image_name):
    try:
        return send_from_directory(image_folder, image_name)
    except FileNotFoundError:
        abort(404, description=f"File {image_name} not found.")

if __name__ == '__main__':
    app.run(debug=True)
