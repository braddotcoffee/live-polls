class Observable:
    def __init__(self):
        self.observers = list()

    def subscribe(self, handler):
        self.observers.append(handler)

    async def emit(self, value):
        for observer in self.observers:
            await observer(value)
