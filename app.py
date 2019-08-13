# dependencies
from flask import Flask, render_template, redirec
import pymongo
import scrape_mars

# initialize flask
app = Flask(__name__)

# remember to start server before executing
client = pymongo.MongoClient('mongodb://localhost:27017/')

# MongoDb database and collection
db = client.mars_DB
collection = db.mars_info

# default route that renders index.html template
@app.route("/")
def index():

# add index route here






# scrape route
@app.route("/scrape")
def scrape():

# add scrape route here





if __name__ == "__main__":
    app.run(debug=True)