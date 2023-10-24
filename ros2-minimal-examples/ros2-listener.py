from __future__ import print_function
import roslibpy
from geometry_msgs.msg import Twist 

# client = roslibpy.Ros(host='54.90.73.9', port=9090)

host='54.90.73.9'
port=9090
client = roslibpy.Ros("ws://%s:%d" % (host, port))
client.run()

listener = roslibpy.Topic(client, '/chatter', 'std_msgs/String')
listener.subscribe(lambda message: print('Heard talking: ' + message['data']))

speedSub = roslibpy.Topic(client, '/cmd_vel', 'geometry_msgs/Twist')
speedSub.subscribe(lambda message: print('Heard speed data: ' + str(message["linear"]) + str(message["angular"]))) #{'linear': {'x': -1.0, 'y': 0.0, 'z': 0.0}, 'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}}

try:
    while True:
        pass
except KeyboardInterrupt:
    client.terminate()