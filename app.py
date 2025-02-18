from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import socket
import geocoder
import datetime

app = Flask(__name__)
socketio = SocketIO(app)

# Store users with their info
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    username = users.get(request.sid, {}).get('username', 'Anonymous')
    country_flag = users.get(request.sid, {}).get('country_flag', '🌍')  # Default to globe flag
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')

    # Emit the message to all users
    emit('new_message', {'username': username, 'country_flag': country_flag, 'message': msg, 'timestamp': timestamp}, broadcast=True)

@socketio.on('set_username')
def handle_username(username):
    # Get the user's IP address
    user_ip = request.remote_addr
    g = geocoder.ip(user_ip)
    country = g.country

    # Simple flag handling (you can replace with images of flags or a more detailed system)
    country_flag = f"🇺🇸" if country == 'United States' else "🌍"  # Placeholder for actual flag logic

    # Store the user's username and country flag
    users[request.sid] = {'username': username, 'country_flag': country_flag}
    emit('username_set', {'username': username, 'country_flag': country_flag})

if __name__ == '__main__':
    socketio.run(app, debug=True)
