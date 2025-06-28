//includes
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/UInt16.h"
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
#include <signal.h>
#include "beginner_tutorials/J1939.h"
#include "beginner_tutorials/Num.h"

//globals 
int nbytes;
int rc;
int sockfd;
struct sockaddr_can addr;
struct ifreq ifr;
struct can_frame frame;
int pf, ps;
uint8_t priority;
uint8_t da, sa;
uint32_t pgn;
//uint64_t rq_pgn[100];
//int cnt;


//defines
#define PRIORITY_MASK  0x1C000000
#define EDP_MASK       0x02000000
#define DP_MASK        0x01000000
#define PF_MASK        0x00FF0000
#define PS_MASK        0x0000FF00
#define SA_MASK        0x000000FF
#define PDU1_PGN_MASK  0x03FF0000
#define PDU2_PGN_MASK  0x03FFFF00
#define TSC1	       0x0000
#define TPCM_RTS_CTS   0xEC00
#define TPCM_BAM       0xEB00
#define REQUEST        0xEA00
#define ENGINE         0x00
#define BRAKE          0x0B
#define TRANSMISSION   0x03
#define DIAG           0xF9
#define BODY           0x31


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
}

//decode can frame
extern "C" void decode_j1939()
{
    priority = (PRIORITY_MASK & frame.can_id) >> 26;
    pf = (PF_MASK & frame.can_id) >> 16;
    ps = (PS_MASK & frame.can_id) >> 8;
    if (pf >= 0xF0) {
        da = 255;
        pgn = (frame.can_id & PDU2_PGN_MASK) >> 8;
    } else {
        da = ps;
        pgn = (frame.can_id & PDU1_PGN_MASK) >> 8;
    }
    sa = (frame.can_id & SA_MASK);
}



//void rq_handler()
//{
//  rq_pgn[cnt]  = (frame.data[2] << 16) + (frame.data[1] << 8) + frame.data[0];
  //ROS_INFO("Requested PGN : %l", rq_pgn[cnt]);
//  cnt = cnt + 1;
//}


//ISR
void sighandler(int signum) {
   exit(1);
}

int main(int argc, char **argv)
{
  using namespace std::chrono_literals;

  //ros initialization
  ros::init(argc, argv, "talker");
  ros::NodeHandle n;
  ros::Publisher transport_pub = n.advertise<beginner_tutorials::J1939>("transport_data", 1000);
  ros::Publisher command_pub = n.advertise<beginner_tutorials::J1939>("command_data", 1000);
  ros::Publisher periodic_pub = n.advertise<beginner_tutorials::J1939>("periodic_data", 1000);
  ros::Rate loop_rate(1000);
  ROS_INFO("ROS Initialized");
  

  //can initilization
  can_initialize();
  ROS_INFO("SOCKET INITIALIZED");

  int count = 0;
  //read can messages
  while (ros::ok())
  {
      signal(SIGINT, sighandler);
      beginner_tutorials::J1939 msg;
      nbytes = ::read(sockfd, &frame, sizeof(struct can_frame));
      decode_j1939();
      msg.pgn = pgn;
      msg.sa = sa;
      for (int i = 0; i<8; i++){
	      msg.data[i] = frame.data[i];
      }
      if (pgn == TSC1 && sa == BRAKE && da == ENGINE)
      {    
      	command_pub.publish(msg);
      }
      else if (pgn == REQUEST || pgn == TPCM_RTS_CTS && da == ENGINE)
      {
	//ROS_INFO("Got Transport message");
        transport_pub.publish(msg);
      }
      else{
	periodic_pub.publish(msg);
      }
    ros::spinOnce();
    loop_rate.sleep();
  }
  return 0;
}

