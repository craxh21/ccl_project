import os, datetime
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import boto3
from utils import calculate_md5

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
db = client.file_uploads
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

@app.route('/')
def home():
    return "Flask app is running!"

@app.route("/upload-form")
def upload_form():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files['file']
    file_data = file.read()
    checksum = calculate_md5(file_data)

    existing = db.files.find_one({"checksum": checksum})
    if existing:
        db.files.update_one(
            {"_id": existing["_id"]},
            {"$set": {"last_uploaded": datetime.datetime.now()}}
        )
        return jsonify({"status": "duplicate", "message": "File already exists"})

    # Upload to S3
    s3.upload_fileobj(request.files['file'], os.getenv("S3_BUCKET_NAME"), file.filename)

    db.files.insert_one({
        "filename": file.filename,
        "checksum": checksum,
        "size": len(file_data),
        "extension": file.filename.split('.')[-1],
        "timestamp": datetime.datetime.now()
    })

    return jsonify({"status": "success", "message": "File uploaded"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)

