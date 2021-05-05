from flask import Flask, request, jsonify, abort, Response
import json

server = Flask(__name__)
port = 5002

vehicles = [
   {"id" : 1,
     "model": "AMX 40",
     "year": "1983",
     "origin": "France"
     },
     {"id" : 2,
     "model": "KV-1",
     "year": "1939",
     "origin": "USSR"
     },
     {"id" : 3,
     "model": "Jagdpanzer 38",
     "year": "1944",
     "origin": "Nazi Germany"
     }
]

currentId = 4

@server.route("/")
def home():
    return ("<h1>PC vehicles list</h1><a href='http://localhost:%d/api/vehicles'>All vehicles</a>" % port)


@server.route("/api/vehicles", methods = ["GET"])
def GetAllVehicles():
    if request.method != "GET":
        abort(404)

    return jsonify(vehicles)

@server.route("/api/vehicles", methods = ["POST"])
def PostAVehicle():
    if request.method != "POST":
        abort(404)

    data = request.get_json(force=True)
    if "model" in data and "year" in data and "origin" in data:
        global currentId
        vehicle ={
            "id": currentId,
            "model": data["model"],
            "year": data["year"],
            "origin": data["origin"]
        }
        vehicles.append(vehicle)
        currentId += 1
        return Response(response=(json.dumps({"Success":"Vehicle added", "id" : str(currentId-1)})), status=201, headers={"location": "/api/vehicles/"+str(currentId-1) }, mimetype="application/json")
    else:
        error = "Missing "
        if "model" not in data:
            error += "model "
        if "year" not in data:
            error += "year "
        if "origin" not in data:
            error += "origin "
        error +=  ".Please spefify in Body."
        return Response(json.dumps({"Failure" : error}),status=400,mimetype="application/json")


@server.route("/api/vehicles/<int:vehicleId>", methods = ["GET"])
def GetOneVehicle(vehicleId):
    if request.method != "GET":
        abort(404)

    return jsonify(vehicles[vehicleId])

@server.route("/api/vehicles/<int:vehicleId>", methods = ["PATCH"])
def PatchAVehicle(vehicleId):
    if request.method != "PATCH":
        abort(404)

    data = request.get_json("force=True")
    if "model" not in data and "year" not in data and "origin" not in data:
        error = "Missing "
        if "model" not in data:
            error += "model "
        if "year" not in data:
            error += "year "
        if "origin" not in data:
            error += "origin "
        error +=  ".Please spefify in Body."
        return Response(json.dumps({"Failure" : error}),status=404, mimetype="application/json")

    message = ""
    if "model" in data:
        vehicles[vehicleId]["model"] = data["model"]
        message += "model "
    if "year" in data:
        vehicles[vehicleId]["year"] = data["year"]
        message += "year "
    if "origin" in data:
        vehicles[vehicleId]["origin"] = data["origin"]
        message += "origin "
    message += "have been changed"
    return Response(json.dumps(vehicles[vehicleId]),status=200, mimetype="application/json")

@server.route("/api/vehicles/<int:vehicleId>", methods = ["PUT"])
def PutAVehicle(vehicleId):
    if request.method != "PUT":
        abort(404)

    data = request.get_json("force=True")
    if "model" not in data or "year" not in data or "origin" not in data:
        error = "Missing "
        if "model" not in data:
            error += "model "
        if "year" not in data:
            error += "year "
        if "origin" not in data:
            error += "origin "
        error +=  ".Please spefify in Body."
        return Response(json.dumps({"Failure" : error}),status=404, mimetype="application/json")

    message = ""
    if "model" in data:
        vehicles[vehicleId]["model"] = data["model"]
        message += "model "
    if "year" in data:
        vehicles[vehicleId]["year"] = data["year"]
        message += "year "
    if "origin" in data:
        vehicles[vehicleId]["origin"] = data["origin"]
        message += "origin "
    message += "have been changed"
    return Response(json.dumps(vehicles[vehicleId]),status=200, mimetype="application/json")

@server.route("/api/vehicles/<int:vehicleId>", methods = ["DELETE"])
def DeleteAVehicle(vehicleId):
    if request.method != "DELETE":
        abort(404)

    for vehicle in vehicles:
        if vehicle["id"] == vehicleId:
            vehicles.remove(vehicle)
            return Response(response=(json.dumps({"Success" : "Deleted"})), status=204, mimetype="application/json")
        error = "There is no such vehicle in vehicles"
        return Response(json.dumps({"Failure" : error}),status=400,mimetype="application/json")

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000, debug=True)

