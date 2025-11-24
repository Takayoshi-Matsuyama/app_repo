class ConfigLoader:
    """Configuration Loader for MotionFlow."""

    def __init__(self, config_path="tkmotion/default_config.json"):
        self.config_path = config_path
        self.config = []

    def load(self):
        """Load configuration from a JSON file."""
        import json
        import os

        print("Loading configuration...")
        print(f"{os.getcwd()=}")

        try:
            with open(self.config_path, "r") as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error loading configuration: {e}")

        return self.config
