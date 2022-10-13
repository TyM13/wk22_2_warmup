import string
from apihelper import check_endpoint_info
import dbhelper
from flask import Flask, request, make_response
import json
import dbcreds


app = Flask(__name__)

@app.get('/api/pokemon')
def show_all_pokemon():
    results = dbhelper.run_statment('CALL all_pokemon')
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)


@app.post('/api/pokemon')
def insert_pokemon():
    invalid = check_endpoint_info(request.json, ['pokemon_name', 'pokemon_description', 'pokemon_image'])
    if(invalid != None):
        return make_response(json.dumps(invalid, default=str), 400)

    results = dbhelper.run_statment('CALL insert_pokemon(?,?,?)', 
    [request.json.get('pokemon_name'), request.json.get('pokemon_description'), request.json.get('pokemon_image')])
    if(type(results) == list):
        return make_response(json.dumps(results, default=str), 200)
    else:
        return make_response(json.dumps(results, default=str), 500)







if(dbcreds.production_mode == True):
    print("Running in Production Mode")
    import bjoern # type: ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode!")
    app.run(debug=True)