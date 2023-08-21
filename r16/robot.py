from Raspi_MotorHAT import Raspi_MotorHAT
from gpiozero import DistanceSensor

import atexit
import leds_led_shim
from servos import Servos
from encoder_counter import EncoderCounter


class Robot:
    wheel_diameter_mm = 70.0
    ticks_per_revolution = 40.0
    wheel_distance_mm = 132.0

    def __init__(self, motorhat_addr=0x6f):
        # Inicjalizacja nakładki sterownika silników znajdującym się pod podanym adresem
        self._mh = Raspi_MotorHAT(addr=motorhat_addr)

        self.left_motor = self._mh.getMotor(1)
        self.right_motor = self._mh.getMotor(2)

        # Inicjalizacja paska LED
        self.leds = leds_led_shim.Leds()
        # Set up servo motors for pan and tilt.
        self.servos = Servos(addr=motorhat_addr)

        # Inicjalizacja czujników odległości
        self.left_distance_sensor = DistanceSensor(echo=17, trigger=27, queue_len=2)
        self.right_distance_sensor = DistanceSensor(echo=5, trigger=6, queue_len=2)

        # Inicjalizacja enkoderów
        EncoderCounter.set_constants(self.wheel_diameter_mm, self.ticks_per_revolution)
        self.left_encoder = EncoderCounter(4)
        self.right_encoder = EncoderCounter(26)

        # Upewnienie się, że silniki się zatrzymają, gdy program przestanie działać
        atexit.register(self.stop_all)

    def convert_speed(self, speed):
        # Wybór trybu jazdy
        mode = Raspi_MotorHAT.RELEASE
        if speed > 0:
            mode = Raspi_MotorHAT.FORWARD
        elif speed < 0:
            mode = Raspi_MotorHAT.BACKWARD

        # Przeskalowanie prędkości
        output_speed = (abs(speed) * 255) // 100
        return mode, int(output_speed)

    def set_left(self, speed):
        mode, output_speed = self.convert_speed(speed)
        self.left_motor.setSpeed(output_speed)
        self.left_motor.run(mode)

    def set_right(self, speed):
        mode, output_speed = self.convert_speed(speed)
        self.right_motor.setSpeed(output_speed)
        self.right_motor.run(mode)

    def stop_motors(self):
        self.left_motor.run(Raspi_MotorHAT.RELEASE)
        self.right_motor.run(Raspi_MotorHAT.RELEASE)

    def stop_all(self):
        self.stop_motors()

        # Wygaszenie wyświetlacza
        self.leds.clear()
        self.leds.show()

        # Zatrzymanie obsługi czujników
        self.left_encoder.stop()
        self.right_encoder.stop()

        # Reset serwomotorów
        self.servos.stop_all()

    def set_pan(self, angle):
        self.servos.set_servo_angle(1, angle)

    def set_tilt(self, angle):
        self.servos.set_servo_angle(0, angle)

