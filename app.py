# app.py
from flask import Flask, render_template, request, jsonify
import os
from color_extractor import extract_colors

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')

# app.py - Updated /extract route


@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        hex_colors, rgb_colors = extract_colors(filepath)

        # 🔁 Convert np.int32 to Python int
        colors = []
        for hex_val, rgb_tuple in zip(hex_colors, rgb_colors):
            rgb_list = [int(val) for val in rgb_tuple]  # ← This fixes it!
            colors.append({"hex": hex_val, "rgb": rgb_list})

        return jsonify({
            "image_url": filepath.replace("\\", "/"),
            "colors": colors
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
