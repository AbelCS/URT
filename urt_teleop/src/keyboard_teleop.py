#!/usr/bin/env python
# coding=utf-8

""" This ROS Python module is intended for doing keyboard teleop with
    multiple libraries (p2os, rosaria).
"""

__author__ = "Abel Castro Suárez"
__version__ = "0.1"


import curses
import argparse

import rospy
from geometry_msgs.msg import Twist


class KeyboardTeleop():

    def __init__(self):

        _args = self._parse()

        self._topic = str(_args.topic)
        self._linear_speed = float(_args.linear_speed)
        self._angular_speed = float(_args.angular_speed)

        self._cmd_vel = rospy.Publisher(self._topic, Twist)

        self._teleop()

    def _stop_exit(self):
        """Publish stop message and exit"""

        rospy.loginfo("Ending URT keyboard teleop node...")
        self._cmd_vel.publish(Twist())
        rospy.sleep(1)
        curses.nocbreak()
        curses.echo()
        curses.endwin()


    def _teleop(self):
        """"Read inputs from keyboard and publish robot's movement messages"""

        rospy.init_node('urt_keyboard_teleop', anonymous=False)

        rospy.on_shutdown(self._stop_exit)

        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(1)

        stdscr.addstr(0, 0, "Be water my friend...")
        stdscr.refresh()

        nokey = False

        while not rospy.is_shutdown():
            twist = Twist()

            curses.halfdelay(3)
            char = stdscr.getch()

            if char == ord('q'):
                exit()
            elif char == curses.KEY_UP:
                twist.linear.x = self._linear_speed
            elif char == curses.KEY_DOWN:
                twist.linear.x = -self._linear_speed
            elif char == curses.KEY_LEFT:
                twist.angular.z = self._angular_speed
            elif char == curses.KEY_RIGHT:
                twist.angular.z = -self._angular_speed

            if char != curses.ERR:
                self._cmd_vel.publish(twist)
                nokey = False
            elif nokey is False:
                self._cmd_vel.publish(Twist())
                nokey = True

    def _parse(self):
        """Parses input arguments"""

        parser = argparse.ArgumentParser(description="Publish keyboard arrow keys inputs as Twist messages.")
        parser.add_argument("LIBRARY",
                            type=str,
                            help="The name of the library to use for publishing teleop messages.",
                            choices=["p2os", "rosaria"])

        parser.add_argument("-ls", "--linear-speed",
                            type=float,
                            help="Linear speed value in m/s. (Default 0.2)",
                            default=0.2)

        parser.add_argument("-as", "--angular-speed",
                            type=float,
                            help="Angular speed value in m/s. (Default 0.5)",
                            default=0.5)

        args = parser.parse_args()

        if str(args.LIBRARY) == 'p2os':
            args.topic = '/cmd_vel'
        elif str(args.LIBRARY) == 'rosaria':
            args.topic = 'RosAria/cmd_vel'

        return args


if __name__ == '__main__':
    try:
        rospy.loginfo("Stating URT keyboard teleop node...")
        KeyboardTeleop()
    except rospy.ROSInterruptException:
        pass