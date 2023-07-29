from icm20948 import ICM20948
from vpython import vector


class RobotImu:
    """Definicja wspólnego interfejsu dla jednostki nawigacji inercyjnej z funkcją pomiaru temperatury"""
    def __init__(self):
        self._imu = ICM20948()

    def read_temperature(self):
        """Odczyt temperatury w stopniach C."""
        return self._imu.read_temperature()

    def read_gyroscope(self):
        """ Pobranie przeskalowanych danych z żyroskopu"""
        _, _, _, x, y, z = self._imu.read_accelerometer_gyro_data()
        return vector(x, y, z)

    def read_accelerometer(self):
        """Pobranie danych z akcelerometru"""
        accel_x, accel_y, accel_z, _, _, _ = self._imu.read_accelerometer_gyro_data()
        return vector(accel_x, accel_y, accel_z)

    def read_magnetometer(self):
        """Pobranie danych z magnetometru"""
        mag_x, mag_y, mag_z = self._imu.read_magnetometer_data()
        return vector(mag_x, -mag_y, -mag_z)

