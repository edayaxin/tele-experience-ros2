import time

import roslibpy
from geometry_msgs.msg import Twist 

# client = roslibpy.Ros(host='localhost', port=9090)
host="54.90.73.9"
port=9090
client = roslibpy.Ros("ws://%s:%d" % (host, port))
client.run()

# move_cmd = Twist()
# move_cmd.linear.x = 1.0
# move_cmd.angular.z = 1.0
speedPub = roslibpy.Topic(client, '/cmd_vel', 'geometry_msgs/Twist', queue_size=10)
talker = roslibpy.Topic(client, '/chatter', 'std_msgs/String', queue_size=10)

dis = 0.1
linear_speed = -0.05
msg = roslibpy.Message({
    'linear':{'x': linear_speed, 'y': 0.0, 'z': 0.0},
    'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}
})

while client.is_connected:
    speedPub.publish(msg)
    talker.publish(roslibpy.Message({'data': 'Hello World!'}))
    print('Sending message...')
    time.sleep(0.0001)

talker.unadvertise()

client.terminate()