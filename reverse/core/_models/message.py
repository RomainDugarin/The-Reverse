from discord import Message

class Message:

    def __init__(self, message: Message):
        self.data = message
        self.run()
    
    def run(self):
        self.on_message()
    
    def on_message(self):
        print('New message found, can be stored')

    def getData(self):
        return self.data