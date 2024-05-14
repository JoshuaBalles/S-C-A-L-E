# app.py (do not change/remove this comment)
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
import crop
from datetime import datetime

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
    return render_template(
        "results.html", image_urls=image_urls, get_formatted_date=get_formatted_date
    )


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

    try:
        # Call the crop function
        crop.crop_objects(filepath)
        return jsonify({"success": True, "filepath": filepath})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/cropped/<filename>")
def serve_cropped_image(filename):
    return send_from_directory(app.config["CROPPED_FOLDER"], filename)


def get_formatted_date(image_url):
    parts = image_url.split("_")
    date_string = parts[0] + " " + parts[1]
    date_string = date_string[:-6]
    date_object = datetime.strptime(date_string, "%Y-%m-%d %H-%M-%S")
    formatted_date = date_object.strftime("%B %d, %Y, %I:%M%p")
    return formatted_date


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    if not os.path.exists(app.config["CROPPED_FOLDER"]):
        os.makedirs(app.config["CROPPED_FOLDER"])
    app.run(debug=True)
