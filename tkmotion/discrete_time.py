class DiscreteTime:
    """離散時間クラス"""

    def __init__(self, config: dict):
        self.config: dict = config
        try:
            self._dt: float = float(config["time_step_us"]) / 1000000.0  # 秒単位
        except KeyError:
            raise ValueError("Missing 'time_step_us' in configuration")
        except ValueError:
            raise ValueError("'time_step_us' must be a number")
        try:
            self._duration_s: float = float(config["duration_s"])
        except KeyError:
            raise ValueError("Missing 'duration_s' in configuration")
        except ValueError:
            raise ValueError("'duration_s' must be a number")

    @property
    def dt(self) -> float:
        """Returns the discrete time step in seconds."""
        return self._dt

    @property
    def duration(self) -> float:
        """Returns the duration in seconds."""
        return self._duration_s

    def get_config(self) -> dict:
        """Returns the configuration dictionary."""
        return self.config

    def get_time_step_generator(self):
        """Generator that yields time steps from 0 to duration with step dt."""
        t = 0.0
        while t <= self._duration_s:
            yield t
            t += self._dt

    def step(self, state, control):
        # Implement the discrete time step logic here
        new_state = state + control * self.dt
        return new_state
