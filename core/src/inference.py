import socketio

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')


@sio.on("inference")
def my_message(data):
    print('message received with ', data)
    # sio.emit('my response', {'response': 'my response'})


@sio.event
def disconnect():
    print('disconnected from server')


sio.connect('ws://localhost:8080')
sio.wait()
