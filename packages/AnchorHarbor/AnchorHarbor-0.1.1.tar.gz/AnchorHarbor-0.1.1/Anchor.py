import uuid

class Anchor():
    events = {}

    def __init__(self):
        pass

    @staticmethod
    def register(event, listener):
        uuid = Anchor.__get_uuid()
        if event not in Anchor.events:
            Anchor.events[event] = {}
        Anchor.events[event][uuid] = listener

        return lambda *args: Anchor.__unsubscribe(event, uuid)


    @staticmethod
    def emit(event, data=None):
        for callback_uuid in Anchor.events[event]:
            Anchor.events[event][callback_uuid](data)


    @staticmethod
    def __unsubscribe(event, uuid):
        del Anchor.events[event][uuid]


    @staticmethod
    def __get_uuid():
        return str(uuid.uuid4())


    @staticmethod
    def destroy():
        del Anchor.events[event]
