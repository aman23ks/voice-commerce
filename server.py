import os
from flask import Flask, render_template, url_for, request, redirect, jsonify, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import Binary
from google.cloud import speech
from google.cloud import translate_v2
import bcrypt
import uuid
from authlib.integrations.flask_client import OAuth
import jwt

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"key.json"

app = Flask(__name__)

client = MongoClient('localhost', 27017)

app.secret_key = "testing"

# login_manager = LoginManager()
# login_manager.init_app(app)

appConf = {
    "OAUTH2_CLIENT_ID":"378032575715-lvv8a51t9rm1gs5f4vrobtgfqun9kf3j.apps.googleusercontent.com",
    "OAUTH2_CLIENT_SECRET":"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",
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": "77ac1e43-41d2-4f65-a6bd-36bfa405773b",
    "FLASK_PORT": 5000
}

app.secret_key = appConf.get("FLASK_SECRET")

oauth = OAuth(app)

oauth.register(
    "Vcom",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email"
        # 'code_challenge_method': 'S256'  # enable PKCE
    },
    server_metadata_url=f'{appConf.get("OAUTH2_META_URL")}',
)

#assign URLs to have a particular route 
@app.route("/", methods=['POST', 'GET'])
def register():
    message = ''
    #if method post in register
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #if found in database showcase that it's found 
        user_found = users.find_one({"name": user})
        email_found = users.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('register.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('register.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('register.html', message=message)
        else:
            #hash the password and encode it
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            #assing them in a dictionary in key value pairs
            user_input = {'name': user, 'email': email, 'password': hashed}
            #insert it in the record collection
            users.insert_one(user_input)
            
            #find the new created account and its email
            user_data = users.find_one({"email": email})
            new_email = user_data['email']
            session["email"] = new_email
            #if registered redirect to logged in as the registered user
            return render_template('index.html', email=new_email)
    return render_template('register.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("register"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        #check if email exists in database
        email_found = users.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            #encode the password and check if it matches
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('register'))
            else:
                if "email" in session:
                    return redirect(url_for("register"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)

@app.route('/logged_in')
def logged_in():
    if "email" in session:
        email = session["email"]
        return render_template('index.html', email=email)
    else:
        return redirect(url_for("login"))

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('register.html')

@app.route("/google-login")
def googleLogin():
    return oauth.Vcom.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))

@app.route("/google-signin")
def googleCallback():
    # fetch access token and id token using authorization code
    token = oauth.Vcom.authorize_access_token()

    # google people API - https://developers.google.com/people/api/rest/v1/people/get
    # Google OAuth 2.0 playground - https://developers.google.com/oauthplayground
    # make sure you enable the Google People API in the Google Developers console under "Enabled APIs & services" section

    # set complete user information in the session
    email = token['userinfo']['email']
    email_found = users.find_one({"email": email})
    session["email"] = email
    name = token['userinfo']['name']
    
    if not email_found:
        #assing them in a dictionary in key value pairs
        user_input = {'name': name, 'email': email}
        #insert it in the record collection
        users.insert_one(user_input)

    return render_template('index.html', email=email)

@app.route("/index", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/products", methods=['GET'])
def products():
    user_products = prod.find_one({"user_email": session['email']})
    if user_products is None or user_products['products'] == []:
        return render_template('no_products.html')
    return render_template('products.html', products=user_products['products'])

@app.route("/orders", methods=['GET'])
def orders():
    return render_template('orders.html')

@app.route("/add-product", methods=['POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_price = request.form['product_price']
    user_products = prod.find_one({"user_email": session['email']})
    if user_products:
        new_product = {"id": str(uuid.uuid1()), "product_name": product_name, "product_price": product_price}
        prod.update_one({"user_email": session["email"]}, {"$push": {"products": new_product}})
        user_products = prod.find_one({"user_email": session['email']})
        return render_template('products.html', products=user_products['products'])
    else:
        new_product = {"id": str(uuid.uuid1()), "product_name": product_name, "product_price": product_price}
        prod.insert_one({"user_email": session["email"], "products": [new_product]})
        user_products = prod.find_one({"user_email": session['email']})
        return render_template('products.html', products=user_products['products'])

@app.route("/<id>/delete/")
def delete(id):
    prod.update_one({
        "user_email": session["email"],
        "products": {
            "$elemMatch": {
                "id": id
            }
        }
    }, {
        "$pull": {"products": { "id": id } }
    })
    return redirect(url_for('products'))

@app.route("/qrcode", methods=['GET'])
def qrcode():
    email = session['email']
    user = users.find_one({"email": email})
    user_id = str(user['_id'])
    return render_template('qrcode.html', user_id=user_id)

@app.route('/process_audio', methods=['POST'])
def process_audio():
    audio_file = request.files['audio']
    audio_data = audio_file.read()
    audio_file_path = 'temp_audio.wav'
    with open(audio_file_path, 'wb') as f:
        f.write(audio_data)
    client = speech.SpeechClient.from_service_account_file('key.json')
    file_name = 'temp_audio.wav'
    with open(file_name, 'rb') as f:
        wav_data = f.read()
    audio_file = speech.RecognitionAudio(content=wav_data)
    config = speech.RecognitionConfig(
        sample_rate_hertz=48000,
        enable_automatic_punctuation=True,
        language_code='hi-IN'
    )
    response = client.recognize(
        config=config,
        audio=audio_file
    )
    text = response.results[0].alternatives[0].transcript
    translate_client = translate_v2.Client()
    output = translate_client.translate(text, source_language="hi", target_language="en")
    return jsonify({'translatedText': output['translatedText']})

# This is a mongodb database
db = client.flask_database

# This is a products collection
prod = db.products
users = db.users

if __name__ == "__main__":
    app.run(debug=True)