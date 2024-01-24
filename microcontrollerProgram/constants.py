# phases
START_PHASE = 1  # when user has plug in bin
MAIN_PHASE = 2  # main screen displaying percentage and next victim
LID_UP_PHASE = 4  # when lid was moved
SELECT_USER_PHASE = 6  # user selects who took out trash
SYNCING_PHASE = 8  # microcontroller syncs with server
SUCCESS_PHASE = 10  # dipslayed when action was successful

# joystick
JOYSTICK_MAX_VALUE = 4095
JOYSTICK_MID_VALUE = JOYSTICK_MAX_VALUE // 2
JOYSTICK_MIN_VALUE = 0
JOYSTICK_DEADZONE = 1000  # how much user needs to move the stick, to trigger an input

JOYSTICK_MOVED_LEFT = 10
JOYSTICK_MOVED_RIGHT = 20
JOYSTICK_MOVED_UP = 30
JOYSTICK_MOVED_DOWN = 40

# ultrasonic sensor
ULTRASONIC_SENSOR_TOLERANCE = 5  # in cm ; due to uncertainity of measurements
MIN_READING_TIME = 750
# time in miliseconds how long sygnal should be present, to be registered

# how full bin should be, to register act of taking out trash
PERCENTAGE_TO_REGISTER_TAKING_OUT = 50
