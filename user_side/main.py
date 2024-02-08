from flask import Flask, render_template, redirect, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('localhost', 27017)
global user_id

@app.route("/", methods=['GET', 'POST'])
def index():
    return redirect(f'/{user_id}/store')

@app.route("/<id>/store", methods=['GET', 'POST'])
def store(id):
    global user_id
    user = users.find_one({"_id": ObjectId(id)})
    user_email = user['email']
    products = prod.find_one({"user_email": user_email})['products']
    user_id = id
    return render_template('store.html', products=products, id = user_id)

@app.route("/<id>/cart", methods=["GET", "POST"])
def cart(id):
    user = users.find_one({"_id": ObjectId(id)})
    user_email = user['email']
    products = prod.find_one({"user_email": user_email})['products']
    return render_template("cart.html", products = products)

# This is a mongodb database
db = client.flask_database

# This is a products collection
prod = db.products
users = db.users

if __name__ == "__main__":
    app.run(port=5001, debug=True)