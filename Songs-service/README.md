# Songs-service

// Sukurti image "songs-image" <br>
docker build -t songs-image . <br>

// Paleisti image "songs-image" per porta 5000, (sukuria container "songs-container") <br>
docker run --name songs-container -p 5000:5000 songs-image <br>

// Pakartotinai paleisti container "songs-container" <br>
docker start songs-container <br>

Restful serviso adresas localhost:5000/songs <br>

Front end adresas localhost:5000 <br>

Serviso aptarnaujami resursai - songs. <br>

SONG DATA STRUCTURE: <br>
{ <br>
  "id" : "\<unique identification number\>", <br>
  "artist" : "\<artist name\>", <br>
  "name" : "\<song name\>", <br>
  "date_created" : "\<release date\>", <br>
  "link" : "\<youtube url\>" <br>
}<br>

RESTFUL API: <br>

(curl - command-line tool for transferring data using various network protocols) <br>

(READ ALL) <br>
GET http://localhost:5000/songs <br>
pvz: curl http://localhost:5000/songs -X GET <br>

(READ) <br>
GET http://localhost:5000/songs/<songs_id> <br>
pvz: curl http://localhost:5000/songs/1 -X GET <br>

(ADD) <br>
POST http://localhost:5000/songs <br>
pvz: curl http://localhost:5000/songs -d '{"name":"daina", "artist":"muzikantas", "date_created":"2018-02-03", "link":"https://www.google.com"}' -H "Content-Type: application/json" -X POST <br>

(REMOVE) <br>
DELETE http://localhost:5000/songs/<songs_id> <br>
pvz: curl http://localhost:5000/songs/12 -X DELETE <br>

(UPDATE) <br>
PUT http://localhost:5000/songs/<songs_id> <br>
curl http://localhost:5000/songs/<12> -d '{"name":"daina2", "artist":"muzikantas2", "date_created":"2018-02-03", "link":"https://www.google.com"}' -H "Content-Type: application/json" -X PUT
