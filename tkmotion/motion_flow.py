class MotionFlow:
    """A class to handle motion flow operations."""

    def __init__(self):
        self.config = []

    def load_config(self):
        print("Loading configuration...")

        from tkmotion.config_loader import ConfigLoader

        loader = ConfigLoader()
        self.config = loader.load()

    def execute(self):
        print("Executing motion flow...")
