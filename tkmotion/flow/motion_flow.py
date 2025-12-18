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

import pandas as pd

from tkmotion.time.discrete_time import DiscreteTimeLoader
from tkmotion.time.discrete_time import DiscreteTime
from tkmotion.ctrl.controller import ControllerLoader
from tkmotion.ctrl.controller import Controller
from tkmotion.plant.plant import PlantLoader
from tkmotion.plant.plant import Plant
from tkmotion.prof.motion_profile import MotionProfileLoader
from tkmotion.prof.motion_profile import MotionProfile


# モーションフローモジュールのバージョン情報
# (motion flow module version information)
module_version = "0.3.0"


class MotionFlow:
    """モーション制御指令の流れを司るクラス
    (Class that manages the flow of motion control commands)"""

    def __init__(self) -> None:
        """モーションフローを初期化する (Initialize the MotionFlow)"""
        self._discrete_time: DiscreteTime | None = None
        self._controller: Controller | None = None
        self._plant: Plant | None = None
        self._motion_profile: MotionProfile | None = None

    @property
    def module_version(self) -> str:
        """モーションフローモジュールのバージョン (Motion flow module version)"""
        return module_version

    @property
    def discrete_time(self) -> DiscreteTime | None:
        """離散時間設定 (Discrete time configuration)"""
        return self._discrete_time

    @property
    def mprof(self) -> MotionProfile | None:
        """モーションプロファイル (Motion profile)"""
        return self._motion_profile

    @property
    def controller(self) -> Controller | None:
        """コントローラ (Controller)"""
        return self._controller

    @property
    def plant(self) -> Plant | None:
        """プラント (Plant)"""
        return self._plant

    def load_discrete_time(
        self, filepath="tkmotion/time/default_discrete_time_config.json"
    ) -> None:
        """離散時間設定を読み込む (Load discrete time configuration)

        Args:
            filepath (str): 設定JSONファイルのパス
              (Path to the configuration JSON file)

        Returns:
            None

        Raises:
            ValueError: 離散時間設定の読込に失敗した場合に発生
              (If loading discrete time configuration fails)
        """
        self._discrete_time = DiscreteTimeLoader().load(filepath)
        if self._discrete_time is None:
            raise ValueError("Failed to load discrete time configuration.")

    def load_motion_profile(
        self, filepath="tkmotion/prof/default_motion_prof_config.json", prof_index=0
    ) -> None:
        """モーションプロファイル設定をロードする
        (Load motion profile configuration)

        Args:
            filepath (str): モーションプロファイル設定JSONファイルのパス (Path to the motion profile configuration JSON file)
            prof_index (int): プロファイル設定辞書のインデックス (Index of the profile setting dictionary)

        Returns:
            None

        Raises:
            ValueError: モーションプロファイルの読込に失敗した場合に発生
              (If loading motion profile fails)
        """
        self._motion_profile = MotionProfileLoader().load(filepath, prof_index)
        if self._motion_profile is None:
            raise ValueError("Failed to load motion profile.")

    def load_controller(
        self, filepath="tkmotion/ctrl/default_controller_config.json", ctrl_index=0
    ) -> None:
        """コントローラ設定をロードする
        (Load controller configuration)

        Args:
            filepath (str): コントローラ設定JSONファイルのパス (Path to the controller configuration JSON file)
            ctrl_index (int): コントローラ設定辞書のインデックス (Index of the controller setting dictionary)

        Returns:
            None

        Raises:
            ValueError: コントローラの読込に失敗した場合に発生
              (If loading controller fails)
        """
        self._controller = ControllerLoader().load(filepath, ctrl_index)
        if self._controller is None:
            raise ValueError("Failed to load controller.")

    def load_plant(
        self,
        filepath="tkmotion/plant/default_plant_config.json",
        plant_index=0,
        phyobj_index=0,
    ) -> None:
        """プラント設定をロードする
        (Load plant configuration)

        Args:
            filepath (str): プラント設定JSONファイルのパス (Path to the plant configuration JSON file)
            plant_index (int): プラント設定辞書のインデックス (Index of the plant setting dictionary)
            phyobj_index (int): 物理オブジェクト設定辞書のインデックス (Index of the physical object setting dictionary)

        Returns:
            None

        Raises:
            ValueError: プラントの読込に失敗した場合に発生
              (If loading plant fails)
        """
        self._plant = PlantLoader().load(filepath, plant_index, phyobj_index)
        if self._plant is None:
            raise ValueError("Failed to load plant.")

    def execute(self) -> pd.DataFrame:
        """モーションシミュレーションを実行する
        (Execute motion simulation)

        Returns:
            pd.DataFrame: シミュレーション結果のデータフレーム
            (DataFrame of simulation results)

        Raises:
            ValueError: 必要な設定がロードされていない場合に発生
              (If required configurations are not loaded)
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
        motion_prof_observer = self._motion_profile.get_observer()
        controller_observer = self._controller.get_observer()
        phyobj_observer = self._plant.physical_obj.get_observer()

        # コントローラ状態初期化 (initialize controller state)
        self._controller.reset()

        # プラント状態の初期化は、execute()呼び出し前に、excute()呼び出し側で行う
        # (The initialization of the plant state is performed by the caller before calling execute())

        # 時間ステップ毎のシミュレーション (simulation for each time step)
        for t in time_steps_gen:
            time_list.append(t)

            # 指令速度と位置 (command velocity and position)
            cmd_vel, cmd_pos = self._motion_profile.calculate_cmd_vel_pos(t)
            motion_prof_observer.observe()

            # サーボ推力計算 (servo force calculation)
            force = self._controller.calculate_force(
                t,
                cmd_vel,
                cmd_pos,
                self._plant.physical_obj.vel,
                self._plant.physical_obj.pos,
            )
            controller_observer.observe()

            # 物理オブジェクト状態更新 (physical object state update)
            phyobj_observer.observe()  # 経過時間tでの状態を観測 (observe state at elapsed time t)
            self._plant.physical_obj.apply_force(
                force, self._discrete_time.dt
            )  # 離散時間dtで状態更新 (update state with discrete time dt)

        # シミュレーション結果のデータフレーム作成 (create DataFrame of simulation results)
        result_df = pd.DataFrame(
            {
                "time_s": time_list,
            }
        )

        for key, value in motion_prof_observer.get_observed_data().items():
            result_df[key] = value

        for key, value in controller_observer.get_observed_data().items():
            result_df[key] = value

        for key, value in phyobj_observer.get_observed_data().items():
            result_df[key] = value

        return result_df
