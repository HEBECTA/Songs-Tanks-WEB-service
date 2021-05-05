from flask import Flask, jsonify, request, render_template, redirect
import psycopg2
from datetime import datetime
import requests

conn = psycopg2.connect("dbname=postgres user=postgres password=postgres host=localhost")

cur = conn.cursor()

cur.execute("CREATE TABLE [IF NOT EXISTS] Songs( \
    id serial PRIMARY KEY,\
    artist VARCHAR (50),\
    name VARCHAR (50), \
    date_created  date, \
    link VARCHAR (500)\
    );")

cur.execute("INSERT INTO Songs(artist, name, date, link) \
    VALUES('Alexander Alexandrov', \
    'Государственный гимн СССР', \
    '1939-01-08', \
    'https://www.youtube.com/watch?v=_sxTbfeYdO0'\
    );")


app = Flask(__name__)

url = 'http://localhost:5000/api/vehicles'


@app.route('/songs', methods=['GET'])
def get_all():
    
    output = []

    try:

        cur.execute("SELECT * FROM Songs;")
        data = cur.fetchall()

    except psycopg2.Error as e:

        t_message = "Database error: " + e + "/n SQL: " + s
        print(t_message)
        return render_template('add.html')
        
    for i in range(len(data)):
        print(data[i])
        output.append(data[i])

    return jsonify(output)

# curl http://localhost:5000/songs -X GET

@app.route('/songs/<song_id>', methods=['GET'])
def get_song(song_id):
    
    output = []
    

    return jsonify(output)

# curl http://localhost:5000/songs/1 -X GET

@app.route('/songs', methods=['POST'])
def add_song():
    


    resp = make_response()
   
    resp.status_code = 201
   
    return resp

# curl http://localhost:5000/songs -d '{"name":"daina", "artist":"muzikantas", "date_created":"2018-02-03", "link":"www.google.com"}' -H "Content-Type: application/json" -X POST


@app.route('/songs/<song_id>', methods=['DELETE'])
def delete_song(song_id):
  
    output = []
    

    return jsonify(output)

# curl http://localhost:5000/songs/12 -X DELETE

@app.route('/songs/<song_id>', methods=['PUT'])
def edit_song(song_id):
   
    output = []
    
    output.append(currSong)
    return jsonify(output)

# curl http://localhost:5000/songs/12 -d '{"name":"daina2", "artist":"muzikantas2", "date_created":"2018-02-03", "link":"www.google.com"}' -H "Content-Type: application/json" -X PUT


###############################################################################################################
# F R O N T   E N D

@app.route('/')
def index():
  
    return render_template('add.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        
        return render_template('add.html')
    else:
        return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    
    if request.method == 'POST':
       
        return render_template('add.html')
    else:
        return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
   
    return render_template('add.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
