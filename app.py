from flask import Flask, render_template, request, jsonify
from corrector import correct_with_textblob, correct_with_symspell
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    corrected_output = ""
    if request.method == "POST":
        input_text = request.form.get("text", "")
        method = request.form.get("method")

        if "file" in request.files:
            file = request.files["file"]
            if file.filename.endswith(".txt"):
                filepath = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(filepath)
                with open(filepath, "r", encoding="utf-8") as f:
                    input_text = f.read()

        if method == "textblob":
            corrected_output = correct_with_textblob(input_text)
        elif method == "symspell":
            corrected_output = correct_with_symspell(input_text)

    return render_template("index.html", corrected=corrected_output)


# ✅ LIVE Correction via JS AJAX call
@app.route("/live-correct", methods=["POST"])
def live_correct():
    data = request.get_json()
    text = data.get("text", "")
    method = data.get("method", "textblob")

    if method == "textblob":
        corrected = correct_with_textblob(text)
    else:
        corrected = correct_with_symspell(text)

    return jsonify({"corrected": corrected})


if __name__ == "__main__":
    app.run(debug=True)
