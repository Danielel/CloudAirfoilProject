#!flask/bin/python
from flask import Flask, jsonify
import subprocess
import sys
import jsonExample

app = Flask(__name__)


@app.route('/')#, methods=['GET'])
def flask_example():
    #data=subprocess.check_output(["cowsay","Hello student"])
    data = jsonExample.readJsonDataFile()
    return data

if __name__ == '__main__':
    
    app.run(host='0.0.0.0',debug=True)
