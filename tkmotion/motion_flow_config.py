from tkmotion.discrete_time import DiscreteTime


class MotionFlowConfig:
    """Motion Flow Configuration Class"""

    def __init__(self, config) -> None:
        """Initialize MotionFlowConfig with given configuration."""
        self.config: dict = config
        self.discrete_time: DiscreteTime | None = DiscreteTime(config["discrete_time"])

    @property
    def version(self):
        """Return the version of the configuration."""
        return self.config["version"]

    def get_config(self):
        """Return the configuration dictionary."""
        return self.config
