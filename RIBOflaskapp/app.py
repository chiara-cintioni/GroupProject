# importiamo l'oggetto flask dal flask package.
from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

# usiamo l'oggetto Flask per creare l'istanza della nostra app Flask con il nome app.
# __name__ è il nome del modulo python corrente. Usato per dire all'app dove si trova. Serve perché Flask definisce dei path dietro le quinte.
app = Flask(__name__)

# ora che abbiamo creato l'app, la useremo per gestire le richieste HTTP che riceviamo.

client = MongoClient('mongodb+srv://DeniseFalcone:Giappone4ever@cluster0.yelotpf.mongodb.net/test', 27017)
db= client.RIBOdb
collection= db.prova

#è un decoratore che rende una funzione python regolare in una funzione di vista Flask.
#serve a convertire il valore di ritorno della funzione in una risposta HTTP da far vedere
#al cliente HTTP, come un browser web.
#'/' vuol dire che la funzione risponderà alle richieste web per l'url '/' che è l'url principale.
# corrisponde al nostro home.html
@app.route('/', methods=('GET','POST'))
def index():
    if request.method == 'POST':
        content = request.form['content']
        degree = request.form['degree']
        collection.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('index'))

    all_collections = collection.find()
    return render_template('index.html', collection=all_collections)

@app.route('/home/')
def home():
    return render_template('home.html')

@app.route('/search/')
def search():
    return render_template('search.html')

@app.route('/contact/')
def contact():
    return render_template('contact.html')

@app.route('/documentation/')
def documentation():
    return render_template('documentation.html')

@app.route('/list', methods=['GET','POST'])
def lists():
    if request.method == 'POST':
        my_position = request.form['mypos']#form input on initial position
        check_db = collection.find()#check all documents in collection
        for record in check_db:
            if (record['content'] == my_position):
                return 'found'
            else:
                return 'sorry route not found'

    return render_template('form.html')

@app.post('/<id>/delete/')
def delete(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

