import mars_weather
from flask import Flask, render_template, redirect
import pymongo

# Create a Flask app
app = Flask(__name__)

# Connect to MongoDB
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db

# index route
@app.route("/")
def index():
    mars = db.mars.find_one()
    return render_template('index.html', mars=mars)


@app.route("/scrape")
def scrape():
    mars_data = mars_weather.scrape()
    db.mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
