#!/usr/bin/env python3

import postgresql
import flask
import json
import uuid
import os
from flask import request, render_template, jsonify, redirect, flash, session
from flask_restful import reqparse
from flask_httpauth import HTTPBasicAuth
from json2html import *


app = flask.Flask(__name__)
auth = HTTPBasicAuth()


def databaseConection():
    """Connect to a database"""
    # return postgresql.open('pq://titanic@192.172.253.49:5432/passengers')
    return postgresql.open("pq://{}@{}:{}/{}".format(
        os.environ['POSTGRESQL_DATABASE_USER'],
        os.environ['POSTGRESQL_SERVICE_HOST'],
        os.environ['POSTGRESQL_SERVICE_PORT'],
        os.environ['POSTGRESQL_DATABASE_NAME'])
    )


def toJason(data):
    """Convert to JSON format"""
    return json.dumps(data) + "\n"


def response(code, data):
    """Form a proper response"""
    if(data != ""):
        # Respond in JSON format with description
        return flask.Response(
            status=code, 
            mimetype="application/json", 
            response=toJason(data)
        )
    else:
        # Respons with status code only
        return flask.Response(status=code)


# Authentication

# @auth.get_password
@auth.verify_password
def verifyUser(username,password):
    """Verify a username and a password"""
    with databaseConection() as database:
        # Get user credentials for the database
        user = database.query("SELECT username, password FROM users")
        # Verify a username against the database
        if(username == user[0]["username"] and password == user[0]["password"]):
            return True
    return False


@auth.error_handler
def unauthorized():
    return response(401, {'error':'Unauthorized Access'})

# Handlers

@app.errorhandler(400)
def not_found(error):  
    return response(400, {'error':'Bad Request'})


@app.errorhandler(404)
def not_found(error):
    return response(404, {'error':'Not Found'})


@app.errorhandler(405)
def not_found(error):
    return response(405, {'error':'Method Not Allowed'})


@app.route('/login', methods=['GET','POST'])
def loginUser():
    """Show login screen if logged out"""
    if request.method == 'POST':
        if verifyUser(request.form['username'], request.form['password']):
            session['logged_in'] = True
            return rootIndex()
        else:
            return response(401, {'error':'Unauthorized Access'})


@app.route("/logout")
def logoutUser():
    session['logged_in'] = False
    return rootIndex()


@app.route('/', methods=['GET','POST'])
def rootIndex():
    """
    Display index (default) page.
    This endpoint is also used for HTTP health checks.
    """
    # Verify if user has already logged in
    if not session.get('logged_in'):
        return render_template('login.html')
    return "<h>Python API v1</h1><p>The application is meant to be used to manage the information about passengers"

# Define the API resources

@app.route('/people', methods=['GET'])
@auth.login_required
def getPassengers():
    """Get a list of all passengers from the database"""
    with databaseConection() as database:
        tuples = database.query("SELECT uuid, survived, pclass, name, sex, age, siblings_spouses_aboard, parents_children_aboard, fare FROM passengers")
        passengers = []
        
        for(uuid, survived, pclass, name, sex, age, siblings_spouses_aboard, parents_children_aboard, fare) in tuples:
            passengers.append({
                "uuid": uuid,
                "survived": bool(survived),
                "passengerClass": int(pclass),
                "name": name,
                "sex": sex,
                "age": int(age),
                "siblingsOrSpousesAboard": siblings_spouses_aboard,
                "parentsOrChildrenAboard": parents_children_aboard,
                "fare": float(fare)}
            )
        
        if str(request.mimetype) == 'application/json':
            return response(200, passengers)
        elif str(request.mimetype) == 'application/html':
            return json2html.convert(json = passengers)
        else:
            return json2html.convert(json = passengers)
    

@app.route('/people/<string:uuid>', methods=['GET'])
@auth.login_required
def getPassenger(uuid):
    """Get a passenger's information by its UUID"""
    with databaseConection() as database:
        tuples = database.query("SELECT uuid, survived, pclass, name, sex, age, siblings_spouses_aboard, parents_children_aboard, fare FROM passengers WHERE uuid='{}'".format(uuid))
        passengers = []

        for(uuid, survived, pclass, name, sex, age, siblings_spouses_aboard, parents_children_aboard, fare) in tuples:
            passengers.append({
                "uuid": uuid,
                "survived": bool(survived),
                "passengerClass": int(pclass),
                "name": name,
                "sex": sex,
                "age": int(age),
                "siblingsOrSpousesAboard": siblings_spouses_aboard,
                "parentsOrChildrenAboard": parents_children_aboard,
                "fare": float(fare)}
            )

            if str(request.mimetype) == 'application/json':
                return response(200, passengers)
            elif str(request.mimetype) == 'application/html':
                return json2html.convert(json = passengers)
            else:
                return json2html.convert(json = passengers)
    
    return response(400, "Passenger with UUID {} does not exist".format(uuid))


@app.route('/people', methods=['POST'])
@auth.login_required
def addPassenger():
    """Add a new passenger to the database"""
    # Parse arguments provided
    parser = reqparse.RequestParser()
    parser.add_argument("survived", type=bool)
    parser.add_argument("passengerClass", type=int)
    parser.add_argument("name")
    parser.add_argument("sex")
    parser.add_argument("age", type=int)
    parser.add_argument("siblingsOrSpousesAboard", type=int)
    parser.add_argument("parentsOrChildrenAboard", type=int)
    parser.add_argument("fare", type=float)
    args = parser.parse_args()

    with databaseConection() as database:
        # Verify whether a passenger already exists
        result = database.query("SELECT count(1) as record_count FROM passengers WHERE name='{}'".format(args["name"]))
        if(str(result) == "[(0,)]"):
            # Create a prepared statement
            insert = database.prepare("INSERT INTO passengers (uuid, survived, pclass, name, sex, age, siblings_spouses_aboard, parents_children_aboard, fare) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)")

            # Generate an ID for a new passenger
            passengerUuid = str(uuid.uuid4())

            # Insert a record
            (_, rowCounter) = insert(
                passengerUuid,
                args["survived"],
                args["passengerClass"],
                args["name"],
                args["sex"],
                args["age"],
                args["siblingsOrSpousesAboard"],
                args["parentsOrChildrenAboard"],
                args["fare"]
            )
            
            if rowCounter == 0:
                return response(404, "Passenger {} has not been added due to an error".format(args["name"]))
        
            passenger = {
                "uuid": passengerUuid,
                "survived": args["survived"],
                "passengerClass": args["passengerClass"],
                "name": args["name"],
                "sex": args["sex"],
                "age": args["age"],
                "siblingsOrSpousesAboard": args["siblingsOrSpousesAboard"],
                "parentsOrChildrenAboard": args["parentsOrChildrenAboard"],
                "fare": args["fare"]
            }

            return response(201, passenger)
        
        return response(400, "Passenger {} already exists".format(args["name"]))


@app.route('/people/<string:uuid>', methods=['DELETE'])
@auth.login_required
def removePassenger(uuid):
    """Remove a passenger by its UUID"""
    with databaseConection() as database:
        delete = database.prepare("DELETE FROM passengers WHERE uuid = $1")
        (_, rowCounter) = delete(uuid)

        if rowCounter == 0:
            return response(404, "Passenger with UUID {} does not exist".format(uuid))
        
        return response(200, {})


@app.route('/people/<string:uuid>', methods=['PUT'])
@auth.login_required
def alterPassenger(uuid):
    """Alter passenger's information"""
    # Parse arguments provided
    parser = reqparse.RequestParser()
    parser.add_argument("survived", type=bool)
    parser.add_argument("passengerClass", type=int)
    parser.add_argument("name")
    parser.add_argument("sex")
    parser.add_argument("age", type=int)
    parser.add_argument("siblingsOrSpousesAboard", type=int)
    parser.add_argument("parentsOrChildrenAboard", type=int)
    parser.add_argument("fare", type=float)
    args = parser.parse_args()

    with databaseConection() as database:
        update = database.prepare("UPDATE passengers SET survived = $2, pclass = $3, name = $4, sex = $5, age = $6, siblings_spouses_aboard = $7, parents_children_aboard = $8, fare = $9 WHERE uuid = $1")
        (_, rowCounter) = update(
            uuid, 
            args['survived'], 
            args['passengerClass'], 
            args['name'], 
            args['sex'], 
            args['age'], 
            args['siblingsOrSpousesAboard'], 
            args['parentsOrChildrenAboard'], 
            args['fare']
        )
        
        if rowCounter == 0:
            return response(404, "Passenger with UUID {} does not exist".format(uuid))
        
        return response(200, {})


if __name__ == '__main__':
    app.debug = True
    app_address = os.environ.get('APP_ADDRESS')
    app_port = int(os.environ.get('APP_PORT'))
    app.secret_key = os.urandom(24)
    app.run(host=app_address,port=app_port)
