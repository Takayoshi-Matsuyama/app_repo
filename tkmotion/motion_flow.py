from tkmotion.motion_flow_config import MotionFlowConfig
from tkmotion.motion_profile import MotionProfile


class MotionFlow:
    """A class to handle motion flow operations."""

    def __init__(self):
        self.config: MotionFlowConfig = None
        self.motion_profile: MotionProfile = None

    def load_config(self):
        from tkmotion.config_loader import ConfigLoader

        loader = ConfigLoader()
        self.config = loader.load()

    def load_motion_profile(self):
        from tkmotion.motion_profile_loader import MotionProfileLoader

        profile_loader = MotionProfileLoader()
        self.motion_profile = profile_loader.load()

    def execute(self):
        print("Executing motion flow...")
