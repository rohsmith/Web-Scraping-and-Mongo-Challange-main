from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
     # Find one record of data from the mongo database
    destination_data = mongo.db.mars.find_one()
    # Return template and data
    return render_template("index.html", mars_data=destination_data)

@app.route("/scrape")
def scraper():

    mars_dict = mongo.db.destination_data
    mars_data = scrape_mars.scrape()
    mars_dict.update({}, mars_data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)