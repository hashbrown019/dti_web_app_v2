import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
	'/': {'content_type': 'text/html', 'filename': 'index.html'}
})

class socket_server(object):
	"""docstring for socket_server"""
	def __init__(self, arg):
		super(socket_server, self).__init__()
		self.arg = arg

	def start():
		return eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

	@sio.event
	def connect(self,sid, environ):
		print('connect ', sid)

	@sio.event
	def my_message(self,sid, data):
		print('message ', data)

	@sio.event
	def disconnect(self,sid):
		print('disconnect ', sid)

if __name__ == '__main__':
	eventlet.wsgi.server(eventlet.listen(('', 5000)), app)