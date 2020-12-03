#Dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_db'
mongo = PyMongo(app)

#Main route
@app.route('/')
def index():
    listing = mongo.db.listings.find_one()
    return render_template('index.html', listing=listing)

#Scrape route
@app.route('/scrape')
def scrape():
    listing = scrape_mars.scrape_mars()
    mongo.db.listings.update({}, listing, upsert=True)

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)