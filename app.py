from flask import Flask, render_template, request
import fitz
import os

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "resume" not in request.files:
        return "Please upload a resume"

    file = request.files["resume"]

    if not file.filename.lower().endswith(".pdf"):
        return "Only PDF files are allowed"

    if file.filename == "":
        return "No file selected"

    try:
        pdf = fitz.open(stream=file.read(), filetype="pdf")

        resume_text = "\n".join(
            page.get_text() for page in pdf
        )

        pdf.close()

        if not resume_text.strip():
            return "No readable text found in PDF"

        return render_template(
            "result.html",
            resume_text=resume_text[:5000]
        )

    except Exception:
        return "Unable to read this PDF"

if __name__ == "__main__":
    app.run(debug=True)