from robot import Robot
from time import sleep

class ObstacleAvoidingBehavior:
    """Proste unikanie przeszkód"""
    def __init__(self, the_robot):
        self.robot = the_robot
        self.speed = 60
        # Obliczenie liczby diod dla słupków
        self.led_half = int(self.robot.leds.count/2)
        print(self.led_half)
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
        # print(led_bar)
        self.robot.leds.set_range(range(led_bar), self.sense_colour)
        # Prawa strona
        led_bar = self.distance_to_led_bar(right_distance)
        # Bardziej skomplikowane - zakres diod musi zaczynać się od adresu osatatniej diody w słupku do adresu ostatniej diody w pasku LED.
        start = (self.robot.leds.count - 1) - led_bar
        self.robot.leds.set_range(range(start, self.robot.leds.count - 1), self.sense_colour)
        # Zapalenie ustawionych diod LED
        self.robot.leds.show()

    def get_speeds(self, nearest_distance):
        if nearest_distance >= 1.0:
            nearest_speed = self.speed
            furthest_speed = self.speed
            delay = 100
        elif nearest_distance > 0.5:
            nearest_speed = self.speed
            furthest_speed = self.speed * 0.8
            delay = 100
        elif nearest_distance > 0.2:
            nearest_speed = self.speed
            furthest_speed = self.speed * 0.6
            delay = 100
        elif nearest_distance > 0.1:
            nearest_speed = -self.speed * 0.4
            furthest_speed = -self.speed
            delay = 100
        else: # Kolizja
            nearest_speed = -self.speed
            furthest_speed = -self.speed
            delay = 250
        return nearest_speed, furthest_speed, delay

    def run(self):
        while True:
            # Odczytanie odległości podanej w metrach
            left_distance = self.robot.left_distance_sensor.distance
            right_distance = self.robot.right_distance_sensor.distance
            # Wyświetlenie odczytów z czujników
            self.display_state(left_distance, right_distance)
            # Ustalenie prędkości silników na podstawie odległości
            nearest_speed, furthest_speed, delay = self.get_speeds(min(left_distance, right_distance))
            print(f"Distances: l {left_distance:.2f}, r {right_distance:.2f}. Speeds: n: {nearest_speed}, f: {furthest_speed}. Delay: {delay}")
            # i ruch robota
            # Ustawienie prędkości silników
            if left_distance < right_distance:
                self.robot.set_left(nearest_speed)
                self.robot.set_right(furthest_speed)
            else:
                self.robot.set_right(nearest_speed)
                self.robot.set_left(furthest_speed)
            # Zatrzymanie programu na czas określony przez zmienną delay
            sleep(delay * 0.001)


bot = Robot()
behavior = ObstacleAvoidingBehavior(bot)
behavior.run()

