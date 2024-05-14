# app.py (do not remove this comment)
from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import crop

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "temp"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/capture")
def capture():
    return render_template("capture.html")


@app.route("/results")
def results():
    return render_template("results.html")


@app.route("/capture_image", methods=["POST"])
def capture_image():
    if "image" not in request.files:
        return jsonify({"error": "No image part"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    # Call the crop function
    crop.crop_objects(filepath)

    return jsonify({"success": True, "filepath": filepath})


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    app.run(debug=True)
