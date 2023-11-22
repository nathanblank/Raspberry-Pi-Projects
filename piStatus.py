from twilio.rest import Client
import os
import time


account_sid = 'AC3218b306ea7758dde3f6ac005e345534'
auth_token = '62d08cd2b1a99a8d6d4bf77d662daf1f'

def measure_temp():
    temp = os.popen("vcgencmd measure_temp").readline()
    # print(temp)
    return (temp)

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage

# Open the plain text file whose name is in textfile for reading.

client = Client(account_sid, auth_token)
if __name__ == '__main__':
    while True:
        # At the top of every hour, send a text message with the system temperature using the measure_temp() function
        result = time.localtime(time.time())
        # while True:
        #     print(measure_temp())
        #     time.sleep(1)
        if(True):
            print("HIT")
            # message = client.messages.create(
            #             from_='+18447271166',
            #             to='+12029039214',
            #             body= str(measure_temp())
            #             )
            # print(message.sid)
            
            msg = EmailMessage()

            # me == the sender's email address
            # you == the recipient's email address
            msg['Subject'] = f'Pi Status: {result.tm_hour}:{result.tm_min}'
            msg['From'] = "nathan@blanken.me"
            msg['To'] = "nathan@blanken.me"

            # Send the message via our own SMTP server.
            s = smtplib.SMTP('localhost')
            s.send_message(msg)
