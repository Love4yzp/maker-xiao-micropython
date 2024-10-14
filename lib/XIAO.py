from os import uname
from re import search
from machine import Pin

class LED:
    """
    D4|GPIO15: Yellow Light
    """
    def __init__(self, pin=15):
        self.led = Pin(pin, Pin.OUT)
    
    def on(self):
        self.led.off()
    
    def off(self):
        self.led.on()
    
    def toggle(self):
        self.led.value(not self.led.value())

class BoardConfig:
    """
    BoardConfig class defines pin mappings for XIAO ESP32 boards using properties.
    
    Supported board types:
    - 'xiao_esp32c3' : XIAO ESP32C3 Board
    - 'xiao_esp32c6' : XIAO ESP32C6 Board
    - 'xiao_esp32s3' : XIAO ESP32S3 Board
    """

    def __init__(self, board_type = None):
        """
        Initializes the BoardConfig based on the provided board type.

        Args:
        - board_type (str): Type of XIAO board.
        """
        self._board_type = board_type or self.detect_board_type()
        
        if self.LED_BUILTIN: self.board_led = self.LED_BUILTIN

    @classmethod
    def detect_board_type(cls):
        """
        Detects the board type based on the machine name from os.uname().
        
        Returns:
        - str: The detected board type.
        """
        machine = uname().machine
        if search(r'ESP32C6', machine):
            return 'xiao_esp32c6'
        elif search(r'ESP32C3', machine):
            return 'xiao_esp32c3'
        elif search(r'ESP32S3', machine):
            return 'xiao_esp32s3'
        return None

    def _get_pin_mapping(self, pin_name):
        """Returns the pin number for the given pin name based on the board type."""
        pin_mappings = {
            "xiao_esp32c3": {
                "D0": 2, "D1": 3, "D2": 4, "D3": 5, "D4": 6, "D5": 7, "D6": 21, "D7": 20,
                "D8": 8, "D9": 9, "D10": 10, "TX": 21, "RX": 20,
                "SDA": 6, "SCL": 7, "A0": 2, "A1": 3, "A2": 4
            },
            "xiao_esp32c6": {
                "D0": 0, "D1": 1, "D2": 2, "D3": 21, "D4": 22, "D5": 23, "D6": 16, "D7": 17,
                "D8": 19, "D9": 20, "D10": 18, "TX": 16, "RX": 17,
                "SDA": 22, "SCL": 23, "A0": 0, "A1": 1, "A2": 2,
                "LED_BUILTIN": 15,
            },
            "xiao_esp32s3": {
                "D0": 1, "D1": 2, "D2": 3, "D3": 4, "D4": 5, "D5": 6, "D6": 43, "D7": 44,
                "D8": 7, "D9": 8, "D10": 9, "TX": 43, "RX": 44,
                "SDA": 5, "SCL": 6, "A0": 1, "A1": 2, "A2": 3, "A3": 4, "A4": 5, "A5": 6,
                "A8": 7, "A9": 8, "A10": 9,
                "LED_BUILTIN": 21
            },
        }

        if self._board_type not in pin_mappings:
            raise ValueError(f"Unsupported board type: {self._board_type}")
        
        if pin_name not in pin_mappings[self._board_type]:
            raise ValueError(f"Pin {pin_name} not available for board {self._board_type}")
        
        return pin_mappings[self._board_type][pin_name]

    @property
    def board_led(self):
        return self.__led
    
    @board_led.setter
    def board_led(self, led_pin):
        """
        Args:
        - led_pin(int): the pin of a led
        """
        if led_pin != self.LED_BUILTIN:
            print("USING NOT BUILT-IN LED for board")
        self.__led = LED(led_pin)
        return self.__led

    @property
    def D0(self):
        return self._get_pin_mapping("D0")

    @property
    def D1(self):
        return self._get_pin_mapping("D1")

    @property
    def D2(self):
        return self._get_pin_mapping("D2")

    @property
    def D3(self):
        return self._get_pin_mapping("D3")

    @property
    def D4(self):
        return self._get_pin_mapping("D4")

    @property
    def D5(self):
        return self._get_pin_mapping("D5")

    @property
    def D6(self):
        return self._get_pin_mapping("D6")

    @property
    def D7(self):
        return self._get_pin_mapping("D7")

    @property
    def D8(self):
        return self._get_pin_mapping("D8")

    @property
    def D9(self):
        return self._get_pin_mapping("D9")

    @property
    def D10(self):
        return self._get_pin_mapping("D10")

    @property
    def TX(self):
        return self._get_pin_mapping("TX")

    @property
    def RX(self):
        return self._get_pin_mapping("RX")

    @property
    def SDA(self):
        return self._get_pin_mapping("SDA")

    @property
    def SCL(self):
        return self._get_pin_mapping("SCL")

    @property
    def A0(self):
        return self._get_pin_mapping("A0")

    @property
    def A1(self):
        return self._get_pin_mapping("A1")

    @property
    def A2(self):
        return self._get_pin_mapping("A2")
    
    @property
    def LED_BUILTIN(self):
        return self._get_pin_mapping("LED_BUILTIN")

    # Add other pin properties as needed