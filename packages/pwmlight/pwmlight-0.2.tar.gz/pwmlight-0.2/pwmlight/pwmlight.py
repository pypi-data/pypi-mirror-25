import pigpio as pg

class pwmlight():
    def __init__(self, pin, min_cycle, max_cycle, name = None, frequency = 2000):
        self._pin = pin
        self._min_cycle = min_cycle
        self._max_cycle = max_cycle
        self._name = name
        self._state = True
        self._brightness = 255
        self._gpio = pg.pi()
        self._convfactor = (max_cycle - min_cycle) / 255
        self._freq = frequency

        if name is None:
            self._name = 'P' + str(pin)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = value

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.update()

    def turnOn(self):
        self._state = True
        self.update()

    def turnOff(self):
        self._state = False
        self.update()

    def setBrightness(self, value):
        self._brightness = value
        self.update()

    def getState(self):
        if self._brightness  * self._convfactor + self._min_cycle > self._min_cycle:
            return True
        else:
            return False

    def update(self):
        self._gpio.hardware_PWM(self._pin, self._freq,
                                (self._brightness * self._convfactor * int(self._state) + self._min_cycle))

    def debug(self, val):
        self._gpio.hardware_PWM(self._pin, self._freq, val)
