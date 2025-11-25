class DiscreteTime:
    """離散時間クラス"""

    def __init__(self, dt):
        self.dt = dt

    def step(self, state, control):
        # Implement the discrete time step logic here
        new_state = state + control * self.dt
        return new_state
