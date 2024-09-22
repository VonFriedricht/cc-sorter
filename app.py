from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# Pfade und Dateien
CHESTS_FILE = 'chests.json'
IMAGES_DIR = os.path.join('static', 'images')

# Beispielwerte für chests, falls die Datei nicht existiert
EXAMPLE_CHESTS = [[] for _ in range(30)]  # 30 leere Kisten

@app.route('/')
def index():
    # Erstelle chests.json mit Beispielwerten, falls nicht vorhanden
    if not os.path.exists(CHESTS_FILE):
        with open(CHESTS_FILE, 'w') as f:
            json.dump(EXAMPLE_CHESTS, f)

    # Lade das chests-Array
    with open(CHESTS_FILE, 'r') as f:
        chests = json.load(f)

    # Erhalte alle zugewiesenen Hashes
    assigned_hashes = set()
    for chest in chests:
        assigned_hashes.update(chest)

    # Finde alle Bilder im Images-Verzeichnis
    all_images = set()
    for filename in os.listdir(IMAGES_DIR):
        if filename.endswith('.png'):
            hash_name = filename[:-4]
            all_images.add(hash_name)

    # Bestimme die unzugeordneten Items
    unassigned_items = list(all_images - assigned_hashes)

    return render_template('index.html', chests=chests, unassigned_items=unassigned_items)

@app.route('/save_chests', methods=['POST'])
def save_chests():
    data = request.get_json()
    with open(CHESTS_FILE, 'w') as f:
        json.dump(data['chests'], f)
    return jsonify({'status': 'success'})

@app.route('/static/images/<path:filename>')
def custom_static(filename):
    return send_from_directory(IMAGES_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
