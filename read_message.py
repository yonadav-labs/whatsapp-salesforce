import os
import sys
import time

from webwhatsapis import WhatsAPIDriver
from simple_salesforce import Salesforce
from config import *

sf = Salesforce(username=username, password=password, security_token=security_token)

def run():
    driver = WhatsAPIDriver(extra_params={ 'executable_path': './geckodriver' }, loadstyles=True, headless=True)
    print("Waiting for QR")
    # driver.get_qr('qr.png')   # does not work 
    driver.screenshot('./ref/qr.png')
    driver.wait_for_login(600)
    print("Bot started")

    # print (driver.get_my_contacts())
    driver.subscribe_new_messages(NewMessageObserver())
    print("Waiting for new messages...")
    driver.screenshot('./ref/12.png')
    """ Locks the main thread while the subscription in running """
    while True:
        time.sleep(60)


class NewMessageObserver:
    def on_message_received(self, new_messages):
        for message in new_messages:
            if message.type == 'chat':
                print("New message '{}' received from number {}".format(message.content, message.sender.id))
                sf.Whatsapp_Message__c.create({ 'Message_Body__c': message.content, 'Phone__c': message.sender.id.split('@')[0]})
            else:
                print("New message of type '{}' received from number {}".format(message.type, message.sender.id))


if __name__ == '__main__':
    run()
