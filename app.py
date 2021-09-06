# app.py

from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   # mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
   # mars = mongo.db.mars
   try:
      mars = mongo.db.mars
      mars_data = scraping.scrape_all()
      mars.update({}, mars_data, upsert=True)
      # mars.replace_one({}, mars_data, upsert=True)
    
   except AttributeError:
        return None, None  
        
   else:
      browser.quit()
      return redirect('/', code=404)

   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()

