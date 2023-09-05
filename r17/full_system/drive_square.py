from robot import Robot, EncoderCounter
from pid_controller import PIController
import time
import math
import logging
logger = logging.getLogger("drive_square")

def drive_distances(bot, left_distance, right_distance, speed=80):
    # Chcemy, aby główny silnik zawsze pokonywał dłuższy dystans, dlatego musi obracać się szybciej
    if abs(left_distance) >= abs(right_distance):
        logger.info("Lewy jest głównym silnkiem")
        set_primary = bot.set_left
        primary_encoder = bot.left_encoder
        set_secondary = bot.set_right
        secondary_encoder = bot.right_encoder
        primary_distance = left_distance
        secondary_distance = right_distance
    else:
        logger.info("Prawy jest głównym silnkiem")
        set_primary = bot.set_right
        primary_encoder = bot.right_encoder
        set_secondary = bot.set_left
        secondary_encoder = bot.left_encoder
        primary_distance = right_distance
        secondary_distance = left_distance
    primary_to_secondary_ratio = secondary_distance / primary_distance
    secondary_speed = speed * primary_to_secondary_ratio
    logger.debug("Cele - główny: %d, drugorzędny: %d, stosunek: %.2f" % (primary_distance, secondary_distance, primary_to_secondary_ratio))
    primary_encoder.reset()
    secondary_encoder.reset()

    controller = PIController(proportional_constant=5, integral_constant=0.2)

    # Upewnienie się, że enkoder wie, w którą stronę się kręci
    primary_encoder.set_direction(math.copysign(1, speed))
    secondary_encoder.set_direction(math.copysign(1, secondary_speed))

    # Uruchomienie silników i pętli
    set_primary(speed)
    set_secondary(int(secondary_speed))
    while abs(primary_encoder.pulse_count) < abs(primary_distance) or abs(secondary_encoder.pulse_count) < abs(secondary_distance):
        time.sleep(0.01)
        # Jaka jest wartość uchybu?
        secondary_target = primary_encoder.pulse_count * primary_to_secondary_ratio
        error = secondary_target - secondary_encoder.pulse_count
        adjustment = controller.get_value(error)
        # Jak szybko silniki powinny się poruszać, aby jechać prosto?
        set_secondary(int(secondary_speed + adjustment))
        secondary_encoder.set_direction(math.copysign(1, secondary_speed+adjustment))

        # Log
        logger.debug(f"Enkodery: główny: {primary_encoder.pulse_count}, drugorzędny: {secondary_encoder.pulse_count}," 
                    f"uchyb:{error} korekta: {adjustment:.2f}")
        logger.info(f"Odległości: główny: {primary_encoder.distance_in_mm()} mm, drugorzędny: {secondary_encoder.distance_in_mm()} mm")
        # Zatrzymanie głównego silnika
        if abs(primary_encoder.pulse_count) >= abs(primary_distance):
            logger.info("główny stop")
            set_primary(0)
            secondary_speed = 0

def drive_arc(bot, turn_in_degrees, radius, speed=80):
    """ Skręt opiera się na zmianie położenia czoła robota """
    # Pobranie szerokości robota w tyknięciach
    half_width_ticks = EncoderCounter.mm_to_ticks(bot.wheel_distance_mm/2.0)
    if turn_in_degrees < 0:
        left_radius = radius - half_width_ticks
        right_radius = radius + half_width_ticks
    else:
        left_radius = radius + half_width_ticks
        right_radius = radius - half_width_ticks
    logger.info(f"Promień lewego łuku {left_radius:.2f}, prawy promień {right_radius:.2f}")
    radians = math.radians(abs(turn_in_degrees))
    left_distance = int(left_radius * radians)
    right_distance = int(right_radius * radians)
    logger.info(f"Długośc lewego łuku {left_distance}, dystans prawego koła {right_distance}")
    drive_distances(bot, left_distance, right_distance, speed=speed)


logging.basicConfig(level=logging.DEBUG)
bot = Robot()
distance_to_drive = 300 # W mm
distance_in_ticks = EncoderCounter.mm_to_ticks(distance_to_drive)
radius = bot.wheel_distance_mm + 100 # W mm
radius_in_ticks = EncoderCounter.mm_to_ticks(radius)

for n in range(4):
    drive_distances(bot, distance_in_ticks, distance_in_ticks)
    drive_arc(bot, 90, radius_in_ticks, speed=50)

