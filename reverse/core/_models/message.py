from discord import Message

class Message:

    DEBUG = False

    def __init__(self, message: Message):
        self.data = message
        self.run()
    
    def run(self):
        self.on_message()

    def toggleDebug(self):
        Message.Debug != Message.Debug

    def isDebug(self):
        return Message.DEBUG
    
    def on_message(self, trigger: str="Unknown"):
        if(Message.DEBUG): print('New message found, triggered by {}'.format(trigger))

    def getData(self):
        return self.data