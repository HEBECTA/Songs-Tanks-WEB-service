from flask import Flask, jsonify, request, render_template, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import json

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/songs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

url = 'http://localhost:5002/api/vehicles'

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
    tanks = []
    i = 0
    for song in songs:
        currSong = {}
        currSong['id'] = song.id
        currSong['artist'] = song.artist
        currSong['name'] = song.name
        currSong['date_created'] = song.date_created
        currSong['link'] = song.link
        

        #temp_url = url + "/" + str(i)

        response = requests.get(url)

        print(response)

        tanks.append(response.json())
        currSong['tanks'] = tanks
   
        output.append(currSong)

        #output.append(response.json())

        i += 1
        
    return jsonify(output)

# curl http://localhost:5000/songs -X GET

@app.route('/songs/<song_id>', methods=['GET'])
def get_song(song_id):
    song = Songs.query.get_or_404(song_id)
    output = []
    currSong = {}
    currSong['id'] = song.id
    currSong['artist'] = song.artist
    currSong['name'] = song.name
    currSong['date_created'] = song.date_created
    currSong['link'] = song.link
    output.append(currSong)

    #temp_url = url + "/" + str(song_id-1)
    #response = requests.get(temp_url)
    #output.append(response.json())

    return jsonify(output)

# curl http://localhost:5000/songs/1 -X GET

@app.route('/songs', methods=['POST'])
def add_song():
    songData = request.get_json()
    date = datetime.strptime(songData['date_created'], "%Y-%m-%d")
    song = Songs(artist=songData['artist'], name=songData['name'], date_created=date, link=songData['link'], origin=songData['origin'])
    db.session.add(song)
    db.session.commit()



    #tank = {
    #    "model": songData["model"],
    #    "year": songData["year"],
    #    "origin": songData["origin"]
    #}

    #response = requests.post(url, data=tank)


    resp = make_response()
    resp = jsonify(songData)
    resp.status_code = 201
    resp.headers['Content-Location'] = f'http://localhost:5000/songs/{song.id}'
    return resp

# curl http://localhost:5000/songs -d '{"name":"daina", "artist":"muzikantas", "date_created":"2018-02-03", "link":"www.google.com"}' -H "Content-Type: application/json" -X POST


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

    #temp_url = url + "/" + str(song_id-1)
    #response = requests.get(temp_url)


    db.session.delete(song)
    db.session.commit()

    return jsonify(output)

# curl http://localhost:5000/songs/12 -X DELETE

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
    output.append(currSong)
    return jsonify(output)

# curl http://localhost:5000/songs/12 -d '{"name":"daina2", "artist":"muzikantas2", "date_created":"2018-02-03", "link":"www.google.com"}' -H "Content-Type: application/json" -X PUT


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
        #print("DATA ATSPAUSDINTA")
        #print(request.form["date"])
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
