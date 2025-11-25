import serial
import time

class ArduinoLogger:
    def __init__(self, port="COM3", baud=9600):
        self.port = port
        self.baud = baud
        self.ser = serial.Serial(self.port, self.baud, timeout=1)
        time.sleep(2)  # Arduino reset

    def read_line(self):
        line = self.ser.readline().decode().strip()
        return line

    def parse_line(self, line):
        if line.startswith("ERR"):
            return None, None, True
        try:
            parts = line.split(";")
            temp = float(parts[0].split(":")[1])
            hum = float(parts[1].split(":")[1])
            return temp, hum, False
        except:
            return None, None, True

    def get_measurement(self):
        while True:
            line = self.read_line()
            if line:
                temp, hum, error = self.parse_line(line)
                if not error:
                    return temp, hum
