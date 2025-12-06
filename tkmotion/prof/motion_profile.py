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

from __future__ import annotations

import numpy as np
import json

from tkmotion.util.utility import Utility
from tkmotion.util.utility import ConfigVersionIncompatibleError


# モーションプロファイルモジュールのバージョン情報
# (motion profile module version information)
module_version = "0.1.0"


class VelocityZeroOrMinusError(Exception):
    """速度がゼロまたは負の値の場合に発生する例外
    (Exception raised for zero or negative velocity)"""

    pass


class AccelerationZeroOrMinusError(Exception):
    """加速度がゼロまたは負の値の場合に発生する例外
    (Exception raised for zero or negative acceleration)"""

    pass


class MovingLengthZeroError(Exception):
    """移動距離がゼロの場合に発生する例外
    (Exception raised for zero moving length)"""

    pass


class MotionProfileLoader:
    """モーションプロファイル読込クラス (Loader for MotionProfile)"""

    def __init__(self):
        """MotionProfileLoaderを初期化する
        (Initialize the MotionProfileLoader)"""
        pass

    @property
    def module_version(self) -> str:
        """モーションプロファイルモジュールのバージョンを返す
        (Returns the motion profile module version)"""
        return module_version

    def load(
        self, filepath="tkmotion/prof/default_motion_prof.json", prof_index=0
    ) -> MotionProfile | None:
        """JSONファイルからモーションプロファイル設定を読み込む
        (Load motion profile from a JSON file)

        Args:
            filepath (str): JSONファイルのパス (Path to the JSON file)
            prof_index (int): プロファイル設定辞書のインデックス (Index of the profile setting dictionary)
        Returns:
            MotionProfile | None: モーションプロファイルオブジェクト (MotionProfile object)
        """
        try:
            with open(filepath, "r") as f:
                config = json.load(f)
                # 設定バージョン互換性確認 (Check configuration version compatibility)
                is_compatible = Utility.is_config_compatible(
                    module_version, config[0]["motion_profile"][prof_index]["version"]
                )
                if not is_compatible:
                    raise ConfigVersionIncompatibleError(
                        f"Incompatible motion profile config version: "
                        f"module_version={module_version}, "
                        f"config_version={config[0]['motion_profile'][prof_index]['version']}"
                    )
                # モーションプロファイルオブジェクト作成 (Create motion profile object)
                match config[0]["motion_profile"][prof_index]["type"]:
                    case "trapezoid":
                        return TrapezoidalMotionProfile(
                            config[0]["motion_profile"][prof_index]
                        )
                    case "impulse":
                        return ImpulseMotionProfile(
                            config[0]["motion_profile"][prof_index]
                        )
                    case _:
                        return MotionProfile(config[0]["motion_profile"][prof_index])
        except Exception as e:
            print(f"Error loading motion profile: {type(e)} {e}")
        return None


class MotionProfile:
    """モーションプロファイルの基底クラス (A base class for motion profiles)"""

    def __init__(self, config: dict):
        """モーションプロファイルを初期化する
        (Initialize the MotionProfile)."""
        self._config: dict = config

    @property
    def module_version(self) -> str:
        """モーションプロファイルモジュールのバージョンを返す
        (Returns the motion profile module version)"""
        return module_version

    @property
    def config_version(self) -> str:
        """モーションプロファイル設定のバージョンを返す
        (Returns the motion profile configuration version)"""
        try:
            return self._config["version"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'version' in motion profile configuration: {type(e)} {e}"
            )

    @property
    def type(self) -> str:
        """モーションプロファイルタイプを返す
        (Returns the motion profile type)"""
        try:
            return self._config["type"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'type' in motion profile configuration: {type(e)} {e}"
            )

    def get_config(self) -> dict:
        """プロファイルソースの辞書を返す
        (Returns the profile source dictionary)"""
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
            _V: float = self._config["max_velocity_m_s"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'max_velocity_m_s' in motion profile "
                f"configuration: {type(e)} {e}"
            )

        if _V <= 0.0:
            raise VelocityZeroOrMinusError("Velocity must be positive.")
        self.V: float = _V

        # 加速度 (acceleration)
        try:
            _A: float = self._config["acceleration_m_s2"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'acceleration_m_s2' in motion profile "
                f"configuration: {type(e)} {e}"
            )

        if _A <= 0.0:
            raise AccelerationZeroOrMinusError("Acceleration must be positive.")
        self.A: float = _A

        # 移動距離 (moving length)
        try:
            _L: float = self._config["length_m"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'length_m' in motion profile configuration: {type(e)} {e}"
            )

        if _L == 0.0:
            raise MovingLengthZeroError("Moving length must be non-zero.")
        self.L: float = np.abs(_L)
        self.dir: float = np.sign(_L)

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
            vel = self.dir * self.A * t
            pos = self.dir * (0.5 * self.A * t**2)
            return vel, pos
        # 等速 (constant velocity)
        elif t < (self.Ta + self.Tc):
            vel = self.dir * self.A * self.Ta
            pos = self.dir * (0.5 * self.A * self.Ta**2 + self.V * (t - self.Ta))
            return vel, pos
        # 減速 (deceleration)
        elif t <= self.T:
            td = t - self.Ta - self.Tc
            vel = self.dir * self.A * (self.T - t)
            pos = self.dir * (
                0.5 * self.A * self.Ta**2
                + self.V * self.Tc
                + self.V * td
                - 0.5 * self.A * td**2
            )
            return vel, pos
        # 停止 (stop)
        else:
            vel = 0.0
            pos = self.dir * self.L
            return vel, pos


class ImpulseMotionProfile(MotionProfile):
    """インパルスモーションプロファイルのクラス
    (A class for impulse motion profiles)"""

    def __init__(self, config: dict):
        """ImpulseMotionProfileを初期化する
        (Initialize the ImpulseMotionProfile)"""
        super().__init__(config)

        # インパルス速度 (impulse velocity)
        try:
            _p_vel: float = self._config["impulse_vel_m_s"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'impulse_vel_m_s' in motion profile "
                f"configuration: {type(e)} {e}"
            )
        self.p_vel: float = _p_vel

        # インパルス位置 (impulse position)
        try:
            _p_pos: float = self._config["impulse_pos_m"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'impulse_pos_m' in motion profile "
                f"configuration: {type(e)} {e}"
            )
        self.p_pos: float = _p_pos

        # インパルスタイムステップ (impulse time step)
        try:
            _t_step: int = self._config["impulse_timestep"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'impulse_timestep' in motion profile "
                f"configuration: {type(e)} {e}"
            )
        self.t_step: int = _t_step

        # 時間ステップカウンタ (time step counter)
        self._step_counter: int = 0

    def calculate_cmd_vel_pos(self, t: float) -> tuple[float, float]:
        """速度と位置のタプルを返す
        (Return a tuple of velocity and position)

        Args:
            t (float): [s] 時間 (Time)
        Returns:
            tuple[float, float]: ([m/s], [m]) (速度、位置) (velocity, position)
        """

        # 指定時間ステップの間はインパルス値を返す (return impulse values for specified time steps)
        if self._step_counter < self.t_step:
            self._step_counter += 1
            return self.p_vel, self.p_pos
        else:
            return 0.0, 0.0
