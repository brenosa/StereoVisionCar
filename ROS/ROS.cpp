#include "rosAPI.h"

int goTo(int direction , int orientation, int speed){
	
	
}

int emergencyStop(){
	int cmd;
	cmd = system ("rostopic pub -l /mavros/rc/override mavros_msgs/OverrideRCIn '[1500, CHAN_NOCHANGE, 1500, CHAN_NOCHANGE, CHAN_NOCHANGE, CHAN_NOCHANGE, CHAN_NOCHANGE, CHAN_NOCHANGE]'")
	
}

int smoothStop(){
	
	
}

int changeMode(int mode){	
	std::string const command = std::string( "rosrun mavros mavsys mode -c" ) + mode;
	system( command.c_str() );
}

int arm(){
	int cmd;
	cmd = system("rosrun mavros mavsafety arm");	
	printf("Return: %i",&cmd);
	if(cmd == 0)	\
		printf("ARMED!");
	else
		printf("FAILED TO ARM");
}

int disarm(){
	int cmd;
	cmd = system("rosrun mavros mavsafety disarm");	
	printf("Return: %i",&cmd);
	if(cmd == 0)	\
		printf("DISARMED!");
	else
		printf("FAILED TO DISARM");
	
}

int connect(){
	int comd;
	cmd = system("roslaunch mavros apm2.launch");
	printf("Return: %i",&cmd);
	if(cmd == 0)	\
		printf("CONNECTED!");
	else
		printf("FAILED TO CONNECT");
	
}

int disconnect(){
	
	
}

int status(){
	int cmd;
	cmd = system("rostopic echo  /mavros/state");
	printf("Return: %i",&cmd);
	if(cmd == 0)	\
		printf("STATUS!");
	else
		printf("NO STATUS");
	
}
