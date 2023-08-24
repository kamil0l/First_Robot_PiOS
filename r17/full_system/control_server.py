from flask import Flask, render_template, jsonify
from robot_modes import RobotModes
from leds_led_shim import Leds

# Aplikacja Flask App zawiera wszystkie ścieżki.
app = Flask(__name__)
# Przygotowanie trybów robota do użycia
mode_manager = RobotModes()
leds = Leds()
leds.set_one(1, [0, 255, 0])
leds.show()


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    return response


@app.route("/")
def index():
    return render_template('menu.html', menu=mode_manager.menu_config)


@app.route("/run/<mode_name>", methods=['POST'])
def run(mode_name):
    global leds
    if leds:
        leds.clear()
        leds.show()
        leds = None

    # Użycie naszej aplikacji do uruchomienia procesu powiązanego z nazwą trybu (mode_name)
    mode_manager.run(mode_name)
    response = {'message': f'{mode_name} uruchomiony'}
    if mode_manager.should_redirect(mode_name):
        response['redirect'] = True
    return jsonify(response)


@app.route("/stop", methods=['POST'])
def stop():
    # Nakazanie naszemu systemowi, by zatrzymał wykonywany właśnie proces
    mode_manager.stop()
    return jsonify({'message': "Zatrzymano"})


app.run(host="0.0.0.0")
