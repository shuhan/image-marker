#!/usr/bin/env python3
import os
import json
from flask import Flask, request, Markup, render_template, url_for, jsonify

app         = Flask(__name__)
types       = { 'Obstacle' : False, 'MR.York' : False, 'Vehicle' : False, 'Wall' : False, 'RescueVehicle': False, 'Floor' : True }
image_dir   = 'static/flight_capture'
result_dir  = 'static/marked'

def get_first_image():

    filelist = os.listdir(image_dir)
    for fichier in filelist[:]: # filelist[:] makes a copy of filelist.
        if not(fichier.endswith(".png")):
            filelist.remove(fichier)
    
    if len(filelist) == 0:
        return None

    file_path = 'flight_capture/' + filelist[0]

    return file_path


@app.route("/", methods=['GET'])
def index():
    file_path = get_first_image()

    if file_path is None:
        return render_template('marking_complete.html')

    return render_template('index.html', image_url=url_for('static', filename=file_path), karnel_size=60, types=types)

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    content = request.json
    if content is None or 'url' not in content.keys():
        print("Invalid request")
        return jsonify({ 'success' : False, 'message' : 'Invalid request' })

    filename = os.path.basename(content['url'])
    content['url'] = filename

    if not os.path.isdir(result_dir):
        os.makedirs(os.path.join(app.root_path, result_dir))

    image_path  = os.path.join(app.root_path, image_dir, filename)
    move_to     = os.path.join(app.root_path, result_dir, filename)
    data_path   = os.path.join(app.root_path, result_dir, os.path.splitext(filename)[0] + '.json')

    if not os.path.exists(image_path) or not os.path.isfile(image_path):
        return jsonify({ 'success' : False, 'message' : 'File is already processed or invalid' })

    os.rename(image_path, move_to)
    datafile = open(data_path, "w")
    datafile.write(json.dumps(content))
    datafile.close()

    file_path = get_first_image()

    if file_path is None:
        image_url = ''
    else:
        image_url = url_for('static', filename=file_path)

    return jsonify({ 'success' : True, 'message' : 'Image stored', 'image_url' : image_url })