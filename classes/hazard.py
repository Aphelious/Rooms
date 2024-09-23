class Hazard:
    def __init__(self, initial_message, inspect_message) -> None:
        self.initial_message = initial_message
        self.inspect_message = inspect_message
        self.attributes = []
        self.interactions = []