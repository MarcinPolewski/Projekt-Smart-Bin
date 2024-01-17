from machine import Pin, ADC, SoftI2C
from hcsr04 import HCSR04
import ssd1306
from time import sleep

# ports declaration
JOYSTICK_X = 34
JOYSTICK_Y = 35
JOYSTICK_BUTTON = 13

OLED_SDA = 21
OLED_SCL = 22


# oled initialization
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# potenciometer initialization
pot_x = ADC(JOYSTICK_X)
pot_x.atten(ADC.ATTN_11DB)  # Full range: 3.3v

pot_y = ADC(JOYSTICK_Y)
pot_y.atten(ADC.ATTN_11DB)  # Full range: 3.3v

# distance sensor initialization
sensor = HCSR04(trigger_pin=5, echo_pin=18, echo_timeout_us=10000)

print("initialized properly!")

while True:
    sx = "x: " + str(pot_x.read())
    sy = "y: " + str(pot_y.read())
    sd = "distance: " + str(sensor.distance_cm())

    oled.fill(0)
    oled.text(sx, 0, 0)
    oled.text(sy, 0, 10)
    oled.text(sd, 0, 20)

    oled.show()
