class MotionFlow:
    """A class to handle motion flow operations."""

    def __init__(self):
        self.config = []

    def load_config(self):
        print("Loading configuration...")
        import json
        import os

        print(f"{os.getcwd()=}")

        try:
            with open("tkmotion/default_config.json", "r") as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error loading configuration: {e}")

    def execute(self):
        print("Executing motion flow...")
