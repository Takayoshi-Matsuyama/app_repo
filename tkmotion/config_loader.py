from tkmotion.motion_flow_config import MotionFlowConfig


class ConfigLoader:
    """Configuration Loader for MotionFlow."""

    def __init__(self):
        pass

    def load(self, config_path="tkmotion/default_config.json"):
        """Load configuration from a JSON file."""
        import json

        print("Loading configuration...")

        try:
            with open(config_path, "r") as f:
                config = json.load(f)
                return MotionFlowConfig(config)
        except Exception as e:
            print(f"Error loading configuration: {e}")
        return None
