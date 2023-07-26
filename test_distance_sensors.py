import time
from gpiozero import DistanceSensor

print("Przygotowanie pinów GPIO")
sensor_l = DistanceSensor(echo=17, trigger=27, queue_len=2)
sensor_r = DistanceSensor(echo=5,  trigger=6, queue_len=2)

while True:
    print("Lewy: {l:.2f}, Prawy: {r:.2f}".format(
        l=sensor_l.distance * 100,
        r=sensor_r.distance * 100))
    time.sleep(0.1)
