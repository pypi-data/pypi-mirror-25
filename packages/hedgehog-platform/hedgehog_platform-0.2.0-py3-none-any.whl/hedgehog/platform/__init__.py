import time

RASPBERRY_PI_3B = 'Raspberry Pi 3 Model B'
ORANGE_PI_2 = 'Orange Pi 2'

try:
    from RPi import GPIO as _GPIO
except (ImportError, RuntimeError):
    PLATFORM = ORANGE_PI_2
else:
    PLATFORM = RASPBERRY_PI_3B

try:
    # don't fail if you work without PySerial (e.g. emulator)
    import serial
except ImportError:
    pass
else:
    SERIAL_PARAMS = dict(
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=0.5,
        xonxoff=False,
        rtscts=False,
        writeTimeout=None,
        dsrdtr=False,
        interCharTimeout=None,
    )

NRST_PIN = 29
BOOT0_PIN = 31

if PLATFORM == RASPBERRY_PI_3B:
    SERIAL = '/dev/ttyS0'

    _GPIO.setmode(_GPIO.BOARD)

    class GPIO:
        HIGH = _GPIO.HIGH
        LOW = _GPIO.LOW

        OUT = _GPIO.OUT
        IN = _GPIO.IN

        PUD_OFF = _GPIO.PUD_OFF
        PUD_UP = _GPIO.PUD_UP
        PUD_DOWN = _GPIO.PUD_DOWN

        def __init__(self, channel):
            self.channel = channel

        @classmethod
        def cleanup(cls):
            _GPIO.cleanup()

        def setup(self, direction, pull_up_down=PUD_OFF, initial=None):
            if initial is None:
                _GPIO.setup(self.channel, direction, pull_up_down)
            else:
                _GPIO.setup(self.channel, direction, pull_up_down, initial)

        def set(self, value):
            _GPIO.output(self.channel, value)

        def get(self):
            _GPIO.input(self.channel)
elif PLATFORM == ORANGE_PI_2:
    SERIAL = '/dev/ttyS3'

    _pin_map = {
        29: 'PA7',
        31: 'PA8',
    }

    class GPIO:
        HIGH = 1
        LOW = 0

        OUT = 0
        IN = 1

        PUD_OFF = 20
        PUD_UP = 22
        PUD_DOWN = 21

        def __init__(self, pin):
            """
            Creates a GPIO object.

            :param pin: a pin name such as `'PA0'`
            """
            self.pin = _pin_map[pin]
            self.data_file = self._pin_file(self.pin, 'data')

        @classmethod
        def cleanup(cls):
            pass

        @classmethod
        def _pin_file(cls, pin, file):
            """
            Returns the file path, specific to the Orange PI/gpio-sunxi kernel module,
            that corresponds to the given pin and function.
            The validity of the arguments is not checked.

            :param pin: a pin name such as `'PA0'`
            :param file: a file name such as `'data'`
            :return: the absolute path of the specified file
            """
            return '/sys/class/gpio_sw/%s/%s' % (pin, file)

        @classmethod
        def _write(cls, file, value):
            """
            Performs a single write to the given file.

            :param file: the file name
            :param value: the string value to write
            """
            with open(file, 'w') as fd:
                fd.write(value)

        @classmethod
        def _read(cls, file):
            """
            Reads the given file.

            :param file: the file name
            :return: the string content of the file
            """
            with open(file, 'r') as fd:
                return fd.read()

        def setup(self, direction, pull_up_down=PUD_OFF, initial=None):
            if direction != GPIO.OUT:
                raise NotImplementedError
            if initial is not None:
                self.set(initial)

        def set(self, value):
            """
            Writes the value to the pin's `data` file. The boolean value is
            converted to `'1'`/`'0'`.

            :param value: a boolean value
            """
            self._write(self.data_file, '1' if value else '0')

        def get(self):
            """
            Reads the value of the pin's `data` file.

            :return: `True` if the file contains `'1'`, `False` otherwise
            """
            return self._read(self.data_file).strip() == '1'

        def write(self, file, value):
            """
            Writes an arbitrary string to one of the pin's files.

            :param file: a file name such as `'data'`
            :param value: the string value for the file
            """
            self._write(self._pin_file(self.pin, file), value)

        def read(self, file):
            """
            Reads the contents of one of the pin's files.

            :param file: a file name such as `'data'`
            :return: the string content of the file
            """
            return self._read(self._pin_file(self.pin, file))
else:
    assert False


class Controller:
    def __init__(self):
        self.nrst = GPIO(NRST_PIN)
        self.nrst.setup(GPIO.OUT)

        self.boot0 = GPIO(BOOT0_PIN)
        self.boot0.setup(GPIO.OUT)

        self.serial = serial.Serial(port=SERIAL, **SERIAL_PARAMS)

    def reset(self, on=False, boot0=False):
        """
        Resets the connected hardware controller. If `on` is false, the controller will stay in the reset state.
        Otherwise, the controller will subsequently restart. In that case, `boot0` controls whether the controller runs
        the bootloader, or the user's program; and the controller's serial connection is flushed, so that no garbage
        from before the reset is subsequently read.

        Keep in mind that the `boot0` pin is set even if `not on`.

        :param on: Whether to turn the controller on
        :param boot0: Whether to start into the bootloader
        """
        self.boot0.set(boot0)
        self.nrst.set(False)
        time.sleep(0.1)
        if on:
            self.nrst.set(True)
            time.sleep(0.5)

            self.serial.flushInput()
            self.serial.flushOutput()

    def cleanup(self):
        self.serial.close()
        GPIO.cleanup()
