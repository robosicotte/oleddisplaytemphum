## oleddisplaytemphum:
A simple utility  to display temperature and humidity for a Raspberry Pi with a 128 x 64 OLED.

### Depends on CircuitPython which requires system-site-packages
To make the venv
```
python -m venv --system-site-packages venv
```
Enter the venv and then:
```
pip install -r requirements.txt
```
### Depends on freesans fonts:
To install
```
sudo apt install fonts-freefont-ttf
```
### Pinouts:

Display must be connected to I2C on the Pi.
<br/>
Momentary switch (NO) from pin D21 to GND


