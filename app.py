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

@app.route('/delete_unassigned_images', methods=['POST'])
def delete_unassigned_images():
    data = request.get_json()
    hashes = data.get('hashes', [])

    deleted_files = []
    errors = []

    for hash_name in hashes:
        filename = f"{hash_name}.png"
        file_path = os.path.join(IMAGES_DIR, filename)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                deleted_files.append(filename)
            else:
                errors.append(f"{filename} existiert nicht.")
        except Exception as e:
            errors.append(f"Fehler beim Löschen von {filename}: {str(e)}")

    if errors:
        return jsonify({'status': 'error', 'errors': errors})
    else:
        return jsonify({'status': 'success', 'deleted_files': deleted_files})

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')
