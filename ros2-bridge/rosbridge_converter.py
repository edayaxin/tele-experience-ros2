from __future__ import print_function
import roslibpy
from geometry_msgs.msg import Twist 
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Joy

host='54.90.73.9'
port=9090
client = roslibpy.Ros("ws://%s:%d" % (host, port))
# if (client.is_connected): 
#     client.run()
# else: 
#     print("ros bridge not connected")
client.run()

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('speedPublisher')
        self.publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.speed = Twist()
        timer_period = 0.1 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

        # listen from ros bridge
        #{'linear': {'x': -1.0, 'y': 0.0, 'z': 0.0}, 'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}}
        self.rosbridgeSub = roslibpy.Topic(client, '/rosbridge_msg', 'std_msgs/String')
        self.rosbridgeSub.subscribe(lambda message: self.rosbridge_callback(message)) 

        # listen from joystick
        self.joySub = self.create_subscription(Joy, '/joy', self.joy_callback, 10)
        self.joySub

    def timer_callback(self):
        self.speed.linear.x = round(self.speed.linear.x, 4)
        self.speed.angular.z = round(self.speed.angular.z, 4)

        if (self.speed.linear.x >= 0.26): self.speed.linear.x = 0.26
        if (self.speed.linear.x <= -0.26): self.speed.linear.x = -0.26

        if (self.speed.angular.z >= 1): self.speed.angular.z = 0.7
        if (self.speed.angular.z <= -1): self.speed.angular.z = -0.7

        self.publisher.publish(self.speed)
        # self.get_logger().info('Publishing cmd_vel: "%s"' % self.speed)
        self.i += 1

    # remote control (joystick or keyboard) callback
    def rosbridge_callback(self, message):
        print("receiving ros bridege", message)
        if (message['data'] == "left_cmd"):
            self.move_left_cmd()
        if (message['data'] == "right_cmd"):
            self.move_right_cmd()
        if (message['data'] == "forward_cmd"):
            self.move_forward_cmd()
        if (message['data'] == "backward_cmd"):
            self.move_backward_cmd()
        if (message['data'] == "left_joy"):
            self.move_left()
        if (message['data'] == "right_joy"):
            self.move_right()
        if (message['data'] == "forward_joy"):
            self.move_forward()
        if (message['data'] == "backward_joy"):
            self.move_backward()
        if (message['data'] == "stop"):
            self.stop()
        if (message['data'] == "left_slow"):
            self.move_left_slow()
        if (message['data'] == "right_slow"):
            self.move_right_slow()
    
    def move_left(self):
        self.get_logger().info('Go left %f' % self.speed.angular.z )
        self.speed.angular.z = min(self.speed.angular.z + 0.05, 1)
    def move_right(self):
        self.get_logger().info('Go right %f' % self.speed.angular.z )
        self.speed.angular.z = max(self.speed.angular.z - 0.05, -1)
    def move_forward(self):
        self.get_logger().info('Go forward %f' % self.speed.linear.x)
        self.speed.linear.x = min(self.speed.linear.x + 0.01, 0.26)
    def move_backward(self):
        self.get_logger().info('Go backward %f' % self.speed.linear.x)
        self.speed.linear.x = max(self.speed.linear.x - 0.01, -0.26)

    def move_left_slow(self):
        self.get_logger().info('Go left slow %f' % self.speed.angular.z )
        self.speed.angular.z = min(self.speed.angular.z + 0.01, 0.7)

    def move_right_slow(self):
        self.get_logger().info('Go right slow %f' % self.speed.angular.z )
        self.speed.angular.z = max(self.speed.angular.z - 0.01, -0.7)

    def move_left_cmd(self):
        # self.speed.linear.x = 0
        self.speed.angular.z = 0.1
    def move_right_cmd(self):
        # self.speed.linear.x = 0
        self.speed.angular.z = -0.1
    def move_forward_cmd(self):
        self.speed.angular.z = 0
        self.speed.linear.x = 0.05
    def move_backward_cmd(self):
        self.speed.angular.z = 0
        self.speed.linear.x = -0.05

    def stop(self):
        self.speed = Twist()

    # Local joystick callback
    def joy_callback(self, message):
        if (message.axes[6] == 1): 
            self.move_left()
        if (message.axes[6] == -1):
            self.move_right()
            self.get_logger().info('Joystick pressed: right %f' % self.speed.angular.z)
        if (message.axes[7] == 1): 
            self.move_forward()
            self.get_logger().info('Joystick pressed: up %s' % message)
        if (message.axes[7] == -1):
            self.move_backward()
            self.get_logger().info('Joystick pressed: down %s' % message)
            
        if (message.buttons[7] == 1 or message.buttons[9] == 1): #right buttons edge
            self.get_logger().info('Joystick pressed: stop %s' % message.buttons)
            self.stop()
            
        if (message.buttons[3] == 1):  
            self.get_logger().info('Joystick pressed: left slow %s' % message.buttons)
            self.move_left_slow()
        if (message.buttons[1] == 1):  
            self.get_logger().info('Joystick pressed: right slow %s' % message.buttons)
            self.move_right_slow()
            
rclpy.init()
speedPublisher = MinimalPublisher()
rclpy.spin(speedPublisher)
speedPublisher.destroy_node()
rclpy.shutdown()

try:
    while True:
        pass
except KeyboardInterrupt:
    client.terminate()