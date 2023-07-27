from robot import Robot
from time import sleep
from led_rainbow import show_rainbow


class ObstacleAvoidingBehavior:
    """Simple obstacle avoiding"""
    def __init__(self, the_robot):
        self.robot = the_robot
        self.speed = 60
        # Obliczenie liczby diod dla słupków
        self.led_half = int(self.robot.leds.count/2)
        self.sense_colour = 255, 0, 0