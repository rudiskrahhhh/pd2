from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from data import init_db, add_user, add_message, get_messages, get_user_stats

app = Flask(__name__)

# Inicializē datubāzi
init_db()

@app.route('/')
def index():
    return redirect(url_for('registration'))

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        
        # Ievades pārbaude
        if not first_name or not last_name or not username:
            return render_template('registration.html', error="Visi lauki ir jāaizpilda!")
        
        # Pievieno lietotāju datubāzē
        if not add_user(first_name, last_name, username):
            return render_template('registration.html', error="Šāds lietotājvārds jau eksistē!")
        
        return redirect(url_for('message'))
    return render_template('registration.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form['username']
        message_text = request.form['message']
        
        # Ievades pārbaude
        if not message_text:
            return render_template('message.html', error="Ziņojumam jābūt tekstam!", users=get_users())
        
        add_message(username, message_text)
    
    messages = get_messages()
    users = get_users()
    return render_template('message.html', messages=messages, users=users)

@app.route('/statistics')
def statistics():
    stats = get_user_stats()
    return render_template('statistics.html', stats=stats)

def get_users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM users ORDER BY username')
    users = cursor.fetchall()
    conn.close()
    return users

if __name__ == '__main__':
    app.run(debug=True)