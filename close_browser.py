import os
import syslog


    
def main():
    os.popen('wmctrl -c \"Chromium\"')
    syslog.syslog(syslog.LOG_INFO, "CLOSED CHROMIUM WINDOW")

if __name__ == "__main__":
    main()