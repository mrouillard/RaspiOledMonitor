# RaspiOledMonitor

OLED monitor for Raspberry Pi to display IP, CPU load, Memory usage and Disk usage as soon as the Raspberry boots.

## hardware @TODO details

Using a ready made mini OLED display 128x32 pixel for use on I2C bus.

## Software

1. Python script stats.py

    This script is loosely forked from [Adafruit CircuitPython SSD1306 library examples](https://github.com/adafruit/Adafruit_CircuitPython_SSD1306/blob/master/examples/ssd1306_stats.py)

    *note: don't forget to install Python dependencies. I choose to do it system wide in my case as it did not hurt.*

    ```bash
    sudo pip3 install adafruit-circuitpython-lis3dh
    sudo pip3 install adafruit-circuitpython-ssd1306
    ```

    My PI is with FR_fr locale, hence the decimal separator is a comma. Thus the awk command was mixed up. And rather than fixing it (I tried for 5 minutes and failed), I replaced the shell command which extracted the system load from `top` to instead read the value from /proc/loadavg.

    The display will be refreshed every 1 second.

2. setting it as a service to start from boot

    This [answer from DougieLawson on raspberrypi.org forum](https://www.raspberrypi.org/forums/viewtopic.php?t=200174#p1247692) was very helpful to point me in a correct direction.

    Put the python script in /home/pi/OLED for example. Make it executable using `chmod +x stats.py` if needed.

    Then create a new config file for our service:

    ```bash
       sudo touch /etc/systemd/system/OLED.service
       sudo nano /etc/systemd/system/OLED.service
    ```

    and use this content:

    ```systemd
    [Unit]
    Description=Get OLED service running at boot
    After=networking.service

    [Service]
    Type=idle
    ExecStart=/home/pi/OLED/stats.py
    Restart=always
    StandartOutput=syslog
    StandartError=syslog
    SyslogIdentifier=OLED
    User=pi

    [Install]
    WantedBy=multi-user.target
    ```

    Once done:

    ```bash
    sudo systemctl enable OLED.service
    sudo systemctl start OLED.service
    ```

    It should already work. If not, first try `sudo systemctl status OLED.service`, and eventually have a look at the system log as the service is defined to ouput any issues in syslog (/var/log/syslog).
    You might also need to issue a `sudo systemctl daemon-reload`

    And finally, reboot your raspberry to your brand new service for good! 😎
