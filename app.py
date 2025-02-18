from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import socket
import geocoder
import datetime
import pytz

app = Flask(__name__)
socketio = SocketIO(app)

users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    username = users.get(request.sid, {}).get('username', 'Anonymous')
    country_flag = users.get(request.sid, {}).get('country_flag', '🌍')
    timestamp = datetime.datetime.now(pytz.timezone('US/Eastern')).strftime('%H:%M:%S')

    # Emit the message to all users
    emit('new_message', {'username': username, 'country_flag': country_flag, 'message': msg, 'timestamp': timestamp}, broadcast=True)

@socketio.on('set_username')
def handle_username(username, anonymous=False):
    user_ip = request.remote_addr
    g = geocoder.ip(user_ip)
    country = g.country

    country_flag = f"🇺🇸" if country == 'United States' else "🌍"

    # If anonymous, don't store username
    if anonymous:
        users[request.sid] = {'username': 'Anonymous', 'country_flag': country_flag}
    else:
        users[request.sid] = {'username': username, 'country_flag': country_flag}
    
    emit('username_set', {'username': username if not anonymous else 'Anonymous', 'country_flag': country_flag})

if __name__ == '__main__':
    socketio.run(app, debug=True)
