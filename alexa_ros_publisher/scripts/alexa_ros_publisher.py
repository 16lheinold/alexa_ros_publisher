#!/usr/bin/env python

# The following is a sample node interfacing amazon alexa and a simple ros 
# string publisher using flask_ask (a flask based plugin designed specifically 
# for use with amazon skills kit) as a web framework. Note: the ros component
# and the flask components are isolated to two seperate processes. This is 
# needed because ros and flask are not compatable, and will cause issues
# when run together in the same thread.  The two processes can talk to each
# other via a multiprocessing Queue (a Pipe also works effectively).

import os
import sys
import signal
from multiprocessing import Process, Queue
import rospy
from std_msgs.msg import String
from flask import Flask, request, render_template
from flask_ask import Ask, statement

intent_queue = Queue(1)


class RosProcess(object):
	def __init__(self, intent_queue):
		self.intent_queue = intent_queue
		self.stringPub = rospy.Publisher("Alexa_pub", String, queue_size=1000)
	
	#this function loops through all callbacks, and publishing functions
	def listen(self):
		while(not rospy.is_shutdown()):
			myString = self.intent_queue.get() #waits for queue to not be empty

			rospy.loginfo("publishing string: %s" % myString)
			self.stringPub.publish(myString)



# As of right now, there is no easy way for flask to call intent callbacks with 
# an instance of the alexaProcess object, making references to instance variables
# impossible.  As a workaround all shared variables need to be either global or
# class variables.

class AlexaProcess(object):
	app = Flask(__name__)
	ask = Ask(app, '/')
	intent_queue = Queue(1)

	def __init__(self, queue):
		intent_queue = queue
	#this function is called when a request is recieved
	@ask.intent('getString')
	def getString(string):
		#all intent slots are parsed as unicode literals, so you need to caste them 
		s = str(string) 
		#send string over to ros_process
		intent_queue.put(s)

		#send response
		#response templates are in templates.yaml
		response = render_template('stringPubResponse', string=string)
		return statement(response).simple_card('stringPubResponse', response)

#functions to initialize the ros and alexa processes 
def startRosProcess(intent_queue):
	rospy.init_node('alexa_string_pub')
	ros_process = RosProcess(intent_queue)
	ros_process.listen()

def startAlexaProcess(queue):
	alexa_process = AlexaProcess(queue)
	AlexaProcess.app.run(debug=True)



if __name__ == '__main__':
	intent_queue = Queue(1)

	try:
		alexa_process = Process(target=startAlexaProcess, args=(intent_queue,))
		ros_process = Process(target=startRosProcess, args=(intent_queue,))

		#run both processes
		alexa_process.start()
		ros_process.start()
		alexa_process.join()
		ros_process.join()
	except KeyboardInterrupt:
		#this is dirty, but the only way we've found to ensure both processes die
		#when you Ctrl-c this node
		os.system('kill -9 {}'.format(ros_process.pid))
    	os.system('kill -9 {}'.format(alexa_process.pid))

