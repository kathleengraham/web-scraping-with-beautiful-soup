############################## SET UP ##############################
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

############################## ROUTES ##############################
# default route that renders index.html template
@app.route("/")
def index():
    # find data 
    mars_info = db.mars_info.find_one()
    # return template
    return render_template("index.html", text=mars_info)

# scrape route
@app.route("/scrape")
def scrape():
    mars_info = db.mars_info
    mars_scraping = scrape_mars.scrape_mars_nasa_news()
    mars_scraping = scrape_mars.scrape_mars_featured_image()
    mars_scraping = scrape_mars.scrape_mars_weather_tweet()
    mars_scraping = scrape_mars.scrape_mars_facts_table()
    mars_scraping = scrape_mars.scrape_mars_hemispheres()
    mars_info.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)