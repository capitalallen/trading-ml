
# +12058804170

from twilio.rest import Client


class Send_message:
    def __init__(self):
        self.account = 'AC7ce530153bf13cc4b5e10f7a951ea8e4'
        self.token = 'c09761f603cd6f5d4b49b89d4fd2a448'
        self.client = Client(self.account, self.token)

    def send_a_message(self, message):
        try:
            self.client.messages.create(from_='+12058804170',
                                        to='+15196972638',
                                        body=message)
        except:
            print("error: send message")
            #self.error_message()

    def error_message(self):
        self.client.messages.create(from_='+12058804170',
                                    to='+15196972638',
                                    body="cannot send the message")
