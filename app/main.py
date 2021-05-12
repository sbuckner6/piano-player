from flask import Flask, render_template, Response, url_for, send_file, send_from_directory
from music.compose import compose_midi
from audio.audio import render_audio
from random import randint
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/audio')
def audio():
    r = randint(1, 100)
    midi_file = f"/build/app/out{r}.mid"
    compose_midi(midi_file)
    mp3_file = f"/build/app/out{r}.mp3"
    render_audio(midi_file, mp3_file)
    return send_file(mp3_file, mimetype='audio/mpeg')


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == '__main__':
    app.run()