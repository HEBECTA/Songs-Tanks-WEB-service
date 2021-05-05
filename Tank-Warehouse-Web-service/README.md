# Tank Warehouse
 **Building in docker**<br />
Clone the project<br />
Navigate to the directory on command line<br />
```docker-compose build```<br />
```docker-compose up -d```<br />

URL = localhost:5000/api<br />

**Usage**<br />

**GET All**<br />
localhost:5000/api/vehicles<br />
Response: returns all vehicles in an array if successful<br />

**GET by vehicleId**<br />
localhost:5000/api/vehicles/<int: vehicleId><br />
Response: returns object if successful<br />

**POST**<br />
localhost:5000/api/vehicles + JSON body<br />
example body:<br />
```
{
    "model": "T34",
    "year": 1945,
    "origin": USSR
}
```
New vehicle will be created with automatically incremented id if successful<br />
An error message will be returned on failure<br />
Status on success: ```201```<br />
Status on failure: ```400```<br />

**PATCH by vehicleId**<br />
localhost:5000/api/vehicles/<int: vehicleId> + JSON body<br />
example body (requires at least one parameter of a vehicle object):<br />
```
{
    "model": "KV-1"
}
```
Edited object will be returned upon success<br />
Otherwise an error message will be returned<br />
Status on success: ```200```<br />
Status on failure: ```404```<br />

**PUT by vehicleId**<br />
localhost:5000/api/vehicles/<int: vehicleId> + JSON body<br />
example body (requires all parameters of a vehicle object):<br />
```
{
    "model": "KV-1"
    "year": 1943,
    "origin": "USSR"
}
```
Replaced object will be returned upon success<br />
Otherwise an error message will be returned<br />
Status on success: ```200```<br />
Status on failure: ```404```<br />

**DELETE by vehicleId**<br />
localhost:5000/api/vehicles/<int: vehicleId><br />
Object with the corresponding id will be deleted upon success<br />
An error message will be returned on failure<br />
Status on success: ```200```<br />
Status on failure: ```404```<br />
