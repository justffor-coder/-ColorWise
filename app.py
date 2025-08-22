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


@app.route('/extract', methods=['POST'])
def extract():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    try:
        hex_colors, rgb_colors = extract_colors(filepath)

        # ✅ Convert np.int32 to Python int
        palette = []
        for hex_val, rgb in zip(hex_colors, rgb_colors):
            rgb_clean = [int(c) for c in rgb]
            palette.append({"hex": hex_val, "rgb": rgb_clean})

        return jsonify({
            "image_url": filepath.replace("\\", "/"),
            "colors": palette
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # ✅ Render requires binding to PORT and 0.0.0.0
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
