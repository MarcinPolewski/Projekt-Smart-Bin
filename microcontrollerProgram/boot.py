from machine import Pin, ADC, SoftI2C
from hcsr04 import HCSR04
import ssd1306

import time

from constants import (
    START_PHASE,
    MAIN_PHASE,
    LID_UP_PHASE,
    SUCCESS_PHASE,
    SYNCING_PHASE,
    SELECT_USER_PHASE,
    JOYSTICK_DEADZONE,
    ULTRASONIC_SENSOR_TOLERANCE,
    JOYSTICK_MAX_VALUE,
    JOYSTICK_MID_VALUE,
    JOYSTICK_MIN_VALUE,
    MIN_READING_TIME,
    JOYSTICK_MOVED_LEFT,
    JOYSTICK_MOVED_RIGHT,
    JOYSTICK_MOVED_UP,
    JOYSTICK_MOVED_DOWN,
)


class ServerConnectivityHandler:
    # @TODO
    def __init__(self):
        pass

    def send_depth_to_server(self, depth):
        """sends current depth detected to server"""
        pass

    def send_log_to_server(self, who_took_out, who_should_have):
        """sends info, when somebody took out the trash"""
        pass

    def fetch_users_from_server(self):
        data = [{"user_name": "Jórek Ogórek"}, {"user_name": "Jacek Wacek"}]
        return data

    def fetch_bin_data(self):
        data = [{"bin_name", "THE bin"}]
        return data


class BinStatusHandler:
    """handles status of bin"""

    def __init__(self, screen_handler, server_connectivity_hanlder):
        self._screen_handler = screen_handler
        self._server_handler = server_connectivity_hanlder
        self._base_depth = 10
        self._current_depth = 10
        self._lid_is_up = True
        self._phase = START_PHASE

        self._designated_user = None  # one who should take out
        self._selected_user = None  # one who did take out the trash

    @property
    def phase(self):
        return self._phase

    @property
    def lid_is_up(self):
        return self._lid_is_up

    @property
    def base_depth(self):
        return self._base_depth

    @property
    def current_depth(self):
        return self._current_depth

    def was_bin_emptied(self, new_distance):
        # TODO
        return False

    def exit_lid_up_phase(self, new_distance_value):
        self._phase = MAIN_PHASE

        # sending current status of bin
        self._server_handler.send_depth_to_server(new_distance_value)

        # sending log if bin was emptied
        if self.was_bin_emptied(new_distance_value):
            self._server_handler.send_log_to_server(
                designated_user=self._designated_user,
                selected_user=self._selected_user,
            )

    def distance_value_changed(self, new_value):
        """method called when distance sensor has detected a change"""
        self._phase = LID_UP_PHASE

    def joystick_interaction(self, event_type):
        """method called when user has interacted with joystick"""
        if event_type == JOYSTICK_MOVED_DOWN:
            if self.phase == LID_UP_PHASE:
                self.exit_lid_up_phase()
            # print("moeved down")
        elif event_type == JOYSTICK_MOVED_UP:
            if self.phase == LID_UP_PHASE:
                self.exit_lid_up_phase()
            # print("moeved up")
        elif event_type == JOYSTICK_MOVED_LEFT:
            if self.phase == LID_UP_PHASE:
                self.exit_lid_up_phase()
            # print("moeved left")
        elif event_type == JOYSTICK_MOVED_RIGHT:
            if self.phase == LID_UP_PHASE:
                self.exit_lid_up_phase()
            # print("moeved right")

    def calibrate_bin(self):
        pass

    def sync_with_server(self):
        pass

    def get_bin_fullness_percentage(self):
        return int((self._current_depth / self._base_depth) * 100)

    def update(self):
        self._screen_handler.set_phase(self._phase)

    # def update(self, read_distance):

    #     if self.phase ==

    #     # check if lid was removed
    #     if self.phase != LID_UP_PHASE and abs(read_distance - self._current_depth) > ULTRASONIC_SENSOR_TOLERANCE:
    #         self._phase = LID_UP_PHASE

    #     elif


class ScreenHandler:
    """handles displaing on the screen and controlling phases"""

    def __init__(self, screen, screen_height, screen_width):
        self._screen = screen
        self._screen_height = screen_height
        self._screen_width = screen_width
        self._phase = None

    @property
    def phase(self):
        return self._phase

    def set_phase(self, phase):
        """method changes phase and starts animation towars next phase"""
        self._phase = phase

    def update(self):
        # method updates animations if such are happening
        pass

    def draw_main_phase(self):
        next_turn = "Jan"

        self._screen.text("Main Phase", 0, 0)
        self._screen.text("Next Victim:" + next_turn, 0, 10)

    def draw_lid_up_phase(self):
        self._screen.text("Lid was removed.", 0, 0)
        self._screen.text("Reposition it", 0, 10)
        self._screen.text("and tap joystick", 0, 20)
        self._screen.text("to continue.", 0, 30)

    def draw(self):
        self._screen.fill(0)
        if self._phase == MAIN_PHASE:
            self.draw_main_phase()
        elif self._phase == LID_UP_PHASE:
            self.draw_lid_up_phase()
        self._screen.show()

    # def draw(self):
    #     # method handles drawing elements on screen
    #     if self.phase == MAIN_PHASE:
    #         self.draw_main_phase()
    #     elif self.phase == LID_UP_PHASE:
    #         self.draw_lid_up_phase()
    #     elif self.phase == SUCCESS_PHASE:
    #         self.draw_success_phase()
    #     elif self.phase == SYNCING_PHASE:
    #         self.draw_syncing_phase()
    #     elif self.phase == SELECT_USER_PHASE:
    #         self.draw_select_user_phase
    #     else:

    #     pass


class InputHandler:
    """method handles user input and triggers right methods in BinStatusHandler"""

    def __init__(self, bin_status_handler):
        self._bin_status_handler = bin_status_handler

        # variables are true if, corresponding movement was already registered
        self._joystick_up = False
        self._joystick_down = False
        self._joystick_left = False
        self._joystick_right = False

        # stores previous reading from ultrasonic sensor
        self._current_distance_reading = 0
        self._current_distance_reading_time = time.time()
        self._registered_distance = 0

    @property
    def phase(self):
        return self._bin_status_handler.phase

    def update_joystick(self, joystick_x, joystick_y):
        """returns true if movement was detected, so controller"""
        # joystick moved left
        if joystick_x <= JOYSTICK_DEADZONE - JOYSTICK_MIN_VALUE:
            if not self._joystick_left:
                self._joystick_left = True
                self._bin_status_handler.joystick_interaction(JOYSTICK_MOVED_LEFT)

        # joystick moved right
        elif joystick_x >= JOYSTICK_MID_VALUE + JOYSTICK_DEADZONE:
            if not self._joystick_right:
                self._joystick_right = True
                self._bin_status_handler.joystick_interaction(JOYSTICK_MOVED_RIGHT)
        else:
            self._joystick_left = False
            self._joystick_right = False

        # joystick moved up
        if joystick_y <= JOYSTICK_DEADZONE - JOYSTICK_MIN_VALUE:
            if not self._joystick_up:
                self._joystick_up = True
                self._bin_status_handler.joystick_interaction(JOYSTICK_MOVED_UP)

        # joystick moved down
        elif joystick_y >= JOYSTICK_MID_VALUE + JOYSTICK_DEADZONE:
            if not self._joystick_down:
                self._joystick_down = True
                self._bin_status_handler.joystick_interaction(JOYSTICK_MOVED_DOWN)
        else:
            self._joystick_down = False
            self._joystick_up = False

    def update_ultrasonic_sensor(self, read_distance):
        current_distance_delta = abs(read_distance - self._current_distance_reading)
        registered_value_distance_delta = abs(read_distance - self._registered_distance)
        time_delta = time.time() - self._current_distance_reading_time

        if current_distance_delta <= ULTRASONIC_SENSOR_TOLERANCE:
            if (time_delta >= MIN_READING_TIME) and (
                registered_value_distance_delta >= ULTRASONIC_SENSOR_TOLERANCE
            ):
                # value has changed and it has been so for atleas MIN_READING_TIME
                # register distance change
                self._registered_distance = read_distance
                self._bin_status_handler.distance_value_changed(read_distance)
        else:
            # wartość analizowanego odczytu się zmieniłą
            self._current_distance_reading_time = time.time()
            self._current_distance_reading = read_distance

    def update(self, joystick_x, joystick_y, distance):
        """method checks if input values have changed and triggers right methods
        in bin_status_controller"""
        self.update_joystick(joystick_x, joystick_y)
        self.update_ultrasonic_sensor(distance)


def main():
    # saving moment(time) of start of program
    start_time = time.time()
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

    # initializing handlers
    server_connectivity_hanlder = ServerConnectivityHandler()
    screen_handler = ScreenHandler(
        screen=oled, screen_height=oled_height, screen_width=oled_width
    )
    bin_status_handler = BinStatusHandler(
        screen_handler=screen_handler,
        server_connectivity_hanlder=server_connectivity_hanlder,
    )
    input_handler = InputHandler(bin_status_handler=bin_status_handler)

    while True:
        # fetching readings
        sx = pot_x.read()
        sy = pot_y.read()
        sd = sensor.distance_cm()

        input_handler.update(joystick_x=sx, joystick_y=sy, distance=sd)
        bin_status_handler.update()
        screen_handler.update()

        screen_handler.draw()

        # oled.fill(0)
        # oled.text(str(sd), 0, 0)
        # oled.text(("start: " + str(start_time)), 0, 10)
        # oled.text(("now: " + str(time_passed)), 0, 20)
        # # oled.text(sx, 0, 0)
        # # oled.text(sy, 0, 10)
        # # oled.text(sd, 0, 20)

        # oled.show()


if __name__ == "__main__":
    main()
