from flask import Flask, render_template, request, redirect, url_for

app = Flask("crtblaster")

@app.route('/')
@app.route('/index')
def index():
    return render_template('./index.html')

@app.route('/upload/video', methods=['POST'])
def upload_file():
    print(request)
    print(f"video name is {request.form['videoname']}")
    print(request.files['video'])
    request.files['video'].save(f"../data/new_videos/{request.form['videoname']}.mp4")
    return ""
