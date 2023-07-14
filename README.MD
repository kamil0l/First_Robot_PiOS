# **INSTRUCTION**

## Hardware:
- Raspberry Pi 3 B v1.2
- Motor Driver HAT
- ICM20948 9DoF Motion Sensor
- ReSpeaker v1.1 for Raspberry Pi
- Raspberry Pi NoIR Camera HD v2 8MPx
- LED SHIM - 28 LED RGB
- LM393 slot sensor - two pieces
- TT Motor 1:48 DC 3V-6V - two pieces


## RPI configuration:

1. download Pi Imager on : https://www.raspberrypi.org/software
2. choose Raspberry Pi OS (other) --> Raspberry Pi OS Lite (32-bit)
3. install on your raspberry pi.
4. in the wpa_supplicant.conf file, fill in the name and password for your wi-fi network
5. copy the wpa_supplicant.conf file and ssh file and the ssd card on which you installed Pi OS
6. insert the sd card into the rapberrypi and connect to the power supply
7. on our computer (connected to the same network) open the command line (terminal) and type the command: ping raspberrypi.local
8. if everything is configured correctly we should get this response:
    Pinging raspberrypi.local [fe80::7b87:1d40:581f:7fba%6] with 32 bytes of data:
    Reply from fe80::7b87:1d40:581f:7fba%6: time=308ms 
    Reply from fe80::7b87:1d40:581f:7fba%6: time=7ms 
    Reply from fe80::7b87:1d40:581f:7fba%6: time=6ms 
    Reply from fe80::7b87:1d40:581f:7fba%6: time=7ms 
9. download puTTy program https://www.putty.org
10. connect to your raspberrypi using putty, in the address field type raspberrypi.local, the username defaults to: pi and the password is: raspberry
11. after a successful connection, type in terminal: "sudo apt update -y && sudo apt upgrade -y" to update your RPI

