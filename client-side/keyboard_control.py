import roslibpy
import time
from pynput import keyboard

# use ros for joystick comm
host = "54.90.73.9"
port = 9090
ros = roslibpy.Ros("ws://%s:%d" % (host, port))
if (ros.is_connected): print("ros bridge connected for keyboard event")
if (ros.is_connecting): print("ros bridge connecting for keyboard event")
ros.run()

rosbridge_pub = roslibpy.Topic(ros, '/rosbridge_msg', 'std_msgs/String', queue_size=10)

### keyboard control ####
def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
        if (key.char == "w"):
            rosbridge_pub.publish(roslibpy.Message({'data': 'forward_joy'}))
        if (key.char == "x"):
            rosbridge_pub.publish(roslibpy.Message({'data': 'backward_joy'}))
        if (key.char == "a"):
            rosbridge_pub.publish(roslibpy.Message({'data': 'left_joy'}))
        if (key.char == "d"):
            rosbridge_pub.publish(roslibpy.Message({'data': 'right_joy'}))
        if (key.char == "`"):
            print("pressed stop")
            rosbridge_pub.publish(roslibpy.Message({'data': 'stop'}))
            
        
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
        if (str(key) == "Key.up"):
            print('pressed key up')
            rosbridge_pub.publish(roslibpy.Message({'data': 'forward_joy'}))
        if (str(key) == "Key.down"):
            print('pressed key down')
            rosbridge_pub.publish(roslibpy.Message({'data': 'backward_joy'}))
        if (str(key) == "Key.left"):
            print('pressed key left')
            rosbridge_pub.publish(roslibpy.Message({'data': 'left_joy'}))
        if (str(key) == "Key.right"):
            print('pressed key right')
            rosbridge_pub.publish(roslibpy.Message({'data': 'right_joy'}))

 
# ros = roslibpy.Ros(host='localhost', port=9090)
with keyboard.Listener(on_press=on_press,) as listener:
    listener.join()

rosbridge_pub.unadvertise()
ros.terminate()
print(ros.is_connected)