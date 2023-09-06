from robot import Robot
from time import sleep

bot = Robot()
red = (255, 0, 0)
blue = (0, 0, 255)

while True:
    print("czerwony")
    bot.leds.set_all(red)
    bot.leds.show()
    sleep(0.5)
    print("niebieski")
    bot.leds.set_all(blue)
    bot.leds.show()
    sleep(0.5)
