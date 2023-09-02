import time
from robot import Robot
from image_app_core import start_server_process, get_control_instruction, put_output_image
import camera_stream


TIMEOUT_IN = 1

class ManualDriveBehavior(object):
    def __init__(self, robot):
        self.robot = robot
        self.last_time = time.time()

    def process_control(self):
        instruction = get_control_instruction()
        while instruction:
            self.last_time = time.time()
            self.handle_instruction(instruction)
            instruction = get_control_instruction()

    def handle_instruction(self, instruction):
        command = instruction['command']
        if command == "set_left":
            self.robot.set_left(int(instruction['speed']))
        elif command == "set_right":
            self.robot.set_right(int(instruction['speed']))
        elif command == "exit":
            print("zatrzymywanie")
            exit()
        else:
            raise ValueError(f"Nieznana instrukcja: {instruction}")

    def make_display(self, frame):
        """Przygotowanie danych do wyświetlenia i umieszczenie ich w kolejce"""
        encoded_bytes = camera_stream.get_encoded_bytes_for_frame(frame)
        put_output_image(encoded_bytes)

    def run(self):
        # Ustawienie mechanizmu uchylno-obrotowego w pozycji środkowej
        self.robot.set_pan(0)
        self.robot.set_tilt(0)
        # Uruchomienie kamery
        camera = camera_stream.setup_camera()
        # Czas na przygotowanie się kamery do pracy i na ruch serwomechanizmów
        time.sleep(0.1)
        # Serwomotory będą na miejscu - na razie zostaną zatrzymane
        self.robot.servos.stop_all()
        print("Kamera została przygotowana do pracy")

        # Pętla główna
        for frame in camera_stream.start_stream(camera):
            self.make_display(frame)
            self.process_control()
            # Automatyczne zatrzymanie
            if time.time() > self.last_time + TIMEOUT_IN:
                self.robot.stop_motors()

print("Uruchamianie")
behavior = ManualDriveBehavior(Robot())
process = start_server_process('manual_drive.html')
try:
    behavior.run()
except:
    process.terminate()
