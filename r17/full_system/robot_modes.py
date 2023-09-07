import subprocess

class RobotModes(object):
    """Zachownaia i testy robota jako jego tryby działania"""

    # Słownik, gdzie powiązano nazwę tryby ze skryptem do uruchomienia.
    mode_config = {
        "avoid_behavior": {"script": "avoid_behavior.py"},
        "circle_head": {"script": "circle_pan_tilt_behavior.py"},
        "test_rainbow": {"script": "test_rainbow.py"},
        "test_leds": {"script": "leds_test.py"},
        "line_following": {"script": "line_follow_behavior.py", "server": True},
        "color_track": {"script": "color_track_behavior.py", "server": True},
        "face_track": {"script": "face_track_behavior.py", "server": True},
        "manual_drive": {"script": "manual_drive.py", "server": True},
        "behavior_line": {"script": "straight_line_drive.py"},
        "drive_north": {"script": "drive_north.py"}
    }

    menu_config = [
        {"mode_name": "avoid_behavior", "text": "Unikanie przeszkód"},
        {"mode_name": "circle_head", "text": "Kręcenie głową"},
        {"mode_name": "test_rainbow", "text": "Tęcza z diod LED"},
        {"mode_name": "test_leds", "text": "Test diod LED"},
        {"mode_name": "line_following", "text": "Śledzenie linii"},
        {"mode_name": "color_track", "text": "Podążanie za kolorem"},
        {"mode_name": "face_track", "text": "Podążanie za twarzą"},
        {"mode_name": "manual_drive", "text": "Ręczne sterowanie"},
        {"mode_name": "behavior_line", "text": "Jazda po linii prostej"},
        {"mode_name": "drive_north", "text": "Jazda na północ"}
    ]

    def __init__(self):
        self.current_process = None

    def is_running(self):
        """Sprawdzenie, czy jest już uruchomiony jakiś proces. Zmienna returncode jest ustawiana tylko po zakończonym procesie."""
        return self.current_process and self.current_process.returncode is None

    def run(self, mode_name):
        """Uruchom tryb jako podproces, lecz nie rób tego, gdy inny już jest uruchomiony."""
        while self.is_running():
            self.stop()

        script = self.mode_config[mode_name]['script']
        self.current_process = subprocess.Popen(["python3", script])

    def stop(self):
        """Stop a process"""
        if self.is_running():
            # Wysyłanie sygnału sigint jest (w systemie Linux) podobne do naciśnięcia Ctrl+C.
            # To powoduje zakończenie procesu i wyczyszczenie wszystkich jego danych.

            self.current_process.send_signal(subprocess.signal.SIGINT)
            self.current_process = None

    def should_redirect(self, mode_name):
        return self.mode_config[mode_name].get('server') is True and self.is_running()
