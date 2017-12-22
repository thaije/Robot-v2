#include "ros/ros.h"
#include <ros/time.h>
#include <sensor_msgs/Range.h>

#include <sstream>

// Distance = speed * Time/2
// speed of sound at sea level = 343m/s
// Thus, distance(cm) = 17150 * Time (s)

// ros::NodeHandle nh;

#define echoPin 7
#define trigPin 8

int maximumRange = 360;
int minimumRange = 0;
long duration, distance; // duration used to calc distance


sensor_msgs::Range range_msg;
// ros::Publisher pub_range( "/ultrasoundHead", &range_msg);

char frameid[] = "/ultrasoundHead";

void setup() {
    range_msg.radiation_type = sensor_msgs::Range::ULTRASOUND;
    range_msg.header.frame_id = frameid;
    range_msg.field_of_view = 0.1; // fake
    range_msg.min_range = 0.0;
    range_msg.max_range = maximumRange;

    // pinMode(trigPin, OUTPUT);
    // pinMode(echoPin, INPUT);
}

float getRange_Ultrasound() {
    int val = 0;

    for(int i=0; i<4; i++) {
        // digitalWrite(trigPin, LOW);
        // delayMicroseconds(2);
        //
        // digitalWrite(trigPin, HIGH);
        // delayMicroseconds(10);
        //
        // digitalWrite(trigPin, LOW);
        // duration = pulseIn(echoPin, HIGH);
        duration = 0.001;

        // calc distance in cm based on the speed of sound
        val += duration;
    }

    return val / 232.8;
}


/**
 * This tutorial demonstrates simple sending of messages over the ROS system.
 */
int main(int argc, char **argv)
{

    ros::init(argc, argv, "talker");

    ros::NodeHandle n;
    ros::Publisher chatter_pub = n.advertise<sensor_msgs::Range>("chatter", 1000);
    ros::Rate loop_rate(10);

    // setup the ultrasonic sensors
    setup();

    int count = 0;
    while (ros::ok())
    {
        // get current distance measurement
        range_msg.range = getRange_Ultrasound();
        range_msg.header.stamp = ros::Time::now();

        // print it for debugging
        ROS_INFO("Ultrasonic: stamp %6.4f, distance %f", range_msg.header.stamp.toSec(), range_msg.range);

        // send the data
        chatter_pub.publish(range_msg);

        // wait for next loop
        ros::spinOnce();
        loop_rate.sleep();
        ++count;
  }


  return 0;
}
