import time

from image_app_core import start_server_process, get_control_instruction, put_output_image

import cv2
import numpy as np

import camera_stream
from pid_controller import PIController
from robot import Robot


class LineFollowingBehavior:
    def __init__(self, robot):
        self.robot = robot
        self.check_row = 180
        self.diff_threshold = 10
        self.center = 160
        self.running = False
        self.speed = 60
        # self.last_error = 0
        # self.last_value = 0
        # kolory
        self.crosshair_color = [0, 255, 0]  # zielony
        self.line_middle_color = [128, 128, 255]  # czerwony
        self.graph_color = [255, 128, 128]  # niebieski
        # self.text_color = [50, 255, 50] # jasno zielony
        # self.text_font = cv2.FONT_HERSHEY_SIMPLEX

    def process_control(self):
        instruction = get_control_instruction()
        if instruction:
            command = instruction['command']
            if command == "start":
                self.running = True
            elif command == "stop":
                self.running = False
            if command == "exit":
                print("Zamykanie")
                exit()


    def run(self):
        self.robot.set_pan(0)
        self.robot.set_tilt(90)
        camera = camera_stream.setup_camera()
        direction_pid = PIController(proportional_constant=0.4,
                                     integral_constant=0.01, windup_limit=400)

        time.sleep(1)
        self.robot.servos.stop_all()
        print("Konfiguracja zakończona")
        last_time = time.time()
        for frame in camera_stream.start_stream(camera):
            x, magnitude = self.process_frame(frame)
            self.process_control()
            if self.running and magnitude > self.diff_threshold:
                direction_error = self.center - x
                new_time = time.time()
                dt = new_time - last_time
                direction_value = direction_pid.get_value(direction_error, delta_time=dt)
                last_time = new_time

                print(f"Uchyb: {direction_error}, Wartość:{direction_value:2f}, czas: {new_time}")
                # self.last_error = direction_error
                # self.last_value = direction_value
                # speed = self.speed
                # speed -= abs(direction_value) / 3
                self.robot.set_left(self.speed - direction_value)
                self.robot.set_right(self.speed + direction_value)
            else:
                self.robot.stop_motors()
                self.running = False
                direction_pid.reset()
                last_time = time.time()

    def make_cv2_simple_graph(self, frame, data):
        last = data[0]
        graph_middle = 100
        for x, item in enumerate(data):
            cv2.line(frame, (x, last + graph_middle), (x + 1, item + graph_middle), self.graph_color)
            last = item

    def make_display(self, frame, middle, lowest, highest, diff): #, mag):
        # Najpierw na wykres nanosimy odniesienie do środka.
        cv2.line(frame, (self.center - 4, self.check_row), (self.center + 4, self.check_row), self.crosshair_color)
        cv2.line(frame, (self.center, self.check_row - 4), (self.center, self.check_row + 4), self.crosshair_color)
        # Teraz pokażemy, gdzie znaleźliśmy środek.
        cv2.line(frame, (middle, self.check_row - 8), (middle, self.check_row + 8), self.line_middle_color)
        # Następnie nanosimy krawędzie.
        cv2.line(frame, (lowest, self.check_row - 4), (lowest, self.check_row + 4), self.line_middle_color)
        cv2.line(frame, (highest, self.check_row - 4), (highest, self.check_row + 4), self.line_middle_color)
        # W końcu rysujmey wykres.
        graph_frame = np.zeros((camera_stream.size[1], camera_stream.size[0], 3), np.uint8)
        self.make_cv2_simple_graph(graph_frame, diff)
        # cv2.putText(graph_frame, f"Uchyb: {self.last_error}", org=(0, 120), fontFace=self.text_font, fontScale=1, color=self.text_color)
        # cv2.putText(graph_frame, f"Wartość: {self.last_value}", org=(0, 160), fontFace=self.text_font, fontScale=1, color=self.text_color)
        # cv2.putText(graph_frame, f"Wielkość: {mag}", org=(0, 200), fontFace=self.text_font, fontScale=1, color=self.text_color)
        # Połączenie klatki i wykresu w jeden obraz
        display_frame = np.concatenate((frame, graph_frame), axis=1)
        encoded_bytes = camera_stream.get_encoded_bytes_for_frame(display_frame)
        put_output_image(encoded_bytes)

    def process_frame(self, frame):
        # Zmiana na odcienie szarości
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Małe rozmycie w celu uniknięcia szumów
        blur = cv2.blur(gray, (5, 5))
        # Wybranie jednego wiersza i zamiana jego danych na 32-bitowe liczy całkowite ze znakiem, by można było wyznaczyć ujemne szczyty
        row = blur[self.check_row].astype(np.int32)
        # Obliczenie dyskretnej różnicy
        diff = np.diff(row)
        max_d = np.amax(diff, 0)
        min_d = np.amin(diff, 0)
        # Jeśli otrzymana wartość minimalna nie jest mniejsza od zera, a maksymalna więsza, to znaczy, że to nie jest linia.
        if max_d < 0 or min_d > 0:
            return 0, 0
        # Znalezienie pozycji minimum i maksimum
        highest = np.where(diff == max_d)[0][0]
        lowest = np.where(diff == min_d)[0][0]
        # Współrzędna x środka linii
        middle = (highest + lowest) // 2
        # Wielkość różnicy między różnicą minimalną a maksymalną
        mag = max_d - min_d
        # Wyświetlenie
        self.make_display(frame, middle, lowest, highest, diff) #, mag)
        return middle, mag

print("Uruchamianie")
behavior = LineFollowingBehavior(Robot())
process = start_server_process('color_track_behavior.html')
try:
    behavior.run()
finally:
    process.terminate()
