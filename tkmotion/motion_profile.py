class MotionProfile:
    def __init__(self, profile):
        """Initialize the MotionProfile."""
        self.profile = profile

    def get_profile(self):
        """Returns the profile source object."""
        return self.profile

    @property
    def prof_type(self):
        """Returns the motion profile type."""
        return self.profile["motion_profile"][0]["type"]

    @property
    def max_velocity_m_s(self):
        """Returns the volocity. [m/s]"""
        return self.profile["motion_profile"][0]["max_velocity_m_s"]

    @property
    def V(self):
        """Returns the volocity. [m/s]"""
        return self.profile["motion_profile"][0]["max_velocity_m_s"]

    @property
    def acceleration_m_s2(self):
        """Returns the acceleration. [m/s2]"""
        return self.profile["motion_profile"][0]["acceleration_m_s2"]

    @property
    def A(self):
        """Returns the acceleration. [m/s2]"""
        return self.profile["motion_profile"][0]["acceleration_m_s2"]

    @property
    def length_m(self):
        """Returns the movement length. [m]"""
        return self.profile["motion_profile"][0]["length_m"]

    @property
    def L(self):
        """Returns the movement length. [m]"""
        return self.profile["motion_profile"][0]["length_m"]
