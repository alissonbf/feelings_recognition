from flask import Flask, render_template, request
from Classes import GCloudStorage, Vision

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        gstorage = GCloudStorage(bucket_name='abftecnologia.appspot.com', project_name='abftecnologia')
        gstorage.upload_file(file_name=request.files.get('image').filename, file_stream=request.files.get('image'))
        image_url = gstorage.blob.media_link
        vision = Vision(image_uri=image_url)
        emoticon = vision.feeling_emoticon
    else:
        image_url = None
        emoticon = None
    return render_template("index.html", image_url=image_url, emoticon=emoticon)
