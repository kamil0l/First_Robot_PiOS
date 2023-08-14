import subprocess

class RobotModes(object):
    """Zachownaia i testy robota jako jego tryby działania"""

    # Słownik, gdzie powiązano nazwę tryby ze skryptem do uruchomienia.
    mode_config = {
        "avoid_behavior": "avoid_with_rainbows.py",
        "circle_head": "circle_pan_tilt_behavior.py",
        "test_leds": "leds_test.py",
        "test_rainbow": "test_rainbow.py",
        "straight_line": "straight_line_drive.py",
        "square": "drive_square.py",
        "line_following": "line_follow_behavior.py",
        "color_track": "color_track_behavior.py",
        "face_track": "face_track_behavior.py",
    }

    def __init__(self):
        self.current_process = None

    def is_running(self):
        """Sprawdzenie, czt jest już uruchomiony jakiś proces. Zmienna returncode jest ustawiana tylko po zakończonym procesie."""
        return self.current_process and self.current_process.returncode is None

    def run(self, mode_name):
        """Uruchom tryb jako podproces, lecz nie rób tego, gdy inny już jest uruchomiony."""
        if not self.is_running():
            script = self.mode_config[mode_name]
            self.current_process = subprocess.Popen(["python3", script])
            return True
        return False

    def stop(self):
        """Zatrzymanie procesu"""
        if self.is_running():
            # Wysyłanie sygnału sigint jest (w systemie Linux) podobne do naciśnięcia Ctrl+C.
            # To powoduje zakończenie procesu i wyczyszczenie wszystkich jego danych.
            self.current_process.send_signal(subprocess.signal.SIGINT)
            self.current_process = None
