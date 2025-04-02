import os
from flask import Flask, render_template, request, send_file
from converter import docx_to_pdf


app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["CONVERTED_FOLDER"] = CONVERTED_FOLDER

# Erstelle den Upload Folder, falls er nicht existiert

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "Keine Datei hochgeladen", 400
    
    file = request.files["file"]

    if file.filename == "":
        return "Keine Datei ausgewählt", 400
    
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    if file.filename.endswith(".docx"):
        pdf_path = os.path.join(app.config["CONVERTED_FOLDER"], file.filename.replace(".docx",".pdf"))
        docx_to_pdf(file_path, pdf_path)
        return send_file(pdf_path, as_attachment=True)


    return f"Datei erfolgreich gespeichert: {file_path}"



if __name__ == "__main__":
    app.run(debug=True)