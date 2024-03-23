from flask import Flask
from flask import json
import logging
app = Flask(__name__)

@app.route("/status")
def status_1():
    app.logger.info("Returning the status")
    response = app.response_class(
        response = json.dumps({"result":"OK - healthy"}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route("/metrics")
def status():
    app.logger.info("Returning the metrics")
    response = app.response_class(
        response = json.dumps({"status":"success","code":0,"data":{"UserCount":140,"UserCountActive":23}}),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/")
def hello():
    app.logger.info('Main request successfull')
    return "Hello World!"

if __name__ == "__main__":
    logging.basicConfig(filename='app.log',level=logging.DEBUG)
    app.run(host='0.0.0.0')