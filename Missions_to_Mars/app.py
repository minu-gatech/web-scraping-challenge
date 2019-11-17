# import necessary libraries
from flask import Flask, render_template, redirect
import pymongo


# create instance of Flask app
app = Flask(__name__)


# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define the 'classDB' database in Mongo
db = client.mars_DB
collection = db.mars


# create route renders main page
@app.route("/")
def index():
	return render_template("index1.html")
	

# create route that query the Mongo database and pass the mars data into an HTML template to display the data
@app.route("/mars")
def mars():
	data = db.mars.find_one()
	db.mars.remove();
	return render_template("index.html", dict = data)


# create route that will import scrape_mars script and call the scrape function.
@app.route("/scrape")
def scraper():
	from scrape_mars import scrape
	# Data returned from scarpe_mars.py
	data = scrape()

	# Dictionary to be inserted as a MongoDB document
	collection.insert_one(data)
		
	return redirect("/mars", code=302)


if __name__ == "__main__":
    app.run(debug=True)
