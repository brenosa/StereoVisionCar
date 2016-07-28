# StereoVisionCar

## Requisites

  - To run this example you must install DroneKit first:
  
  http://python.dronekit.io/guide/quick_start.html#installation
  
  - And python GPIO library:
  
  https://github.com/derekstavis/python-sysfs-gpio

 - Connect the Pixhawk to the Jetson/RPi using the Serial/USB converter cable;

 - Depending on the USB port it is connected, either the USB0 or USB1, be sure to check it and change it in the code, if necessary; the default is USB0.
 
			#Connect to Pixhawk in the specified port

			connectVehicle('/dev/ttyUSB0')
      
## Usage

- Type the following command sequence:

		$screen
		$sudo python RCOveride.py

- After a successful connection, the program will start outputting the distances in the screen, unplug the network cable and arm the vehicle by holding the switch for 5 seconds;

- To stop the vehicle, disarm it by holding the switch for 5 seconds again.


  
  
  
