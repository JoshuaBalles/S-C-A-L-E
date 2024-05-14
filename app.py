# app.py (do not remove this comment)
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
import crop

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "temp"
app.config["CROPPED_FOLDER"] = "cropped"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/capture")
def capture():
    return render_template("capture.html")


@app.route("/results")
def results():
    image_files = [
        f for f in os.listdir(app.config["CROPPED_FOLDER"]) if f.endswith(".jpg")
    ]
    image_urls = [image_file for image_file in image_files]
    return render_template("results.html", image_urls=image_urls)


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


@app.route("/cropped/<filename>")
def serve_cropped_image(filename):
    return send_from_directory(app.config["CROPPED_FOLDER"], filename)


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    if not os.path.exists(app.config["CROPPED_FOLDER"]):
        os.makedirs(app.config["CROPPED_FOLDER"])
    app.run(debug=True)
