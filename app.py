from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, emit
from geopy.geocoders import Nominatim

app = Flask(__name__)
socketio = SocketIO(app)

# Dummy IP-to-Flag data (you can integrate a real IP-to-country API here)
IP_TO_COUNTRY = {
    "127.0.0.1": "US",  # Localhost for testing, would replace with actual IP
    "192.168.1.1": "IN",
}

# Dummy flag data based on country codes
COUNTRY_FLAGS = {
    "US": "🇺🇸",
    "IN": "🇮🇳",
    "GB": "🇬🇧",
    "CA": "🇨🇦",
    "FR": "🇫🇷",
    "BR": "🇧🇷",
}

# Get country code by IP (dummy function for now)
def get_country_by_ip(ip):
    country_code = IP_TO_COUNTRY.get(ip, "US")  # Default to 'US'
    return COUNTRY_FLAGS.get(country_code, "🌍")  # Default to globe emoji if no flag found

# Serve the HTML and assets
@app.route('/')
def index():
    return render_template('index.html')

# Listen for new users joining and for messages
@socketio.on('join')
def handle_join(username):
    # Detect the IP address (Here we simulate it using a placeholder)
    user_ip = request.remote_addr
    flag = get_country_by_ip(user_ip)
    
    emit('new_user', {'username': username, 'flag': flag}, broadcast=True)

# Handle sending chat messages
@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)

# Run the app
if __name__ == '__main__':
    socketio.run(app, debug=True)
