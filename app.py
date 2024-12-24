from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = '8f3f290ea5731e929f1e5f404b6892b7f6bce3c478e2152434e5c309b0b71e99'
socketio = SocketIO(app)


@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(f"{username} has joined the room.", to=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    send(f"{data['username']}: {data['message']}", to=room)

@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(f"{username} has left the room.", to=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
