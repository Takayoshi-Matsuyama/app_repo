from tkmotion.motion_flow_config import MotionFlowConfig
from tkmotion.motion_profile import MotionProfile
from tkmotion.config_loader import ConfigLoader
from tkmotion.motion_profile_loader import MotionProfileLoader


class MotionFlow:
    """A class to handle motion flow operations."""

    def __init__(self) -> None:
        """Initialize the MotionFlow."""
        self.config: MotionFlowConfig | None = None
        self.motion_profile: MotionProfile | None = None

    def load_config(self) -> None:
        """Load configuration using ConfigLoader."""

        loader = ConfigLoader()
        self.config = loader.load()

    def load_motion_profile(self) -> None:
        """Load motion profile using MotionProfileLoader."""

        profile_loader = MotionProfileLoader()
        self.motion_profile = profile_loader.load()

    def execute(self) -> None:
        print("Executing motion flow...")
