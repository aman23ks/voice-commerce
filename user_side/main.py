import uuid
from flask import Flask, render_template, redirect, request, session
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = "testing"
client = MongoClient('localhost', 27017)
global user_id

@app.route("/", methods=['GET', 'POST'])
def index():
    return redirect(f'/{user_id}/store')

@app.route("/<id>/store", methods=['GET', 'POST'])
def store(id):
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())  # Generate a unique session ID for the guest user
    global user_id
    user = users.find_one({"_id": ObjectId(id)})
    user_email = user['email']
    products = prod.find_one({"user_email": user_email})['products']
    user_id = id
    return render_template('store.html', products=products, id = user_id, session_id=session['user_id'])

@app.route("/<id>/cart", methods=["GET", "POST"])
def cart(id):
    
    if request.method == "POST":
        request_data = request.json  
        sessionId = request_data.get('sessionId')
        
        userCart = user_cart.find_one({"session_id":sessionId})
        
        if userCart:
            addProduct = {"productName":request_data.get('productName'), "productPrice":request_data.get('productPrice'), "quantity":request_data.get('quantity')}
            user_cart.update_one({"session_id":sessionId}, {"$push": {"cartItems": addProduct}})
        
        else:
            addProduct = {"productName":request_data.get('productName'), "productPrice":request_data.get('productPrice'), "quantity":request_data.get('quantity')}
            user_cart.insert_one({"userId":id, "session_id":sessionId, "cartItems":[addProduct]})
            
        return "Successfull"
    
    user = users.find_one({"_id": ObjectId(id)})
    user_email = user['email']
    products = prod.find_one({"user_email": user_email})['products']
    return render_template("cart.html", products = products)

# This is a mongodb database
db = client.flask_database

# This is a products collection
prod = db.products
users = db.users
user_cart = db.cart

if __name__ == "__main__":
    app.run(port=5001, debug=True)