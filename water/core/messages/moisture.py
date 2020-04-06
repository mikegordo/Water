import json

from .message import Message


class MoistureMessage(Message):
    def __init__(self, parameters=None):
        self.value = None
        self.description = None
        self.created = None
        super().__init__(parameters)

    def get_message(self, is_dict=False):
        message = self.get_dict()
        return message if is_dict else json.dumps(message)

    def get_dict(self):
        return {'pot_id': getattr(self, 'pot_id'),
                'value': getattr(self, 'value'),
                'description': getattr(self, 'description'),
                'created': getattr(self, 'created')}
