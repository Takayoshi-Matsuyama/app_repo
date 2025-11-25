from tkmotion.motion_flow_config import MotionFlowConfig
from tkmotion.motion_profile import MotionProfile
from tkmotion.config_loader import ConfigLoader
from tkmotion.motion_profile_loader import MotionProfileLoader


class MotionFlow:
    """A class to handle motion flow operations."""

    def __init__(self) -> None:
        """Initialize the MotionFlow."""
        self._motion_flow_config: MotionFlowConfig | None = None
        self._motion_profile: MotionProfile | None = None

    @property
    def config(self) -> MotionFlowConfig | None:
        """Returns the motion flow configuration."""
        return self._motion_flow_config

    @property
    def mprof(self) -> MotionProfile | None:
        """Returns the motion profile."""
        return self._motion_profile

    def load_config(self) -> None:
        """Load configuration using ConfigLoader."""

        loader = ConfigLoader()
        self._motion_flow_config = loader.load()

    def load_motion_profile(self) -> None:
        """Load motion profile using MotionProfileLoader."""

        profile_loader = MotionProfileLoader()
        self._motion_profile = profile_loader.load()

    def execute(self) -> None:
        print("Executing motion flow...")

        # TODO: 時系列を進める逐次処理

        # TODO: 目標位置生成
