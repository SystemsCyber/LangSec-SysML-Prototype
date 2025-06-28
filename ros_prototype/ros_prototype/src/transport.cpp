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
#define SIZE           100
#define RTS            0x10
#define CTS            0x11

//globals
uint8_t data[8];
int tp_start = 0;
uint32_t rq_queue[SIZE];
int front = -1;
int rear = -1;
ros::Publisher transport_proccesser;

//enqueue()
extern "C" void enqueue()
{
   	//if (rear == SIZE -1){ return;}
        if (front == - 1)
        front = 0;
        rear = rear + 1;
	uint32_t rq_pgn = (data[2] << 16) + data[1] << 8 + data[0];
        rq_queue[rear] = rq_pgn;
	//ROS_INFO("REAR POS : [%d]", rear);
}


//dequeue()
extern "C" void dequeue()
{
    if (front == - 1 || front > rear)
    {
        return ;
    }
    else
    {
        for (int i = 0; i <= rear; i++){
		uint32_t temp = rq_queue[i+1];
		rq_queue[i] = temp;
	}
	rear = rear - 1;
    }
}

//process request
extern "C" void process_rq()
{
	enqueue();
	data[5] = data[0];
        data[6] = data[1];
        data[7] = data[2];
	data[0] = 0x10;
	data[1] = 0x15;
	data[2] = 0x00;
	data[3] = 0x03;
	data[4] = 0xFF; 
}

//frame encoder
extern "C" void process_tp()
{
	if (data[0] == 0x10){
		tp_start = 2;
	}
	else if(data[0] == 0x11){
		tp_start = 1;		
	}
	else{
		tp_start = 0;
	}

}

void timerCallback(const ros::TimerEvent& event)
{
	//ROS_INFO("Dequed Request");
	dequeue();
        //ROS_INFO("Processed Request");

}
void transportCallback(const beginner_tutorials::J1939 msg)
{
	for (int i = 0; i <8; i++){
		data[i] = msg.data[i];
		//ROS_INFO("Data [%hu]", data[i]);
	}
	beginner_tutorials::J1939 msgx;
        msgx.da = msg.sa;	
	if (msg.pgn == REQUEST){
		ROS_INFO("Got Request");
		process_rq();
		//ROS_INFO("Processed Request");
		msgx.pgn = TPCM;
		for (int i = 0; i<8; i++){
			msgx.data[i] = data[i];
			//ROS_INFO("%hu", msgx.data[i]);
		}
		transport_proccesser.publish(msgx);
		for (int i=0; i<8; i++){
			data[i] = 0x00;
		}

	}
	//for (int i = 0; i <8; i++){
        //        data[i] = msg.data[i];
        //        ROS_INFO("Data [%hu]", data[i]);
        //}

	if (msg.pgn == TPCM){
		process_tp();
		//ROS_INFO("Data 0: [%hu]",data[0]);
		if (tp_start == 1){
			ROS_INFO("Got CTS");
			msgx.pgn = 0xEB00;
                        for (int i = 0; i < 3; i++){
                                msgx.data[0] = i;
                                for (int i = 1; i < 8; i++){
                                        data[i] = 0xFF;
					msgx.data[i] = data[i];
                                }
                                transport_proccesser.publish(msgx);
                        }
                        tp_start = 0;
		}
		else if (tp_start == 2){
			ROS_INFO("Got RTS");
			msgx.pgn = TPCM;
			data[5] = data[0];
                	data[6] = data[1];
                	data[7] = data[2];
                	data[0] = 0x11;
                	data[1] = data[5];
                	data[2] = 0x01;
                	data[3] = 0xFF;
                	data[4] = 0xFF;
			for (int i = 0; i < 8; i++){
				msgx.data[i] = data[i];
			}
			transport_proccesser.publish(msgx);
			tp_start = 0;
		}
		else{
			ROS_INFO("Invalid Message");
		}
		for (int i = 0; i<8; i++){
			data[i] = 0x00;
		}
	}
}

int main(int argc, char **argv)
{
  //initialize ros
  ros::init(argc, argv, "transport_processer");
  ros::NodeHandle n;
  transport_proccesser = n.advertise<beginner_tutorials::J1939>("transport_processer", 1000);
  
  //subsribe to ros topic
  ros::Subscriber sub = n.subscribe("transport_data", 1000, transportCallback);
  ros::Timer timer = n.createTimer(ros::Duration(0.001), timerCallback);
  ros::spin();

  return 0;
}

