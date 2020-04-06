import json


class Message:
    def __init__(self, parameters=None):
        self.control_message = False
        self.command = None
        self.pot_id = None
        if parameters:
            self.load_from_dict(parameters)

    def load_from_dict(self, parameters):
        if isinstance(parameters, str):
            parameters = json.loads(parameters)
        if not isinstance(parameters, dict):
            raise Exception('parameters must be a dict')
        for key in parameters:
            setattr(self, key, parameters[key])

    def get_message(self, is_dict=False):
        message = {'control_message': getattr(self, 'control_message'),
                   'command': getattr(self, 'command')}
        return message if is_dict else json.dumps(message)

    def is_control_message(self):
        return hasattr(self, 'control_message') and self.control_message
