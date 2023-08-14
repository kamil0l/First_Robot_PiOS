from flask import Flask

from robot_modes import RobotModes
# Aplikacja Flask App zawiera wszystkie ścieżki.
app = Flask(__name__)
# Przygotowanie trybów robota do użycia
mode_manager = RobotModes()


@app.route("/run/<mode_name>", methods=['POST'])
def run(mode_name):
    # Użycie naszej aplikacji do uruchomienia procesu powiązanego z nazwą trybu (mode_name)
    mode_manager.run(mode_name)
    return "%s uruchomiony"


@app.route("/stop", methods=['POST'])
def stop():
    # Nakazanie naszemu systemowi, by zatrzymał wykonywany właśnie proces
    mode_manager.stop()
    return "Zatrzymany"


app.run(host="0.0.0.0", debug=True)
