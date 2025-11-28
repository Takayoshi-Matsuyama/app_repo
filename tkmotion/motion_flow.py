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

from tkmotion.discrete_time import DiscreteTimeLoader
from tkmotion.discrete_time import DiscreteTime
from tkmotion.controller import ControllerLoader
from tkmotion.controller import Controller
from tkmotion.plant import PlantLoader
from tkmotion.plant import Plant
from tkmotion.motion_profile import MotionProfileLoader
from tkmotion.motion_profile import MotionProfile


# モーションフローモジュールのバージョン情報
# (motion flow module version information)
module_version = "0.0.1"


class MotionFlow:
    """モーションフロー操作を扱うクラス
    (A class to handle motion flow operations)"""

    def __init__(self) -> None:
        """モーションフローを初期化する
        (Initialize the MotionFlow)"""
        self._discrete_time: DiscreteTime | None = None
        self._controller: Controller | None = None
        self._plant: Plant | None = None
        self._motion_profile: MotionProfile | None = None

    @property
    def module_version(self) -> str:
        """モーションフローモジュールのバージョンを返す
        (Returns the motion flow module version)"""
        return module_version

    @property
    def discrete_time(self) -> DiscreteTime | None:
        """離散時間設定を返す
        (Returns the discrete time configuration)"""
        return self._discrete_time

    @property
    def controller(self) -> Controller | None:
        """コントローラを返す
        (Returns the controller)"""
        return self._controller

    @property
    def plant(self) -> Plant | None:
        """プラントを返す
        (Returns the plant)"""
        return self._plant

    @property
    def mprof(self) -> MotionProfile | None:
        """モーションプロファイルを返す
        (Returns the motion profile)"""
        return self._motion_profile

    def load_discrete_time(self) -> None:
        """離散時間設定をロードする
        (Load discrete time configuration)"""

        self._discrete_time = DiscreteTimeLoader().load()
        if self._discrete_time is None:
            raise ValueError("Failed to load discrete time configuration.")

    def load_controller(self, filepath="tkmotion/default_controller.json") -> None:
        """コントローラ設定をロードする
        (Load controller configuration)"""

        self._controller = ControllerLoader().load(filepath)
        if self._controller is None:
            raise ValueError("Failed to load controller.")

    def load_plant(self, filepath="tkmotion/default_plant.json") -> None:
        """プラント設定をロードする
        (Load plant configuration)"""

        self._plant = PlantLoader().load(filepath)
        if self._plant is None:
            raise ValueError("Failed to load plant.")

    def load_motion_profile(self, filepath="tkmotion/default_motion_prof.json") -> None:
        """モーションプロファイルをロードする
        (Load motion profile)"""

        self._motion_profile = MotionProfileLoader().load(filepath)
        if self._motion_profile is None:
            raise ValueError("Failed to load motion profile.")

    def execute(self) -> pd.DataFrame:
        """モーションシミュレーションを実行する
        (Execute motion simulation)

        Returns:
            pd.DataFrame: シミュレーション結果のデータフレーム
            (DataFrame of simulation results)
        """

        if self._discrete_time is None:
            raise ValueError("Discrete time configuration not available.")

        if self._controller is None:
            raise ValueError("Controller not loaded. Call load_controller() first.")

        if self._plant is None:
            raise ValueError("Plant not loaded. Call load_plant() first.")

        if self._motion_profile is None:
            raise ValueError(
                "Motion profile not loaded. Call load_motion_profile() first."
            )

        # 時間ステップ生成器 (time step generator)
        time_steps_gen = self._discrete_time.get_time_step_generator()

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

        # コントローラ状態初期化 (initialize controller state)
        self._controller.reset()

        # 物理オブジェクト状態初期化 (initialize physical object state)
        self._plant.physical_obj.reset()

        # 時間ステップ毎のシミュレーション (simulation for each time step)
        for t in time_steps_gen:
            time_list.append(t)

            # 指令速度と位置 (command velocity and position)
            cmd_vel, cmd_pos = self._motion_profile.calculate_cmd_vel_pos(t)
            cmd_vel_list.append(cmd_vel)
            cmd_pos_list.append(cmd_pos)

            # サーボ推力計算 (servo force calculation)
            force = self._controller.calculate_force(
                cmd_vel,
                cmd_pos,
                self._plant.physical_obj.vel,
                self._plant.physical_obj.pos,
            )

            vel_error_list.append(self._controller.vel_error)
            pos_error_list.append(self._controller.pos_error)

            force_list.append(force)

            # 物理オブジェクト状態更新 (physical object state update)
            self._plant.physical_obj.apply_force(force, self._discrete_time.dt)
            obj_acc_list.append(self._plant.physical_obj.acc)
            obj_vel_list.append(self._plant.physical_obj.vel)
            obj_pos_list.append(self._plant.physical_obj.pos)

        # シミュレーション結果のデータフレーム作成 (create DataFrame of simulation results)
        result_df = pd.DataFrame(
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

        return result_df
