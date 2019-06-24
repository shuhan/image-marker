#!/usr/bin/env python3
from flask import Flask, request, Markup, render_template, url_for

app = Flask(__name__)

@app.route("/")
def index():
    types = { 'Obstacle' : False, 'MR.York' : False, 'Vehicle' : False, 'Wall' : False, 'RescueVehicle': False, 'Floor' : True }
    return render_template('index.html', image_url=url_for('static', filename='flight_capture/2019-06-21 19:16:12.png'), karnel_size=60, types=types)