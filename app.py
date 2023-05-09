from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

app = Flask(__name__)
socketio = SocketIO(app)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: %s", str(rc))
    client.subscribe("dr/temperature")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        socketio.emit('temperature_update', {'data': payload})
    except Exception as e:
        print("Error sending message: %s", str(e))

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("172.20.10.3", 1883, 60)
    client.loop_start()

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    socketio.run(app)
