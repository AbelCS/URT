## URT Teleop Package

#### keyboard_teleop:

###### Description: 
   Publish keyboard arrow keys inputs as Twist messages.


###### Usage: 
    keyboard_teleop.py [-h] [-ls LINEAR_SPEED] [-as ANGULAR_SPEED] {p2os, rosaria}

    positional arguments:
    {p2os, rosaria}        Library to be used.

    optional arguments:
     -h, --help            show this help message and exit
      -ls LINEAR_SPEED, --linear-speed LINEAR_SPEED
                        Linear speed value in m/s. (Default 0.2)
      -as ANGULAR_SPEED, --angular-speed ANGULAR_SPEED
                        Angular speed value in m/s. (Default 0.5)
