from flask import Flask, jsonify, request, render_template, redirect, make_response
from werkzeug.exceptions import RequestTimeout
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import json

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@linkas/songs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

url = 'http://url:5000/api/vehicles'

class Songs(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.Date, nullable=False, default='N/A')
    link = db.Column(db.String(500))
    origin = db.Column(db.String(50), nullable=False)

    def __init__(self, artist, name, date_created, link, origin):
        self.artist = artist
        self.name = name
        self.date_created = date_created
        self.link = link
        self.origin = origin

    def __repr__(self):
        return 'id {}'.format(self.id)


@app.route('/songs', methods=['GET'])
def get_all():
    songs = Songs.query.all()
    output = []

    for song in songs:
        tanks = []
        currSong = {}
        currSong['id'] = song.id
        currSong['artist'] = song.artist
        currSong['name'] = song.name
        currSong['date_created'] = song.date_created
        currSong['link'] = song.link

        try:
            response = requests.get(url)
            data = json.loads(response.text)
            for dat in data:
                if dat["origin"] == song.origin:
                    tanks.append(dat)
        
        except requests.ConnectionError:
            pass

        currSong['tanks'] = tanks
        output.append(currSong)

    return jsonify(output)


@app.route('/songs/<song_id>', methods=['GET'])
def get_song(song_id):
    song = Songs.query.get_or_404(song_id)

    output = []
    tanks = []
    currSong = {}
    currSong['id'] = song.id
    currSong['artist'] = song.artist
    currSong['name'] = song.name
    currSong['date_created'] = song.date_created
    currSong['link'] = song.link

    try:
        response = requests.get(url)
        data = json.loads(response.text)
        for dat in data:
            if dat["origin"] == song.origin:
                tanks.append(dat)
        
    except requests.ConnectionError:
        pass

    currSong['tanks'] = tanks
    output.append(currSong)


    return jsonify(output)



@app.route('/songs', methods=['POST'])
def add_song():
    songData = request.get_json()

    date = datetime.strptime(songData['date_created'], "%Y-%m-%d")
    song = Songs(artist=songData['artist'], name=songData['name'], date_created=date, link=songData['link'], origin=songData['origin'])
    db.session.add(song)
    db.session.commit()

    
    try:
        tanks = songData['tanks']
        for tank in tanks:
            response = requests.post(url, json = tank)

    except requests.ConnectionError:
        resp = make_response()
        resp.status_code = 503
        return resp


    resp = make_response()
    resp = jsonify(songData)
    resp.status_code = 201
    resp.headers['Content-Location'] = f'http://localhost:5000/songs/{song.id}'
    return resp




@app.route('/songs/<song_id>', methods=['DELETE'])
def delete_song(song_id):
    song = Songs.query.get_or_404(song_id)
    output = []
    currSong = {}
    currSong['id'] = song.id
    currSong['artist'] = song.artist
    currSong['name'] = song.name
    currSong['date_created'] = song.date_created
    currSong['link'] = song.link
    output.append(currSong)


    try:
        response = requests.get(url)
        data = json.loads(response.text)

        for dat in data:
            if dat["origin"] == song.origin:
                response = requests.delete(url + "/" + str(dat["id"]))

    except requests.ConnectionError:
        pass

    db.session.delete(song)
    db.session.commit()

    return jsonify(output)



@app.route('/songs/<song_id>', methods=['PUT'])
def edit_song(song_id):
    song = Songs.query.get_or_404(song_id)
    songData = request.get_json()
    song.artist = songData['artist']
    song.name = songData['name']
    song.date_created = datetime.strptime(songData['date_created'], "%Y-%m-%d")
    song.link = songData['link']
    db.session.commit()
    output = []
    currSong = {}
    currSong['id'] = song.id
    currSong['artist'] = song.artist
    currSong['name'] = song.name
    currSong['date_created'] = song.date_created
    currSong['link'] = song.link

  
    tanks = songData['tanks']
    for tank in tanks:
        _tank = {}
        _tank["model"] = tank["model"]
        _tank["year"] = tank["year"]
        _tank["origin"] = tank["origin"]
        requests.put(url + '/' + str(tank["id"]), json = _tank)



    response = requests.get(url)
    data = json.loads(response.text)


    currSong['tanks'] = tanks

    output.append(currSong)
    return jsonify(output)




###############################################################################################################
# F R O N T   E N D

@app.route('/')
def index():
    songs = Songs.query.all()
    return render_template('index.html', songs=songs)

@app.route('/tanks/<int:id>', methods=['GET'])
def tanks(id):
    song = Songs.query.get_or_404(id)

    response = requests.get(url)
    data = json.loads(response.text)

    tanks = []

    for dat in data:
        if dat["origin"] == song.origin:
            tanks.append(dat)

    return render_template('tanks.html', tanks=tanks)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        artist = request.form["artist"]
        name = request.form["name"]
        date = datetime.strptime (request.form["date"], "%Y-%m-%d")
        link = request.form["link"]
        data = Songs(artist=artist, name=name, date_created=date, link=link)
        db.session.add(data)
        db.session.commit()
        return redirect("/")
    else:
        return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    song = Songs.query.get_or_404(id)
    if request.method == 'POST':
        song.artist = request.form["artist"]
        song.name = request.form["name"]
        song.date_created = datetime.strptime (request.form["date"], "%Y-%m-%d")
        song.link = request.form["link"]
        db.session.commit()
        return redirect("/")
    else:
        return render_template('edit.html', song=song)

@app.route('/delete/<int:id>')
def delete(id):
    song = Songs.query.get_or_404(id)
    db.session.delete(song)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
