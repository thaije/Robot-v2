## How to ROS
- Topic: node publishes messages, node subscribed to a topic can receive these messages
- Services: A client node sends a request (what is 2+1?) to a Service node, the service node sends a response(2+1=3) back to the client
- Parameters: rosparam can be used to set, get, load, dump, delete and list parameters (e.g. intialization paramters).

### Topic publisher / Subscriber
- copy listener and talker from beginner_tutorials/scripts
- chmod +x file_name.py (for both files)
- roscore
- rosrun package_name listener.py/talker.py or listener/talker(for cpp)
