from .abort_exception import AbortException

DEFAULT_BROKER = 'localhost:9092'
DEFAULT_GROUP = 'pots-group-default'


class Base:
    def process_message(self, message):
        raise NotImplementedError

    def detect_control_message(self, message) -> None:
        """
        Control message from the server
        """
        if message.is_control_message() and message.command:
            raise AbortException

    def ignore_control_message(self, message) -> None:
        if message.is_control_message():
            raise AbortException
