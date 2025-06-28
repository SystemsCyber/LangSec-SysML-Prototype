//includes
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/UInt16.h"
#include "beginner_tutorials/Num.h"
#include "beginner_tutorials/J1939.h"
//#include "beginner_tutorials/CAN.h"
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <chrono>
#include <linux/can.h>
#include <linux/can/raw.h>
#include <math.h>
#include <unistd.h>
#include <inttypes.h>

//defines
#define PRIORITY_MASK  0x1C000000
#define EDP_MASK       0x02000000
#define DP_MASK        0x01000000
#define PF_MASK        0x00FF0000
#define PS_MASK        0x0000FF00
#define SA_MASK        0x000000FF
#define PDU1_PGN_MASK  0x03FF0000
#define PDU2_PGN_MASK  0x03FFFF00
#define REQUEST        0xEA00
#define TPCM           0xEC00
#define TPDT           0xEB00
#define SIZE           10
#define RTS            0x10
#define CTS            0x11

//globals
uint8_t data[8];
ros::Publisher command_proccesser;

//process command
extern "C" void process_cmd()
{
	data[3] = data[1];
        data[4] = data[2];
	data[0] = 0xFF;
	data[1] = 0xFF;
	data[2] = 0xFF;
        data[5] = 0xFF;
        data[6] = 0xFF;
        data[7] = 0xFF;	
}


void commandCallback(const beginner_tutorials::J1939 msg)
{
	for (int i = 0; i <8; i++){
		data[i] = msg.data[i];
		//ROS_INFO("Data [%hu]", data[i]);
	}
	beginner_tutorials::J1939 msgx;
        msgx.da = 0xFF;
	process_cmd();	
	for (int i = 0; i<8; i++){
		msgx.data[i] = data[i];
	}
	command_proccesser.publish(msgx);
}

int main(int argc, char **argv)
{
  //initialize ros
  ros::init(argc, argv, "command_processer");
  ros::NodeHandle n;
  command_proccesser = n.advertise<beginner_tutorials::J1939>("command_processer", 1000);
  
  //subsribe to ros topic
  ros::Subscriber sub = n.subscribe("command_data", 1000, commandCallback);
  ros::spin();

  return 0;
}

