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

import pandas as pd
from tkmotion.motion_flow_config import MotionFlowConfig
from tkmotion.target_system import TargetSystem
from tkmotion.motion_profile import MotionProfile
from tkmotion.config_loader import ConfigLoader
from tkmotion.target_system_loader import TargetSystemLoader
from tkmotion.motion_profile_loader import MotionProfileLoader


class MotionFlow:
    """A class to handle motion flow operations."""

    def __init__(self) -> None:
        """Initialize the MotionFlow."""
        self._motion_flow_config: MotionFlowConfig | None = None
        self._target_system: TargetSystem | None = None
        self._motion_profile: MotionProfile | None = None

    @property
    def config(self) -> MotionFlowConfig | None:
        """Returns the motion flow configuration."""
        return self._motion_flow_config

    @property
    def target_system(self) -> TargetSystem | None:
        """Returns the target system."""
        return self._target_system

    @property
    def mprof(self) -> MotionProfile | None:
        """Returns the motion profile."""
        return self._motion_profile

    def load_config(self) -> None:
        """Load configuration using ConfigLoader."""

        loader = ConfigLoader()
        self._motion_flow_config = loader.load()

    def load_target_system(self, filepath="tkmotion/default_target.json") -> None:
        """Load target system configuration into motion flow config."""

        loader = TargetSystemLoader()
        self._target_system = loader.load(filepath)

        if self._target_system is None:
            raise ValueError("Failed to load target system.")

    def load_motion_profile(self) -> None:
        """Load motion profile using MotionProfileLoader."""

        profile_loader = MotionProfileLoader()
        self._motion_profile = profile_loader.load()

    def execute(self) -> pd.DataFrame:
        print("Executing motion flow...")

        if self._motion_flow_config is None:
            raise ValueError(
                "Motion flow configuration not loaded. Call load_config() first."
            )

        if self._motion_flow_config.discrete_time is None:
            raise ValueError("Discrete time configuration not available.")

        if self._motion_profile is None:
            raise ValueError(
                "Motion profile not loaded. Call load_motion_profile() first."
            )

        if self._target_system is None:
            raise ValueError(
                "Target system not loaded. Call load_target_system() first."
            )

        motion_profile = self._motion_profile
        target_system = self._target_system

        # 時間ステップ生成器 (time step generator)
        time_steps_gen = (
            self._motion_flow_config.discrete_time.get_time_step_generator()
        )

        # データ収集リスト (lists for data acquisition)
        time_list = []
        cmd_vel_list = []
        cmd_pos_list = []
        pos_error_list = []
        vel_error_list = []
        force_list = []
        obj_acc_list = []
        obj_vel_list = []
        obj_pos_list = []

        # 累積情報 初期値 (cumulative information initial value)
        vel_error_cumsum = 0.0
        pos_error_cumsum = 0.0

        # 時間ステップ毎のシミュレーション (simulation for each time step)
        for t in time_steps_gen:
            time_list.append(t)

            # 指令速度と位置 (command velocity and position)
            cmd_vel, cmd_pos = motion_profile.cmd_vel_pos(t)
            cmd_vel_list.append(cmd_vel)
            cmd_pos_list.append(cmd_pos)

            # サーボ推力計算 (servo force calculation)

            # PID制御

            # P (比例 Proportional)
            # 瞬間的に偏差を比例倍した操作量を出力する。
            # 目標値に近づくと操作量自体も徐々に小さくなる。定常偏差が残りやすい。

            # I (積分 Integral)
            # 偏差を累積し、継続的に偏差をなくすような操作量を出力する。
            # 積分により位相が全周波数域で90度遅れる。

            # D (微分 Derivative)
            # 偏差の変化率に比例した操作量を出力する。
            # 偏差が変化する方向を予測する (偏差が拡大しそうなら早めに操作量を大きくする)。

            # 速度偏差 (指令が先行) (velocity error, command leads)
            vel_error = cmd_vel - target_system.physical_object.vel
            vel_error_list.append(vel_error)
            vel_error_cumsum += vel_error

            # 位置偏差 (指令が先行) (position error, command leads)
            pos_error = cmd_pos - target_system.physical_object.pos
            pos_error_list.append(pos_error)
            pos_error_cumsum += pos_error

            # 速度比例制御 (velocity proportional control)
            kvp = 10000.0  # [N/(m/s)] 比例ゲイン (proportional gain)
            force = kvp * vel_error

            # 速度積分制御 (velocity integral control)
            kvi = 1000.0  # [N/(m/s)] 積分ゲイン (integral gain)
            force += kvi * vel_error_cumsum

            # 位置比例制御 (position proportional control)
            kpp = 1000.0  # [N/m] 比例ゲイン (proportional gain)
            force += kpp * pos_error

            # 位置積分制御 (position integral control)
            kpi = 500.0  # [N/m] 積分ゲイン (integral gain)
            force += kpi * pos_error_cumsum

            force_list.append(force)

            # 力 --> 速度 --> 位置変換 (仮想現在位置 更新) (force --> velocity --> position conversion, update virtual current position)

            # 力Fを与えると、質量mの物体に加速度aが生じる (F = m*a なので a = F/m) (since F = m*a, a = F/m)
            acc = force / target_system.physical_object.mass

            # 加速度aが生じると、速度vが変化 (v = u + a*t) (when acceleration a occurs, velocity v changes)
            target_system.physical_object.vel += acc * (
                self._motion_flow_config.discrete_time.dt
            )

            # 速度vが変化すると、位置xが変化 (x = x0 + v*t) (when velocity v changes, position x changes)
            target_system.physical_object.pos += target_system.physical_object.vel * (
                self._motion_flow_config.discrete_time.dt
            )
            # (
            #     0.5 * acc * (self._motion_flow_config.discrete_time.dt**2)  # これは、速度変化分
            # )
            obj_acc_list.append(acc)
            obj_vel_list.append(target_system.physical_object.vel)
            obj_pos_list.append(target_system.physical_object.pos)

        df = pd.DataFrame(
            {
                "time_s": time_list,
                "cmd_velocity_m_s": cmd_vel_list,
                "cmd_position_m": cmd_pos_list,
                "position_error_m": pos_error_list,
                "velocity_error_m_s": vel_error_list,
                "force_N": force_list,
                "obj_acceleration_m_s2": obj_acc_list,
                "obj_velocity_m_s": obj_vel_list,
                "obj_position_m": obj_pos_list,
            }
        )

        print(f"Generated {len(time_list)} time steps.")

        return df
