import os
from datetime import datetime

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.utils import secure_filename

import crop
from tpot_regression_model import predict_from_image

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "temp"
app.config["CROPPED_FOLDER"] = "cropped"
app.config["MASKED_FOLDER"] = "masked"


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


@app.route("/masked/<filename>")
def serve_masked_image(filename):
    return send_from_directory(app.config["MASKED_FOLDER"], filename)


@app.route("/delete/<filename>", methods=["POST"])
def delete_files(filename):
    try:
        # Define file paths
        cropped_file = os.path.join(app.config["CROPPED_FOLDER"], filename)
        masked_file = os.path.join(app.config["MASKED_FOLDER"], f"masked-{filename}")
        annotation_file = os.path.join("annotation", f"{os.path.splitext(filename)[0]}.txt")

        # Delete files if they exist
        if os.path.exists(cropped_file):
            os.remove(cropped_file)
        if os.path.exists(masked_file):
            os.remove(masked_file)
        if os.path.exists(annotation_file):
            os.remove(annotation_file)

        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/predict/<filename>")
def predict(filename):
    input_image = os.path.join(app.config["CROPPED_FOLDER"], filename)
    prediction = predict_from_image(input_image)
    formatted_date = get_formatted_date(filename)
    
    # Construct the masked image filename
    masked_filename = f"masked-{filename}"
    masked_image_url = url_for("serve_masked_image", filename=masked_filename)

    return render_template(
        "predict.html",
        image_url=url_for("serve_cropped_image", filename=filename),
        masked_image_url=masked_image_url,
        prediction=prediction,
        formatted_date=formatted_date,
        filename=filename
    )


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
    if not os.path.exists(app.config["MASKED_FOLDER"]):
        os.makedirs(app.config["MASKED_FOLDER"])
    app.run(debug=True, host="0.0.0.0")
