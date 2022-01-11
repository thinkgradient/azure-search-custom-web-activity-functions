import logging
import os
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        body = json.dumps(req.get_json())
    except ValueError:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )
    
    if body:
        result = compose_response(body)
        return func.HttpResponse(result, mimetype="application/json")
    else:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )

def compose_response(json_data):
    values = json.loads(json_data)['values']
    
    # Prepare the Output before the loop
    results = {}
    results["values"] = []
    
    for value in values:
        output_record = transform_value(value)
        if output_record != None:
            results["values"].append(output_record)
    return json.dumps(results, ensure_ascii=False)


def transform_value(value):
    try:
        recordId = value['recordId']
    except AssertionError  as error:
        return None

    # Validate the inputs
    try:         
        assert ('data' in value), "'data' field is required."
        data = value['data']        
    except AssertionError  as error:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Error:" + error.args[0] }   ]       
            })

    try:       
        longitude = data['LON']
        latitude = data['LAT']
        if longitude < -180:
            longitude = -179
        if longitude > 80:
            longitude = 79
        if latitude < -90:
            latitude = -89
        if latitude > 90:
            latitude = 89


        
        


    except ValueError as err:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": f"Could not complete operation for record. {err}" }   ]       
            })

    return ({
            "recordId": recordId,
            "data": {
                "data": {"type": "Point", "coordinates": [longitude, latitude]}
                }
            })