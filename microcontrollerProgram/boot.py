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
    PERCENTAGE_TO_REGISTER_TAKING_OUT,
)


class User:
    def __init__(self, user_id, user_name, points_status):
        self._user_id = user_id
        self._user_name = user_name
        self._points_status = points_status

    @property
    def user_id(self):
        return self._user_id

    @property
    def user_name(self):
        return self._user_name

    @property
    def points_status(self):
        return self._points_status

    def __str__(self):
        return self._user_name

    def add_point(self):
        self._points_status += 1


class ServerConnectivityHandler:
    # @TODO
    def __init__(self):
        self._is_wifi_connected = False
        pass

    def connect_to_internet(self):
        pass

    def upload_fullness_percentage(self, depth):
        """sends current depth detected to server"""
        pass

    def send_log_to_server(self, who_took_out, who_should_have):
        """sends info, when somebody took out the trash"""
        print("trash out!")
        pass

    def process_users(self, users):
        users_classes = []
        for user in users:
            user_class = User(
                user_id=user["user_id"],
                user_name=user["user_name"],
                points_status=user["points_status"],
            )
            users_classes.append(user_class)
            return users_classes

    def fetch_users_from_server(self):
        users = [
            {"user_id": 5344, "user_name": "Julka Górka", "points_status": 0},
            {"user_id": 7465, "user_name": "Jarek Darek", "points_status": 10},
            {"user_id": 4321, "user_name": "Jórek Ogórek", "points_status": 2},
            {"user_id": 1234, "user_name": "Jacek Wacek", "points_status": 5},
        ]
        users = self.process_users(users)
        return users

    def fetch_bin_data(self):
        data = [{"bin_name", "THE bin"}]
        return data


class BinStatusHandler:
    """handles status of bin"""

    def __init__(self, screen_handler, server_connectivity_hanlder):
        self._screen_handler = screen_handler
        self._server_handler = server_connectivity_hanlder
        self._base_depth = 10
        self._current_depth = 5
        self._lid_is_up = True
        self._phase = START_PHASE

        self._users = None

        self._designated_user = None  # one who should take out
        self._selected_user = None  # one who did take out the trash
        self._displayed_user = self._designated_user  # user displayed while selecting

        self._screen_handler.switch_to_start_phase()

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
        distance_delta = abs(new_distance - self._base_depth)
        if (distance_delta < ULTRASONIC_SENSOR_TOLERANCE) and (
            self.get_bin_fullness_percentage() > PERCENTAGE_TO_REGISTER_TAKING_OUT
        ):
            return True
        return False

    def switch_to_select_user(self):
        self._phase = SELECT_USER_PHASE
        self._displayed_user = self._designated_user
        self._screen_handler.set_phase(self._phase)

    def exit_lid_up_phase(self, new_distance_value):
        """method triggered when user exits lid up phases"""
        self._phase = MAIN_PHASE
        next_user = "asdf"
        self._screen_handler.switch_to_main_phase(
            next_user, self.get_bin_fullness_percentage()
        )

        self._current_depth = new_distance_value

        # sending current status of bin
        percentage = self.get_bin_fullness_percentage()
        self._server_handler.upload_fullness_percentage(percentage)

        if self.was_bin_emptied(new_distance_value):
            # bin has been emptied
            self.switch_to_select_user()

            self._current_depth = new_distance_value
        else:
            self._current_depth = new_distance_value

    def distance_value_changed(self, new_value):
        """method called when distance sensor has detected a change"""
        if self._phase == START_PHASE:
            return

        self._phase = LID_UP_PHASE
        self._screen_handler.switch_to_lid_up_phase()
        print("registered new distance value =" + str(new_value))

    def switch_displayed_user(self, to_the_left):
        """switching displayed user during selecting user phase"""
        if to_the_left:
            next_victim = "Lewicowy Jarek Marek"

            self._displayed_user = next_victim
            self._screen_handler.set_next_victim(next_victim)
        else:
            next_victim = "Prawicowy Jarek Marek"

            self._displayed_user = next_victim
            self._screen_handler.set_next_victim(next_victim)

    def update_next_designated_user(self):
        """next designated user is the one with the smalles amount of points"""
        print(self._users)
        self._users = sorted(self._users, key=lambda x: x.points_status)
        self._designated_user = self._users[1:]
        print(self._users)

    def user_selected(self, user):
        """triggered when user has been selected"""
        self._phase = SYNCING_PHASE
        self._server_handler.send_log_to_server(
            who_took_out=self._selected_user, who_should_have=self._designated_user
        )
        self.update_next_designated_user()

    def fetch_from_server(self):
        """fetches information from server"""
        self._users = self._server_handler.fetch_users_from_server()

    def handle_interaction_start_phase(self, event_type, distance):
        print("swithing to main")
        print(distance)

        self.fetch_from_server()

        self.calibrate_bin(distance)
        self.update_next_designated_user()
        self._phase = MAIN_PHASE
        self._screen_handler.switch_to_main_phase(
            next_victim=self._designated_user,
            percentage=self.get_bin_fullness_percentage(),
        )

    def handle_interaction_main_phase(self, event_type, distance):
        pass

    def handle_interaction_lid_up_phase(self, event_type, distance):
        self.exit_lid_up_phase(distance)

    def handle_interaction_select_user_phase(self, event_type, distance):
        if event_type == JOYSTICK_MOVED_LEFT:
            self.switch_displayed_user(to_the_left=True)
        elif event_type == JOYSTICK_MOVED_RIGHT:
            self.switch_displayed_user(to_the_left=False)
        elif event_type == JOYSTICK_MOVED_DOWN:
            self.user_selected(user=self._displayed_user)

    def joystick_interaction(self, event_type, distance):
        """method called when user has interacted with joystick"""
        print("event: " + str(event_type) + "phase: " + str(self._phase))

        if self._phase == START_PHASE:
            self.handle_interaction_start_phase(event_type, distance)
        elif self._phase == MAIN_PHASE:
            self.handle_interaction_main_phase(event_type, distance)
        elif self._phase == LID_UP_PHASE:
            self.handle_interaction_lid_up_phase(event_type, distance)
        elif self._phase == SELECT_USER_PHASE:
            self.handle_interaction_select_user_phase(event_type, distance)

    def calibrate_bin(self, distance):
        """triggered when bin is calibrating"""
        self._base_depth = distance

    def get_bin_fullness_percentage(self):
        """returns percentage of bin fullness"""
        return int((self._current_depth // self._base_depth) * 100)


class ScreenHandler:
    """handles displaing on the screen and controlling phases"""

    def __init__(self, screen, screen_height, screen_width):
        self._screen = screen
        self._screen_height = screen_height
        self._screen_width = screen_width
        self._phase = None
        self._next_victim = None
        self._fullness_percentage = None
        self._animation_is_running = False

    @property
    def phase(self):
        return self._phase

    def set_phase(self, phase):
        """method changes phase and starts animation towars next phase"""
        self._phase = phase

    def set_next_victim(self, next_victim):
        self._next_victim = next_victim

    def update(self):
        # method updates animations if such are happening
        pass

    def switch_to_start_phase(self):
        self._phase = START_PHASE
        self._screen.fill(0)

        self._screen.text("Thrasher The Bin", 20, 0)
        self._screen.text("by Trashers", 20, 10)

        self._screen.show()

    def switch_to_main_phase(self, next_victim, percentage):
        self._phase = MAIN_PHASE
        self._screen.fill(0)

        # @TODO - hadnle when name doesn't fit
        self._screen.text("Bin full in " + str(percentage) + "%", 0, 0)
        self._screen.text(str(next_victim) + "is next", 0, 15)

        self._screen.show()

    def switch_to_lid_up_phase(self):
        self._phase = LID_UP_PHASE
        self._screen.fill(0)

        self._screen.text("Lid was removed.", 0, 0)
        self._screen.text("Reposition it", 0, 10)
        self._screen.text("and tap joystick", 0, 20)
        self._screen.text("to continue.", 0, 30)

        self._screen.show()

    def switch_to_select_user_phase(self, displayed_user):
        self._phase = SELECT_USER_PHASE
        self._screen.text("Select who took out the trash", 0, 0)
        self._screen.text(displayed_user, 0, 10)

    def change_user(self, next_victim):
        self._screen.text("Select who took out the trash", 0, 0)
        self._screen.text(str(next_victim), 0, 10)


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
        self._registered_distance = None

    @property
    def phase(self):
        return self._bin_status_handler.phase

    def update_joystick(self, joystick_x, joystick_y, distance):
        """returns true if movement was detected, so controller"""
        # joystick moved left
        if joystick_x <= JOYSTICK_DEADZONE - JOYSTICK_MIN_VALUE:
            if not self._joystick_left:
                self._joystick_left = True
                self._bin_status_handler.joystick_interaction(
                    JOYSTICK_MOVED_LEFT, distance
                )

        # joystick moved right
        elif joystick_x >= JOYSTICK_MID_VALUE + JOYSTICK_DEADZONE:
            if not self._joystick_right:
                self._joystick_right = True
                self._bin_status_handler.joystick_interaction(
                    JOYSTICK_MOVED_RIGHT, distance
                )
        else:
            self._joystick_left = False
            self._joystick_right = False

        # joystick moved up
        if joystick_y <= JOYSTICK_DEADZONE - JOYSTICK_MIN_VALUE:
            if not self._joystick_up:
                self._joystick_up = True
                self._bin_status_handler.joystick_interaction(
                    JOYSTICK_MOVED_UP, distance
                )

        # joystick moved down
        elif joystick_y >= JOYSTICK_MID_VALUE + JOYSTICK_DEADZONE:
            if not self._joystick_down:
                self._joystick_down = True
                self._bin_status_handler.joystick_interaction(
                    JOYSTICK_MOVED_DOWN, distance
                )
        else:
            self._joystick_down = False
            self._joystick_up = False

    def update_ultrasonic_sensor(self, read_distance):
        if self._registered_distance is None:
            print("first run")
            self._registered_distance = read_distance
            self._bin_status_handler.distance_value_changed(read_distance)
            return

        current_distance_delta = abs(read_distance - self._current_distance_reading)
        registered_value_distance_delta = abs(read_distance - self._registered_distance)
        time_delta = time.time() - self._current_distance_reading_time

        if current_distance_delta <= ULTRASONIC_SENSOR_TOLERANCE:
            if (time_delta >= MIN_READING_TIME) and (
                registered_value_distance_delta >= ULTRASONIC_SENSOR_TOLERANCE
            ):
                # value has changed and it has been so for at least MIN_READING_TIME
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

        self.update_ultrasonic_sensor(distance)
        # @TODO check if provided distance works
        self.update_joystick(joystick_x, joystick_y, distance=self._registered_distance)


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
        screen_handler.update()

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
