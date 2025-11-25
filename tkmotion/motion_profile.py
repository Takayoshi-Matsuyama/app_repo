class VelocityZeroOrMinusError(Exception):
    """Exception raised for zero or negative velocity."""

    pass


class AccelerationZeroOrMinusError(Exception):
    """Exception raised for zero or negative acceleration."""

    pass


class MovingLengthZeroOrMinusError(Exception):
    """Exception raised for zero or negative moving length."""

    pass


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

    def cmd_vel_pos(self, t: float) -> tuple[float, float]:
        """Returns a tuple of (velocity, position)."""
        return 0.0, 0.0  # Default implementation for base class


class TrapezoidalMotionProfile(MotionProfile):
    def __init__(self, profile: dict):
        """Initialize the MotionProfile."""
        super().__init__(profile)
        _V: float = self.profile["motion_profile"][0]["max_velocity_m_s"]
        if _V <= 0.0:
            raise VelocityZeroOrMinusError("Velocity must be positive.")
        self.V: float = _V

        _A: float = self.profile["motion_profile"][0]["acceleration_m_s2"]
        if _A <= 0.0:
            raise AccelerationZeroOrMinusError("Acceleration must be positive.")
        self.A: float = _A

        _L: float = self.profile["motion_profile"][0]["length_m"]
        if _L <= 0.0:
            raise MovingLengthZeroOrMinusError("Moving length must be positive.")
        self.L: float = _L

        # Acceleration / Deceleration time
        self.Ta: float = self.V / self.A
        # Moving time
        self.T: float = self.L / self.V + self.Ta
        # Constant velocity time
        self.Tc: float = self.T - 2 * self.Ta
        if self.Tc < 0:
            # 三角形の場合の補正
            self.Ta = (self.L / self.A) ** 0.5
            self.Tc = 0.0
            self.T = 2 * self.Ta

    def cmd_vel_pos(self, t: float) -> tuple[float, float]:
        """Returns a tuple of (velocity, position).

        Args:
            t (float): Time in seconds.
        Returns:
            tuple[float, float]: (velocity in m/s, position in m)
        """

        # 加速
        if t < self.Ta:
            vel = self.A * t
            pos = 0.5 * self.A * t**2
            return vel, pos
        # 等速
        elif t < (self.Ta + self.Tc):
            vel = self.A * self.Ta
            pos = 0.5 * self.A * self.Ta**2 + self.V * (t - self.Ta)
            return vel, pos
        # 減速
        elif t <= self.T:
            td = t - self.Ta - self.Tc
            vel = self.A * (self.T - t)
            pos = (
                0.5 * self.A * self.Ta**2
                + self.V * self.Tc
                + self.V * td
                - 0.5 * self.A * td**2
            )
            return vel, pos
        else:
            vel = 0.0
            pos = self.L
            return vel, pos
