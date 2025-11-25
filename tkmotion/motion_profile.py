class MotionProfile:
    """A base class for motion profiles."""

    def __init__(self, profile: dict):
        """Initialize the MotionProfile."""
        self.profile: dict = profile

    def get_profile(self) -> dict:
        """Returns the profile source object."""
        return self.profile

    @property
    def version(self) -> str:
        """Returns the motion profile version."""
        return self.profile["version"]

    @property
    def type(self) -> str:
        """Returns the motion profile type."""
        return self.profile["motion_profile"][0]["type"]

    def cmd_pos(self, t: float) -> float:
        """Calculate command position at time t."""
        return 0.0  # Default implementation for base class


class TrapezoidalMotionProfile(MotionProfile):
    def __init__(self, profile: dict):
        """Initialize the MotionProfile."""
        super().__init__(profile)

    @property
    def V(self) -> float:
        """Returns the max velocity. [m/s]"""
        return self.profile["motion_profile"][0]["max_velocity_m_s"]

    @property
    def A(self) -> float:
        """Returns the acceleration. [m/s2]"""
        return self.profile["motion_profile"][0]["acceleration_m_s2"]

    @property
    def L(self) -> float:
        """Returns the movement length. [m]"""
        return self.profile["motion_profile"][0]["length_m"]

    def cmd_pos(self, t: float) -> float:
        """Calculate command position at time t."""
        return 0.0  # TODO: Implement position calculation logic
