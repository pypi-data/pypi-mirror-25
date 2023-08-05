import sys
import serial
import fcntl
import time
import termios

class BeamController:
    def __init__(self):
        self.serial = self._open_serial()

    def read_serial(self):
        try:
            fcntl.flock(self.serial.fileno(), fcntl.LOCK_EX)
            
            return self.__do_read(self.serial)
        finally:
            fcntl.flock(self.serial.fileno(), fcntl.LOCK_UN)

    def ensure_serial(self):
        if self.serial.isOpen():
            return

        self.serial = self._open_serial()

    def beam_off(self):
        self.do_command("BEAM OFF\r\n")

    def beam_on(self):
        self.do_command("BEAM ON\r\n")

    def do_command(self, cmd):
        try:
            fcntl.flock(self.serial.fileno(), fcntl.LOCK_EX)
            
            self.serial.write(cmd)
        finally:
            fcntl.flock(self.serial.fileno(), fcntl.LOCK_UN)


    def __do_read(self, serial):
        return serial.read(serial.inWaiting()).decode("ascii")

    def _determine_port(self):
        try:
            import serial.tools.list_ports as list_ports
            for p, _, hwid in list_ports.comports():
                if "2341:0042" in hwid:
                    return p
            return None
        except ImportError:
            print "import serial.tools.list_ports failed. Defaulting to /dev/ttyACM0"
            return "/dev/ttyACM0"

    def _build_serial(self):
        p = self._determine_port()
        if p is None:
            raise ValueError("No MEGA found")
    
        return serial.Serial(p)

    def _wait_for_ready(self, serial):
        try:
            fcntl.flock(serial.fileno(), fcntl.LOCK_EX)
            
            result = ""
            while "Ready" not in result:
                result += self.__do_read(serial)
                time.sleep(16./1000)
        finally:
            fcntl.flock(serial.fileno(), fcntl.LOCK_UN)

    def _open_serial(self):
        ser = self._build_serial()
        self._wait_for_ready(ser)
        return ser


    
    
