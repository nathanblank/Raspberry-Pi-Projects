import os
from twilio.rest import Client
import syslog

account_sid = 'AC925012f813e66fd372400c07361c5e0e'
auth_token = '1ae28399ec3b0b5dfb4130187c0dab24'

temp_threshhold = 72

def get_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    temp = float(temp.replace("temp=","").replace("'C\n",""))
    return temp

def main():
    temperature = get_temp()
    if temperature > temp_threshhold:
        syslog.syslog(syslog.LOG_INFO, "Temperature is too high: {}'C".format(temperature))
        print("Temperature is too high: {}'C".format(temperature))
        initClient = Client(account_sid, auth_token)
        initMessage = initClient.messages.create(
            from_='+18666477322',
            to='+12029039214',
            body = 'TOO HOT\n' + 'Raspberry Pi temp is:\n' + str(temperature) + " degrees C"
        )
    else:
        print("Temperature is OK: {}'C".format(temperature))
        syslog.syslog(syslog.LOG_INFO, "Temperature is OK: {}'C".format(temperature))

if __name__ == "__main__":
    main()