from flask import Flask
from flask import request, jsonify
import os
import subprocess
import time


app = Flask(__name__)

@app.route("/")
def hello_world():
	return "<p>Hello, World!</p>"

@app.route("/experiment", methods = ['POST'])
def do_experiment():
	content = request.json
	runnumber = content["run"]
	subprocess.run("./run.sh sim  " + str(runnumber), shell=True, cwd = "/headless/seams-swim/swim/simulations/swim")
	return "Started run " + str(runnumber)

@app.route("/plot", methods = ['POST'])
def plot_results():
	content = request.json
	plotname = content["name"]
	subprocess.run("../swim/tools/plotResults.sh SWIM sim 1 " + str(plotname)+ str(round(time.time())) + ".png", shell=True, cwd = "/headless/seams-swim/results/")
	return "Plotted " + str(plotname) + ".png"


if __name__ == '__main__':
	app.run(host='0.0.0.0')

