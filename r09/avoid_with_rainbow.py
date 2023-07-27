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

    def distance_to_led_bar(self, distance):
        # Odwrócenie wartości, tak aby mniejsza odległość przekładała się na większą liczbę diod.
        inverted = max(0, 1.0 - distance)
        led_bar = int(round(inverted * self.led_half)) + 1
        return led_bar

    def display_state(self, left_distance, right_distance):
        # Zgaszenie wszystkich diod LED
        self.robot.leds.clear()
        # Lewa strona
        led_bar = self.distance_to_led_bar(left_distance)
        show_rainbow(self.robot.leds, range(led_bar))
        # Prawa strona
        led_bar = self.distance_to_led_bar(right_distance)
        # Bardziej skomplikowane - zakres diod musi zaczynać się od adresu osatatniej diody w słupku do adresu ostatniej diody w pasku LED.
        start = (self.robot.leds.count - 1) - (led_bar)
        right_range = range(self.robot.leds.count - 1, start, -1)
        show_rainbow(self.robot.leds, right_range)
        # Zapalenie ustawionych diod LED
        self.robot.leds.show()