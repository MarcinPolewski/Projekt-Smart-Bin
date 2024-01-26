from machine import Pin, ADC, SoftI2C
from hcsr04 import HCSR04
import ssd1306
import network
import urequests
import ujson

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

from memoryHandler import MemoryHandler


class WiFiConnectionError(Exception):
    def __inti__(self):
        super.__init__("establishing wi-fi connection unsuccessful")


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
        self._bin_id = 1
        self._is_wifi_connected = False
        self._station = network.WLAN(network.STA_IF)
        self._server_link = "http://79.185.97.58:8001/"
        pass

    def connect_to_wifi(self):
        # print("connecting...")
        wifi_name = "AndroidAPbd0b"
        wifi_password = "mwth1802"

        self._station.active(False)
        self._station.active(True)
        self._station.connect(wifi_name, wifi_password)
        time.sleep(10)

        if not self._station.isconnected():
            raise WiFiConnectionError

        # if self._station.isconnected():
        #     # print("connected")
        # else:
        #     # print("connection unsuccessfull")

    def is_wifi_connected(self):
        return self._station.isconnected()

    def handle_connection(self):
        """method tries to connect to wi-fi, return true if connection is on"""
        if self.is_wifi_connected():
            return True
        else:
            try:
                self.connect_to_wifi()
                return True
            except WiFiConnectionError:
                # @TODO save logs to database for later update?
                # print("connection unsuccessful")
                pass

        return False

    def upload_current_depth(self, current_depth):
        """sends current depth to server"""
        if self.handle_connection():
            data = {"date_log": "", "bin_id": self._bin_id, "bin_status": current_depth}
            json_data = ujson.dumps(data)
            link = self._server_link + "logs/"
            urequests.post(link, data=json_data).json()
            time.sleep(0.5)
            # print("current depth sent!: " + str(current_depth))

    def send_log_to_server(self, who_took_out, who_should_have):
        """sends info, when somebody took out the trash"""
        if self.handle_connection():
            # print("sending log..")
            data = {
                "id_empty": 1,
                "which_bin": self._bin_id,
                "who_should": who_should_have,
                "who_did": who_took_out,
                "date": "2020",
                "add_points": 1,
                "sub_points": 1,
            }
            # print(data)
            json_data = ujson.dumps(data)
            link = self._server_link + "takeout/"
            # print(link)
            # print(data)
            urequests.post(link, data=json_data).json()
            time.sleep(0.5)
            # print("log sent!")

    def process_users(self, users):
        user_classes = []
        for user in users:
            user_class = User(
                user_id=user["id_user"],
                user_name=user["user_name"],
                points_status=user["points_status"],
            )
            user_classes.append(user_class)
        return user_classes

    def fetch_users_from_server(self):
        users = []
        link = self._server_link + "users/"

        if self.handle_connection():
            users = urequests.get(link).json()
            # users = [
            #     {"user_id": 5344, "user_name": "Julka Gorka", "points_status": 100},
            #     {"user_id": 7465, "user_name": "Jarek Darek", "points_status": 10},
            #     {"user_id": 4321, "user_name": "Jurek Ogorek", "points_status": 2},
            #     {"user_id": 1234, "user_name": "Jacek Wacek", "points_status": 5},
            # ]
            # print("users fetched!")
            users = self.process_users(users)
            time.sleep(0.5)
        return users

    def send_bin_configuration_to_server(self, base_depth):
        if self.handle_connection():
            # print("startttt")
            link = self._server_link + "bins/"
            # data = urequests.get(link).json()
            # # print("bin data fetched!")
            # # print(data)
            # data[0]["bin_depth"] = str(int(base_depth))
            # # print(data)

            data = {
                "bin_name": "kosz pod zlewem",
                "emp_calendar": 0,
                "bin_depth": str(int(base_depth)),
                "id_bin": 1,
                "emp_reminder": 3,
                "adding_points": 12,
                "subtrack_points": 17,
                "bin_status": "100",
            }

            json_data = ujson.dumps(data)
            headers = {"Content-type": "application/json"}
            urequests.put(link, data=json_data, headers=headers)
            # print("config sent!")


class BinStatusHandler:
    """handles status of bin"""

    def __init__(self, screen_handler, server_connectivity_hanlder, memory_handler):
        self._screen_handler = screen_handler
        self._server_handler = server_connectivity_hanlder
        self._memory_handler = memory_handler

        self._base_depth = 10
        self._current_depth = 5

        self._phase = START_PHASE

        self._bin_name = ""
        self._users = None

        self._designated_user = None  # one who should take out
        self._selected_user = None  # one who did take out the trash
        self._displayed_user = self._designated_user  # user displayed while selecting
        self._displayed_user_idx = 0

        self._screen_handler.switch_to_start_phase()

    @property
    def phase(self):
        return self._phase

    @property
    def base_depth(self):
        return self._base_depth

    @property
    def current_depth(self):
        return self._current_depth

    def was_bin_emptied(self, new_distance):
        distance_delta = abs(new_distance - self._base_depth)

        # jesli aktualnie śmietnik jest pusty i wcześniej pełny powyzej poziomu jakiegos
        if (distance_delta < ULTRASONIC_SENSOR_TOLERANCE) and (
            self.get_bin_fullness_percentage() > PERCENTAGE_TO_REGISTER_TAKING_OUT
        ):
            return True

        return False

    def switch_to_select_user(self):
        """method trigged when trash has been taken out and
        doer must be selected"""
        self._phase = SELECT_USER_PHASE
        self._displayed_user = self._designated_user
        self._displayed_user_idx = 0  # displayed user is always first on the list
        self._screen_handler.switch_to_select_user_phase(
            self._displayed_user, points=self._displayed_user.points_status
        )

    def sync_current_depth(self):
        self._phase = SYNCING_PHASE
        self._screen_handler.switch_to_sync_phase()
        self._server_handler.upload_current_depth(
            self._base_depth - self._current_depth
        )

    def exit_lid_up_phase(self, new_distance_value):
        """method triggered when user exits lid up phases"""

        if self.was_bin_emptied(new_distance_value):
            # bin has been emptied
            self.switch_to_select_user()
            self._current_depth = self._base_depth

        else:
            # bin has not been emptied
            self._current_depth = new_distance_value
            self.sync_current_depth()

            self._phase = MAIN_PHASE

            next_user = str(self._designated_user)
            self._screen_handler.switch_to_main_phase(
                next_user, self.get_bin_fullness_percentage()
            )

    def distance_value_changed(self, new_value):
        """method called when distance sensor has detected a change"""
        # print("registered new distance value =" + str(new_value))
        if self._phase == START_PHASE:
            # print("not registstered due to start phase")
            return

        self._phase = LID_UP_PHASE
        self._screen_handler.switch_to_lid_up_phase()

    def switch_displayed_user(self, to_the_left):
        """switching displayed user during selecting user phase"""
        if to_the_left:
            self._displayed_user_idx -= 1
            if self._displayed_user_idx < 0:
                self._displayed_user_idx = len(self._users) - 1

            next_victim = self._users[self._displayed_user_idx]

            self._displayed_user = next_victim
            self._screen_handler.change_displayed_user(
                next_victim, next_victim.points_status
            )
        else:
            self._displayed_user_idx += 1
            if self._displayed_user_idx >= len(self._users):
                self._displayed_user_idx = 0

            next_victim = self._users[self._displayed_user_idx]

            self._displayed_user = next_victim
            self._screen_handler.change_displayed_user(
                next_victim, next_victim.points_status
            )

    def update_next_designated_user(self):
        """next designated user is the one with the smalles amount of points"""
        self._users = sorted(self._users, key=lambda x: x.points_status)
        self._designated_user = self._users[0]

    def user_selected(self):
        """triggered when user has been selected"""
        self._phase = SYNCING_PHASE
        self._screen_handler.switch_to_sync_phase()

        self._server_handler.send_log_to_server(
            who_took_out=self._displayed_user.user_id,
            who_should_have=self._designated_user.user_id,
        )
        self.sync_current_depth()
        self.fetch_users_from_server()

        self.update_next_designated_user()

        # after sync is completed phase will autoamtially change
        self._phase = MAIN_PHASE
        self._screen_handler.switch_to_main_phase(
            percentage=self.get_bin_fullness_percentage(),
            next_victim=self._designated_user,
        )

    def fetch_users_from_server(self):
        """fetches information from server"""
        self._users = self._server_handler.fetch_users_from_server()

    def handle_interaction_start_phase(self, event_type, distance):
        """when left press, configuration runs, when right, loading data from file"""
        if event_type == JOYSTICK_MOVED_LEFT:
            self.calibrate_bin(distance)
        elif event_type == JOYSTICK_MOVED_RIGHT:
            self.load_configuration()
            self._current_depth = distance
        else:
            return

        self._phase = SYNCING_PHASE
        self._screen_handler.switch_to_sync_phase()

        self.sync_current_depth()
        self.fetch_users_from_server()
        self.update_next_designated_user()

        self._phase = MAIN_PHASE
        self._screen_handler.switch_to_main_phase(
            next_victim=self._designated_user,
            percentage=self.get_bin_fullness_percentage(),
        )
        # print("switched to main")

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
            self.user_selected()

    def joystick_interaction(self, event_type, distance):
        """method called when user has interacted with joystick"""

        if self._phase == START_PHASE:
            self.handle_interaction_start_phase(event_type, distance)
        elif self._phase == MAIN_PHASE:
            self.handle_interaction_main_phase(event_type, distance)
        elif self._phase == LID_UP_PHASE:
            self.handle_interaction_lid_up_phase(event_type, distance)
        elif self._phase == SELECT_USER_PHASE:
            self.handle_interaction_select_user_phase(event_type, distance)

    def load_configuration(self):
        """loads bin configuration from file"""
        data = self._memory_handler.load_configuration()
        self._bin_name = data["bin_name"]
        self._base_depth = data["base_depth"]

    def calibrate_bin(self, distance):
        """triggered when bin is calibrating"""
        self._base_depth = distance
        self._current_depth = distance

        # sending configuration to server
        self._phase = SYNCING_PHASE
        self._screen_handler.switch_to_sync_phase()
        self._server_handler.send_bin_configuration_to_server(self._base_depth)

        # saving configuration to file
        data = {"bin_name": self._bin_name, "base_depth": self._base_depth}
        self._memory_handler.save_configuration(data)

    def get_bin_fullness_percentage(self):
        """returns percentage of bin fullness"""
        percentage = int(100 - ((self._current_depth / self._base_depth) * 100))
        return max(percentage, 0)


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

    def update(self):
        # method updates animations if such are happening
        pass

    def switch_to_start_phase(self):
        self._phase = START_PHASE
        self._screen.fill(0)

        self._screen.text("Thrasher The Bin", 0, 10)

        self._screen.text("by Trashers", 20, 30)

        self._screen.show()

    def switch_to_main_phase(self, next_victim, percentage):
        self._phase = MAIN_PHASE
        self._screen.fill(0)

        # @TODO - hadnle when name doesn't fit
        self._screen.text("Bin full in " + str(percentage) + "%", 0, 0)
        self._screen.text(str(next_victim), 0, 25)
        self._screen.text("is next", 0, 35)
        self._screen.show()

    def switch_to_lid_up_phase(self):
        self._phase = LID_UP_PHASE
        self._screen.fill(0)

        self._screen.text("Lid was removed.", 0, 0)
        self._screen.text("Reposition it", 0, 10)
        self._screen.text("and tap joystick", 0, 20)
        self._screen.text("to continue.", 0, 30)

        self._screen.show()

    def switch_to_sync_phase(self):
        self._phase = SYNCING_PHASE
        self._screen.fill(0)

        self._screen.text("Sync in", 20, 20)
        self._screen.text("progress..", 20, 30)
        self._screen.show()

    def switch_to_select_user_phase(self, displayed_user, points):
        self._phase = SELECT_USER_PHASE
        self._screen.fill(0)

        self._screen.text("Select who took out the trash", 0, 0)
        self._screen.text("out the trash:", 0, 10)
        self._screen.text(str(displayed_user), 0, 25)
        self._screen.text("with " + str(points) + "points", 0, 35)

        self._screen.show()

    def change_displayed_user(self, displayed_user, points):
        self._screen.fill(0)

        self._screen.text("Select who took out the trash", 0, 0)
        self._screen.text("out the trash:", 0, 10)
        self._screen.text(str(displayed_user), 0, 25)
        self._screen.text("with " + str(points) + "points", 0, 35)

        self._screen.show()


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
        self._current_distance_reading_time = (
            time.time_ns() // 1000000
        )  # value in miliseconds
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
        # print(read_distance)
        if self._registered_distance is None:
            self._registered_distance = read_distance
            self._bin_status_handler.distance_value_changed(read_distance)
            return

        current_time_in_ms = time.time_ns() // 1000000

        current_distance_delta = abs(read_distance - self._current_distance_reading)
        registered_value_distance_delta = abs(read_distance - self._registered_distance)
        time_delta = current_time_in_ms - self._current_distance_reading_time

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
            self._current_distance_reading_time = current_time_in_ms
            self._current_distance_reading = read_distance

    def update(self, joystick_x, joystick_y, distance):
        """method checks if input values have changed and triggers right methods
        in bin_status_controller"""

        self.update_ultrasonic_sensor(distance)
        self.update_joystick(joystick_x, joystick_y, distance=self._registered_distance)


def main():
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
    memory_handler = MemoryHandler()
    server_connectivity_hanlder = ServerConnectivityHandler()
    screen_handler = ScreenHandler(
        screen=oled, screen_height=oled_height, screen_width=oled_width
    )
    bin_status_handler = BinStatusHandler(
        screen_handler=screen_handler,
        server_connectivity_hanlder=server_connectivity_hanlder,
        memory_handler=memory_handler,
    )
    input_handler = InputHandler(bin_status_handler=bin_status_handler)

    while True:
        # fetching readings
        sx = pot_x.read()
        sy = pot_y.read()
        sd = sensor.distance_cm()

        input_handler.update(joystick_x=sx, joystick_y=sy, distance=sd)
        screen_handler.update()


if __name__ == "__main__":
    main()
