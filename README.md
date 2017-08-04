# alexa_ros_publisher
A simple node that allows Amazon Alexa and ROS to work together

############################README####################################
Authors:
Alex Meier
Lilia Heinold

Alexa Ros Publisher node: 
This package is intended to be a simple example of what a publisher
node might look like for an amazon alexa integrated ros program.  Note
that the ros, and alexa operations are held in completely self
contained processes that comunicate via a multiprocessing pipe or
queue.  This setup is a result of ros not integrating nicely with the
python flask module, which is what we used for parsing the amazon
service requests.  Because of how ros works, this needs to be run as
its own independent process, and not as a webservice with apache.
This package does not handle ssl, which is required for use with the
alexa skills kit. One way around this is to use a tunneling utility
such as ngrok, to handle the ssl certificate for you, as well as avoid
the need to forward ports to the service. Response text can be stored
in the templates.yaml file in the scripts directory of this project.


This project makes use of the flask_ask module, doccumentation and
tutorials on this module can be found at:
https://flask-ask.readthedocs.io/en/latest/
and more general information about the base flask module at:
http://flask.pocoo.org/


Flask and flask ask can be installed with:
sudo pip install flask_ask

Note: The following dependancies are required by flask and flask_ask
modules, but are not installed automatically with pypy:

Apt-get:
libssl-dev
libffi-dev

Pip:
Cryptography
Werkzeug
itsdangerous
Jinja2
click

To run, just use rosrun on alexa_ros_publisher.py or run with a launchfile.
