# Songs-Tanks-WEBservice

// Paleidimas" <br>
docker-compose up<br>

// Isjungimas <br>
docker-compose down<br>

Dainos yra himnai, kiekvienas himnas turi origin - sali. Kiekvienas himnas turi tanku masyva, kurie buvo pagaminti himno salyje.

Songs serviso adresas localhost:5001/songs <br>

Front end Songs serviso adresas localhost:5001 <br>

Tanks serviso adresas http://localhost:5002/api/vehicles

Songs serviso aptarnaujami resursai. <br>

SONG DATA STRUCTURE: <br>
{ <br>
  "id" : "\<unique identification number\>", <br>
  "artist" : "\<artist name\>", <br>
  "name" : "\<song name\>", <br>
  "date_created" : "\<release date\>", <br>
  "link" : "\<youtube url\>" <br>
  "origin" : "\<country\>" <br>
}<br>

Tanks serviso aptarnaujami resursai. <br>

TANK DATA STRUCTURE: <br>
{ <br>
  "id" : "\<unique identification number\>", <br>
  "name" : "\<tank name\>", <br>
  "year" : "\<release date\>", <br>
  "origin" : "\<country\>", <br>
}<br>

RESTFUL API: <br>

(curl - command-line tool for transferring data using various network protocols) <br>

SONGS <br>

(READ ALL) <br>
GET http://localhost:5001/songs <br>
pvz: curl http://localhost:5001/songs -X GET <br>

(READ) <br>
GET http://localhost:5001/songs/<songs_id> <br>
pvz: curl http://localhost:5001/songs/1 -X GET <br>

(ADD) <br>
POST http://localhost:5001/songs <br>
pvz: curl http://localhost:5001/songs -d '{"name":"The Star-Spangled Banner", "artist":"John Stafford Smith", "date_created":"1773-02-03", "link":"https://www.youtube.com/watch?v=cP5---17O4s", "origin":"USA", "tanks":[{"model":"KV-2", "year":1943, "origin":"USA"}, {"model":"KV-3", "year":1944, "origin":"USA"}]}' -H "Content-Type: application/json" -X POST <br>

(REMOVE) <br>
DELETE http://localhost:5001/songs/<songs_id> <br>
pvz: curl http://localhost:5001/songs/12 -X DELETE <br>

(UPDATE) <br>
PUT http://localhost:5001/songs/<songs_id> <br>
pvz: curl http://localhost:5001/songs/21 -d '{"name":"The Star-Spangled Banner", "artist":"John Stafford Smith", "date_created":"1814-02-03", "link":"https://www.youtube.com/watch?v=FqxJ_iuBPCs", "origin":"USA", "tanks":[{"id": 6, "model":"KV-3", "year":2008, "origin":"USA"}]}' -H "Content-Type: application/json" -X PUT <br>

TANKS <br>

curl http://localhost:5002/api/vehicles -X GET

curl http://localhost:5002/api/vehicles/1 -X GET

curl http://localhost:5002/api/vehicles -d '{"model":"KV-2", "year":1940, "origin":"USSR" }' -H "Content-Type: application/json" -X POST

curl http://localhost:5002/api/vehicles/4 -X DELETE

curl http://localhost:5002/api/vehicles/4 -d '{"model":"IS-2", "year":1943, "origin":"USSR" }' -H "Content-Type: application/json" -X PUT
