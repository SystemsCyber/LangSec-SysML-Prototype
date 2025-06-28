//includes
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/UInt16.h"
#include "beginner_tutorials/Num.h"
#include "beginner_tutorials/J1939.h"
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

//globals 
int nbytes;
int rc;
int sockfd;
struct sockaddr_can addr;
struct ifreq ifr;
struct can_frame frame;

//defines
#define PRIORITY_MASK  0x1C000000
#define EDP_MASK       0x02000000
#define DP_MASK        0x01000000
#define PF_MASK        0x00FF0000
#define PS_MASK        0x0000FF00
#define SA_MASK        0x000000FF
#define PDU1_PGN_MASK  0x03FF0000
#define PDU2_PGN_MASK  0x03FFFF00
#define TP_RTS_CTS     0xEC00
#define TP_DATA        0xEB00
#define BRAKE	       0x0B
#define TRN	       0x03
#define BODY           0x31
#define DIAG	       0xF9

//can initialization
extern "C" void can_initialize()
{
  sockfd = ::socket(PF_CAN, SOCK_RAW, CAN_RAW);
  std::strncpy(ifr.ifr_name, "vcan0", IFNAMSIZ);
  if (::ioctl(sockfd, SIOCGIFINDEX, &ifr) == -1) {}
  addr.can_family = AF_CAN;
  addr.can_ifindex = ifr.ifr_ifindex;
  rc = ::bind(
        sockfd,
        reinterpret_cast<struct sockaddr*>(&addr),
        sizeof(addr)
  );
  frame.can_id |= CAN_EFF_FLAG;
}

//frame encoder
extern "C" void frame_encoder()
{
	frame.can_id = 0x0CF00400 | CAN_EFF_FLAG;
	frame.can_dlc = 8;
	for (int i = 0; i < 8; i++){
		frame.data[i] = 0x00;
	}
}

void sendCallback(const beginner_tutorials::J1939 msg)
{
  //ROS_INFO("I heard: [%hu]" ,msg.data[0]);
  frame.can_id = 0x18000000 | CAN_EFF_FLAG;
  if (msg.pgn == TP_RTS_CTS){
  	frame.can_id += 0x00EC0000;
       	if (msg.da == BRAKE){
		frame.can_id += 0x00000B00;
	}
	else if (msg.da == TRN){
		frame.can_id += 0x00000300;
        }
	else if (msg.da == BODY){
		frame.can_id += 0x00003100;
        }
	else if (msg.da == DIAG){
		frame.can_id += 0x0000F900;
        }
	else{
		frame.can_id += 0x0000FF00;
        }

	for (int i = 0; i<8; i++){
  		frame.data[i] = msg.data[i];
		//ROS_INFO("FRAME 0 [%hu]", frame.data[i]);
  	}	
  	nbytes = write(sockfd, &frame, sizeof(struct can_frame));
   }
  if (msg.pgn == TP_DATA){
        frame.can_id += 0x00EB0000;
        if (msg.da == BRAKE){
                frame.can_id += 0x00000B00;
        }
        else if (msg.da == TRN){
                frame.can_id += 0x00000300;
        }
        else if (msg.da == BODY){
                frame.can_id += 0x00003100;
        }
        else if (msg.da == DIAG){
                frame.can_id += 0x0000F900;
        }
        else{
                frame.can_id += 0x0000FF00;
        }
        for (int i = 0; i<8; i++){
                frame.data[i] = msg.data[i];
        }
        nbytes = write(sockfd, &frame, sizeof(struct can_frame));
   }

}


void dataCallback(const beginner_tutorials::J1939 msg)
{
  //ROS_INFO("I heard: [%hu]" ,msg.data[0]);
  frame.can_id = 0x0CF00400 | CAN_EFF_FLAG;
  for (int i = 0; i<8; i++){
      frame.data[i] = msg.data[i];
  }
  nbytes = write(sockfd, &frame, sizeof(struct can_frame));
}

int main(int argc, char **argv)
{
  //initialize ros
  ros::init(argc, argv, "listener");
  ros::NodeHandle n;
	
  //inilialize can
  can_initialize();

  //configure can frame
  frame_encoder();
  
  //subsribe to ros topic
  ros::Subscriber sub = n.subscribe("transport_processer", 1000, sendCallback);
  ros::Subscriber pub = n.subscribe("command_processer", 1000, dataCallback);
  ros::spin();

  return 0;
}
