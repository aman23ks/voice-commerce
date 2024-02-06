import os
from flask import Flask, render_template, url_for, request, redirect, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from google.cloud import speech
from google.cloud import translate_v2

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"key.json"

app = Flask(__name__)

client = MongoClient('localhost', 27017)

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/products", methods=['GET'])
def products():
    all_products = prod.find()
    products = []
    for product in all_products:
        products.append(product)
    return render_template('products.html', products=products)

@app.route("/orders", methods=['GET'])
def orders():
    return render_template('orders.html')

@app.route("/add-product", methods=['POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_price = request.form['product_price']
    prod.insert_one({"product_name": product_name, "product_price": product_price})
    all_products = prod.find()
    products = []
    for product in all_products:
        products.append(product)
    return render_template('products.html', products=products)

@app.route("/<id>/delete/")
def delete(id):
    prod.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('products'))

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

if __name__ == "__main__":
    app.run(debug=True)