from beam_controller import BeamController
import sys
import time

def main():
    if len(sys.argv) != 2:
        print "You must provide exactly 1 argument ON/OFF"
        exit(1)

    allowed = ["ON", "OFF"]
    arg = sys.argv[1]
    if arg not in allowed:
        print "Argument must be either ON or OFF"
        exit(2)

    con = BeamController()
    print con.read_serial()
    if arg == "ON":
        con.beam_on()
    elif arg == "OFF":
        con.beam_off()
    else:
        print "Someone forgot to handle an argument. Sorry"
        exit(3)

    time.sleep(50./1000)
    print con.read_serial()    

if __name__ == "__main__":
    main()
