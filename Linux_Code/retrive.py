from flask import Flask, render_template, redirect, url_for
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
app=Flask(__name__)

@app.route('/')
def index():
	return render_template('test.html')

@app.route('/<state>')
def turnOn(state):
	print ("send: ", state)
	sock.sendto(state[0].encode(), ('192.168.0.32',8080)) #Pi
	return redirect(url_for('index'))

if __name__=='__main__':
	app.run(host='localhost', port=80, debug=True)

