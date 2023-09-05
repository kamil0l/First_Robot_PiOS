import time

from image_app_core import start_server_process, get_control_instruction, put_output_image

import cv2
import os

import camera_stream
from pid_controller import PIController
from robot import Robot

class FaceTrackBehavior:
    """Zachowanie polegające na znalezieniu twarzy i skierowanie się w jej stronę"""
    def __init__(self, robot):
        self.robot = robot
        cascade_path = "/usr/local/lib/python3.7/dist-packages/cv2/data/haarcascade_frontalface_default.xml"
        assert os.path.exists(cascade_path), f"Plik {cascade_path} nie istnieje w podanej lokalizacji"
        self.cascade = cv2.CascadeClassifier(cascade_path)
        # Wartośći regulujące działanie zachowania
        self.center_x = 160
        self.center_y = 120
        self.min_size = 20
        self.pan_pid = PIController(proportional_constant=0.1, integral_constant=0.03)
        self.tilt_pid = PIController(proportional_constant=-0.1, integral_constant=-0.03)
        # Stan aktualny
        self.running = False

    def process_control(self):
        instruction = get_control_instruction()
        if instruction:
            command = instruction['command']
            if command == "start":
                self.running = True
            elif command == "stop":
                self.running = False
                self.pan_pid.reset()
                self.tilt_pid.reset()
                self.robot.servos.stop_all()
            elif command == "exit":
                print("Zamykanie")
                exit()

    def find_object(self, original_frame):
        """Szukanie obiektu na klatce i zwrócenie prostokąta o największym polu (szerokość (w) * wysokość(h))"""
        gray_img = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
        objects = self.cascade.detectMultiScale(gray_img)
        largest = 0, (0, 0, 0, 0)  # pole, x, y, szerokość (w), wysokość(h)
        for (x, y, w, h) in objects:
            item_area = w * h
            if item_area > largest[0]:
                largest = item_area, (x, y, w, h)
        return largest[1]

    def make_display(self, display_frame):
        encoded_bytes = camera_stream.get_encoded_bytes_for_frame(display_frame)
        put_output_image(encoded_bytes)

    def process_frame(self, frame):
        (x, y, w, h) = self.find_object(frame)
        cv2.rectangle(frame, (x, y), (x + w, y + w), [255, 0, 0])
        self.make_display(frame)
        return x, y, w, h

    def run(self):
        camera = camera_stream.setup_camera()
        time.sleep(0.1)
        print("Konfiguracja zakończona")
        for frame in camera_stream.start_stream(camera):
            (x, y, w, h) = self.process_frame(frame)
            self.process_control()
            if self.running and h > self.min_size:
                pan_error = self.center_x - (x + (w / 2))
                pan_value = self.pan_pid.get_value(pan_error)
                self.robot.set_pan(int(pan_value))
                tilt_error = self.center_y - (y + (h /2))
                tilt_value = self.tilt_pid.get_value(tilt_error)
                self.robot.set_tilt(int(tilt_value))
                print(f"x: {x}, y: {y}, uchyb orbotu: {pan_error}, uchyb nachylenia: {tilt_error}, wartość obrotu: {pan_value:.2f}, wartość nachylenia: {tilt_value:.2f}")

print("Uruchamianie")
behavior = FaceTrackBehavior(Robot())
process = start_server_process('color_track_behavior.html')
try:
    behavior.run()
finally:
    process.terminate()
