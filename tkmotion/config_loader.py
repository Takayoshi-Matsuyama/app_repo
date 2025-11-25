import json
from tkmotion.motion_flow_config import MotionFlowConfig


class ConfigLoader:
    """Configuration Loader for MotionFlow."""

    def __init__(self):
        """Initialize the ConfigLoader."""
        pass

    def load(self, filepath="tkmotion/default_config.json"):
        """Load configuration from a JSON file."""

        try:
            with open(filepath, "r") as f:
                config = json.load(f)
                return MotionFlowConfig(config)
        except Exception as e:
            print(f"Error loading configuration: {e}")
        return None
