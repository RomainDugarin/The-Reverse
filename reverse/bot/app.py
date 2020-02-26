from reverse.client.reverse import Reverse


class Bot(Reverse):
    
    def __init__(self, **kwargs):
        super().__init__(kwargs=kwargs)
        self.registerEvents()

    def registerEvents(self):
        self.getClient().event(self.on_ready)
        self.getClient().event(self.on_message)

    async def on_ready(self):
        print('We have logged in as {0.user} using Bot implementation'.format(self.getClient()))
    
    def run(self, token: str):
        super().run(token=token)