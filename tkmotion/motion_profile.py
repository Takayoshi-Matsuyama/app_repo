# Copyright 2025 Takayoshi Matsuyama
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class VelocityZeroOrMinusError(Exception):
    """速度がゼロまたは負の値の場合に発生する例外
    (Exception raised for zero or negative velocity)"""

    pass


class AccelerationZeroOrMinusError(Exception):
    """加速度がゼロまたは負の値の場合に発生する例外
    (Exception raised for zero or negative acceleration)"""

    pass


class MovingLengthZeroOrMinusError(Exception):
    """移動距離がゼロまたは負の値の場合に発生する例外
    (Exception raised for zero or negative moving length)"""

    pass


class MotionProfile:
    """モーションプロファイルの基底クラス (A base class for motion profiles)"""

    def __init__(self, config: dict):
        """モーションプロファイルを初期化する
        (Initialize the MotionProfile)."""
        self._config: dict = config

    @property
    def version(self) -> str:
        """モーションプロファイルのバージョンを返す
        (Returns the motion profile version)"""
        return self._config["version"]

    @property
    def type(self) -> str:
        """モーションプロファイルタイプを返す
        (Returns the motion profile type)"""
        return self._config["motion_profile"][0]["type"]

    def get_config(self) -> dict:
        """プロファイルソースの辞書を返す
        Returns the profile source dictionary."""
        return self._config

    def calculate_cmd_vel_pos(self, t: float) -> tuple[float, float]:
        """速度と位置のタプルを返す
        (Return a tuple of velocity and position)"""
        # ベースクラスのデフォルト実装 (Default implementation for base class)
        return 0.0, 0.0


class TrapezoidalMotionProfile(MotionProfile):
    """台形モーションプロファイルのクラス (A class for trapezoidal motion profiles)"""

    def __init__(self, config: dict):
        """TrapezoidalMotionProfileを初期化する
        (Initialize the TrapezoidalMotionProfile)"""
        super().__init__(config)

        # 最大速度 (maximum velocity)
        try:
            _V: float = self._config["motion_profile"][0]["max_velocity_m_s"]
        except KeyError:
            raise KeyError("Missing 'max_velocity_m_s' in motion profile configuration")

        if _V <= 0.0:
            raise VelocityZeroOrMinusError("Velocity must be positive.")
        self.V: float = _V

        # 加速度 (acceleration)
        try:
            _A: float = self._config["motion_profile"][0]["acceleration_m_s2"]
        except KeyError:
            raise KeyError(
                "Missing 'acceleration_m_s2' in motion profile configuration"
            )

        if _A <= 0.0:
            raise AccelerationZeroOrMinusError("Acceleration must be positive.")
        self.A: float = _A

        # 移動距離 (moving length)
        try:
            _L: float = self._config["motion_profile"][0]["length_m"]
        except KeyError:
            raise KeyError("Missing 'length_m' in motion profile configuration")

        if _L <= 0.0:
            raise MovingLengthZeroOrMinusError("Moving length must be positive.")
        self.L: float = _L

        # 加減速時間 (Acceleration / Deceleration time)
        self.Ta: float = self.V / self.A
        # 移動時間 (Moving time)
        self.T: float = self.L / self.V + self.Ta
        # 等速時間 (Constant velocity time)
        self.Tc: float = self.T - 2 * self.Ta
        if self.Tc < 0:
            # 三角形の場合の補正 (Correction for triangular case)
            self.Ta = (self.L / self.A) ** 0.5
            self.Tc = 0.0
            self.T = 2 * self.Ta

    def calculate_cmd_vel_pos(self, t: float) -> tuple[float, float]:
        """速度と位置のタプルを返す
        (Return a tuple of velocity and position)

        Args:
            t (float): [s] 時間 (Time)
        Returns:
            tuple[float, float]: ([m/s], [m]) (速度、位置) (velocity, position)
        """

        # 加速 (acceleration)
        if t < self.Ta:
            vel = self.A * t
            pos = 0.5 * self.A * t**2
            return vel, pos
        # 等速 (constant velocity)
        elif t < (self.Ta + self.Tc):
            vel = self.A * self.Ta
            pos = 0.5 * self.A * self.Ta**2 + self.V * (t - self.Ta)
            return vel, pos
        # 減速 (deceleration)
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
        # 停止 (stop)
        else:
            vel = 0.0
            pos = self.L
            return vel, pos
