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


# コントローラモジュールのバージョン情報
# (Controller module version information)
module_version = "0.3.0"


class ControllerLoader:
    """コントローラ読込クラス (Controller Loader Class)"""

    def __init__(self):
        """ControllerLoaderを初期化する (Initializes the ControllerLoader)"""
        pass

    @property
    def module_version(self) -> str:
        """コントローラモジュールのバージョン (Controller module version)"""
        return module_version

    def load(
        self, filepath="tkmotion/ctrl/default_controller_config.json", ctrl_index=0
    ) -> Controller | None:
        """コントローラ設定をJSONファイルから読み込む (Loads Controller configuration from a JSON file)

        Args:
            filepath (str): JSONファイルパス (Path to the JSON file)
            ctrl_index (int): コントローラ設定辞書のインデックス (index of the controller configuration dictionary)

        Returns:
            Controller: コントローラオブジェクト (controller object)
        """
        try:
            with open(filepath, "r") as f:
                config = json.load(f)
                # 設定バージョン互換性確認 (Check configuration version compatibility)
                is_compatible = Utility.is_config_compatible(
                    module_version, config[0]["controller"][ctrl_index]["version"]
                )
                if not is_compatible:
                    raise ConfigVersionIncompatibleError(
                        f"Incompatible controller config version: "
                        f"module_version={module_version}, "
                        f"config_version={config[0]['controller'][ctrl_index]['version']}"
                    )
                # コントローラオブジェクト作成
                match config[0]["controller"][ctrl_index]["type"]:
                    case "PID":
                        return PIDController(config[0]["controller"][ctrl_index])
                    case "impulse":
                        return ImpulseController(config[0]["controller"][ctrl_index])
                    case "step":
                        return StepController(config[0]["controller"][ctrl_index])
                    case "sin":
                        return SinusoidalController(config[0]["controller"][ctrl_index])
                    case _:
                        return Controller(config[0]["controller"][ctrl_index])
        except Exception as e:
            print(f"Error loading controller: {type(e)} {e}")
        return None


class Controller:
    """コントローラクラス (Controller Class)"""

    def __init__(self, config: dict) -> None:
        """コントローラを初期化する (Initializes Controller with given configuration)"""
        self._config: dict = config
        self._force: float = 0.0

    @property
    def module_version(self) -> str:
        """コントローラモジュールのバージョン (Controller module version)"""
        return module_version

    @property
    def config_version(self) -> str:
        """コントローラ設定のバージョン (Controller configuration version)"""
        try:
            return self._config["version"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'version' in controller configuration: {type(e)} {e}"
            )

    @property
    def type(self) -> str:
        """コントローラタイプ (Controller type)

        Raises:
            KeyError: 設定辞書に'type'キーが存在しない場合に発生
              (If 'type' key is missing in the configuration dictionary)
        """
        try:
            return self._config["type"]
        except KeyError as e:
            raise KeyError(f"Missing 'type' in controller configuration: {type(e)} {e}")

    @property
    def vel_error(self) -> float:
        """現在の速度偏差 (Current velocity error)"""
        # 基本的なコントローラでは0を返す
        return 0.0

    @property
    def pos_error(self) -> float:
        """現在の位置偏差 (Current position error)"""
        # 基本的なコントローラでは0を返す
        return 0.0

    @property
    def vel_error_cumsum(self) -> float:
        """現在の速度偏差の累積値 (Current cumulative velocity error)"""
        # 基本的なコントローラでは0を返す
        return 0.0

    @property
    def pos_error_cumsum(self) -> float:
        """現在の位置偏差の累積値 (Current cumulative position error)"""
        # 基本的なコントローラでは0を返す
        return 0.0

    @property
    def vel_error_diff(self) -> float:
        """現在の速度偏差の微分値 (Current derivative of velocity error)"""
        # 基本的なコントローラでは0を返す
        return 0.0

    @property
    def pos_error_diff(self) -> float:
        """現在の位置偏差の微分値 (Current derivative of position error)"""
        # 基本的なコントローラでは0を返す
        return 0.0

    @property
    def force(self) -> float:
        """現在の制御力 (Current control force)"""
        return self._force

    def get_config(self) -> dict:
        """設定辞書を返す (Return the configuration dictionary)"""
        return self._config

    def get_observer(self) -> ControllerObserver:
        """コントローラ観測オブジェクトを返す (Return the controller observer object)"""
        return ControllerObserver(self)

    def reset(self) -> None:
        """コントローラの状態をリセットする (Reset the controller state)"""
        # 基本的なコントローラでは何もしない
        pass

    def calculate_force(
        self,
        t: float,
        cmd_vel: float,
        cmd_pos: float,
        plant_vel: float,
        plant_pos: float,
    ) -> float:
        """制御力を計算する (Calculate the control force)
        Args:
            t (float): 現在の経過時間 [s] (current elapsed time)
            cmd_vel (float): 指令速度 [m/s] (command velocity)
            cmd_pos (float): 指令位置 [m] (command position)
            plant_vel (float): プラントの現在速度 [m/s] (current velocity of the plant)
            plant_pos (float): プラントの現在位置 [m] (current position of the plant)
        """
        # 基本的なコントローラでは0を返す
        return 0.0


class ControllerObserver:
    """コントローラ観測クラス
    (Controller Observer Class)"""

    def __init__(self, controller: Controller) -> None:
        """ControllerObserverを初期化する (Initializes the ControllerObserver)"""
        self._controller: Controller = controller
        self._force_list: list[float] = []

    @property
    def module_version(self) -> str:
        """コントローラモジュールのバージョン (Controller module version)"""
        return module_version

    @property
    def controller(self) -> Controller:
        """観測対象のコントローラ (Observing controller)"""
        return self._controller

    def reset(self) -> None:
        """観測データをリセットする (Resets the observed data)"""
        self._force_list.clear()

    def observe(self) -> None:
        """コントローラの状態を観測し、データリストに追加する
        (Observes the controller state and adds to the data list)"""
        self._force_list.append(self._controller.force)

    def get_observed_data(self) -> dict:
        """観測データを辞書形式で返す (Returns the observed data in dictionary format)
        Returns:
            dict: 観測データ辞書
            (Observed data dictionary)"""
        return {
            "force_N": self._force_list,
        }


class PIDController(Controller):
    """PIDコントローラクラス (PID Controller Class)"""

    def __init__(self, config: dict) -> None:
        """PIDControllerを初期化する (Initializes PIDController with given configuration)

        Raises:
            KeyError: 必要なキーが設定辞書に存在しない場合に発生
              (If required keys are missing in the configuration dictionary)
            ValueError: 設定値が不正な場合に発生
              (If configuration values are invalid)
        """
        super().__init__(config)
        try:
            # Kvp [N/(m/s)] 速度比例ゲイン (velocity proportional gain)
            self._kvp: float = float(self._config["kvp_N_(m_s)"])
            # Kvi [N/(m/s)] 速度積分ゲイン (velocity integral gain)
            self._kvi: float = float(self._config["kvi_N_(m_s)"])
            # Kvd [N/(m/s)] 速度微分ゲイン (velocityderivative gain)
            self._kvd: float = float(self._config["kvd_N_(m_s)"])
            # Kpp [N/m] 位置比例ゲイン (position proportional gain)
            self._kpp: float = float(self._config["kpp_N_m"])
            # Kpi [N/m] 位置積分ゲイン (position integral gain)
            self._kpi: float = float(self._config["kpi_N_m"])
            # Kpd [N/m] 位置微分ゲイン (position derivative gain)
            self._kpd: float = float(self._config["kpd_N_m"])
        except KeyError as e:
            raise KeyError(f"Missing PID parameter in configuration: {type(e)} {e}")
        except ValueError as e:
            raise ValueError(f"PID parameters must be numbers: {type(e)} {e}")

        # コントローラの状態をリセットする
        self.reset()

    @property
    def kvp(self) -> float:
        """速度比例ゲイン (Velocity proportional gain)"""
        return self._kvp

    @property
    def kvi(self) -> float:
        """速度積分ゲイン (Velocity integral gain)"""
        return self._kvi

    @property
    def kvd(self) -> float:
        """速度微分ゲイン (Velocity derivative gain)"""
        return self._kvd

    @property
    def kpp(self) -> float:
        """位置比例ゲイン (Position proportional gain)"""
        return self._kpp

    @property
    def kpi(self) -> float:
        """位置積分ゲイン (Position integral gain)"""
        return self._kpi

    @property
    def kpd(self) -> float:
        """位置微分ゲイン (Position derivative gain)"""
        return self._kpd

    @property
    def vel_error(self) -> float:
        """現在の速度偏差 (Current velocity error)"""
        return self._vel_error

    @property
    def pos_error(self) -> float:
        """現在の位置偏差 (Current position error)"""
        return self._pos_error

    @property
    def vel_error_cumsum(self) -> float:
        """現在の速度偏差の累積値 (Current cumulative velocity error)"""
        return self._vel_error_cumsum

    @property
    def pos_error_cumsum(self) -> float:
        """現在の位置偏差の累積値 (Current cumulative position error)"""
        return self._pos_error_cumsum

    @property
    def vel_error_diff(self) -> float:
        """現在の速度偏差の微分値 (Current derivative of velocity error)"""
        return self._vel_error_diff

    @property
    def pos_error_diff(self) -> float:
        """現在の位置偏差の微分値 (Current derivative of position error)"""
        return self._pos_error_diff

    def get_observer(self) -> PIDControllerObserver:
        """PIDコントローラ観測オブジェクトを返す (Returns the PID controller observer object)"""
        return PIDControllerObserver(self)

    def reset(self) -> None:
        """コントローラの状態をリセットする (Resets the controller state)"""
        # 偏差情報 初期値 (error information initial value)
        self._vel_error = 0.0
        self._pos_error = 0.0

        # 累積情報 初期値 (cumulative information initial value)
        self._vel_error_cumsum = 0.0
        self._pos_error_cumsum = 0.0

        # 微分情報 初期値 (derivative information initial value)
        self._prev_vel_error = 0.0
        self._vel_error_diff = 0.0
        self._prev_pos_error = 0.0
        self._pos_error_diff = 0.0

    def calculate_force(
        self,
        t: float,
        cmd_vel: float,
        cmd_pos: float,
        plant_vel: float,
        plant_pos: float,
    ) -> float:
        """制御力を計算する (Calculates the control force)

        Args:
            t (float): 現在の経過時間 [s] (current elapsed time)
            cmd_vel (float): 指令速度 [m/s] (command velocity)
            cmd_pos (float): 指令位置 [m] (command position)
            plant_vel (float): プラントの現在速度 [m/s] (current velocity of the plant)
            plant_pos (float): プラントの現在位置 [m] (current position of the plant)

        Returns:
            float: 計算された制御力 [N] (calculated control force)
        """

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
        self._vel_error = cmd_vel - plant_vel
        self._vel_error_cumsum += self._vel_error
        self._vel_error_diff = self._vel_error - self._prev_vel_error
        self._prev_vel_error = self._vel_error

        # 位置偏差 (指令が先行) (position error, command leads)
        self._pos_error = cmd_pos - plant_pos
        self._pos_error_cumsum += self._pos_error
        self._pos_error_diff = self._pos_error - self._prev_pos_error
        self._prev_pos_error = self._pos_error

        # 速度比例制御 (velocity proportional control)
        force = self._kvp * self._vel_error

        # 速度積分制御 (velocity integral control)
        force += self._kvi * self._vel_error_cumsum

        # 速度微分制御 (velocity derivative control)
        force += self._kvd * self._vel_error_diff

        # 位置比例制御 (position proportional control)
        force += self._kpp * self._pos_error

        # 位置積分制御 (position integral control)
        force += self._kpi * self._pos_error_cumsum

        # 位置微分制御 (position derivative control)
        force += self._kpd * self._pos_error_diff

        # 推力確定
        self._force = force

        return self._force


class PIDControllerObserver(ControllerObserver):
    """PIDコントローラ観測クラス (PID Controller Observer Class)"""

    def __init__(self, controller: PIDController) -> None:
        """PIDControllerObserverを初期化する (Initializes the PIDControllerObserver)"""
        super().__init__(controller)
        self._controller: PIDController = self._controller
        self._vel_error_list: list[float] = []
        self._pos_error_list: list[float] = []
        self._vel_error_cumsum_list: list[float] = []
        self._pos_error_cumsum_list: list[float] = []
        self._vel_error_diff_list: list[float] = []
        self._pos_error_diff_list: list[float] = []

    @property
    def controller(self) -> PIDController:
        """観測対象のPIDコントローラ (Observing PID controller)"""
        return self._controller

    def reset(self) -> None:
        """観測データをリセットする (Resets the observed data)"""
        super().reset()
        self._vel_error_list.clear()
        self._pos_error_list.clear()
        self._vel_error_cumsum_list.clear()
        self._pos_error_cumsum_list.clear()
        self._vel_error_diff_list.clear()
        self._pos_error_diff_list.clear()

    def observe(self) -> None:
        """コントローラの状態を観測し、データリストに追加する
        (Observes the controller state and adds to the data list)"""
        self._vel_error_list.append(self._controller.vel_error)
        self._pos_error_list.append(self._controller.pos_error)
        self._vel_error_cumsum_list.append(self._controller.vel_error_cumsum)
        self._pos_error_cumsum_list.append(self._controller.pos_error_cumsum)
        self._vel_error_diff_list.append(self._controller.vel_error_diff)
        self._pos_error_diff_list.append(self._controller.pos_error_diff)
        self._force_list.append(self._controller.force)

    def get_observed_data(self) -> dict:
        """観測データを辞書形式で返す (Returns the observed data in dictionary format)

        Returns:
            dict: 観測データ辞書
            (Observed data dictionary)"""
        return {
            "velocity_error_m_s": self._vel_error_list,
            "position_error_m": self._pos_error_list,
            "vel_error_cumsum_m_s": self._vel_error_cumsum_list,
            "pos_error_cumsum_m": self._pos_error_cumsum_list,
            "vel_error_diff_m_s": self._vel_error_diff_list,
            "pos_error_diff_m": self._pos_error_diff_list,
            "force_N": self._force_list,
        }


class ImpulseController(Controller):
    """インパルスコントローラクラス (Impulse Controller Class)"""

    def __init__(self, config: dict) -> None:
        """ImpulseControllerを初期化する (Initializes the ImpulseController)

        Args:
            config (dict): インパルスコントローラ設定辞書 (Impulse controller configuration dictionary)

        Raises:
            KeyError: 必要なキーが設定辞書に存在しない場合に発生
              (If required keys are missing in the configuration dictionary)
        """
        super().__init__(config)

        # インパルス推力 (impulse force)
        try:
            _p_force: float = self._config["impulse_force_N"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'impulse_force_N' in motion profile "
                f"configuration: {type(e)} {e}"
            )
        self.p_force: float = _p_force

        # インパルスONタイムステップ数 (impulse on time step count)
        try:
            _on_timestep_count: int = self._config["impulse_on_timestep_count"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'impulse_on_timestep_count' in motion profile "
                f"configuration: {type(e)} {e}"
            )
        self.on_timestep_count: int = _on_timestep_count

        # 遅延時間 (delay time)
        try:
            _delay_s: float = self._config["delay_s"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'delay_s' in motion profile " f"configuration: {type(e)} {e}"
            )
        self.delay_s: float = _delay_s

        # 時間ステップカウンタ (time step counter)
        self._step_counter: int = 0

    def reset(self) -> None:
        """コントローラの状態をリセットする (Resets the controller state)"""
        self._step_counter = 0

    def calculate_force(
        self,
        t: float,
        cmd_vel: float,
        cmd_pos: float,
        plant_vel: float,
        plant_pos: float,
    ) -> float:
        """制御力を計算する (Calculates the control force)

        Args:
            t (float): 現在の経過時間 [s] (current elapsed time)
            cmd_vel (float): 指令速度 [m/s] (command velocity)
            cmd_pos (float): 指令位置 [m] (command position)
            plant_vel (float): プラントの現在速度 [m/s] (current velocity of the plant)
            plant_pos (float): プラントの現在位置 [m] (current position of the plant)

        Returns:
            float: 計算された制御力 [N] (calculated control force)
        """

        # 遅延時間中はゼロを返す (return zero during delay time)
        if t < self.delay_s:
            self._force = 0.0
        # 指定時間ステップの間はインパルス推力を出力する (return impulse force for specified time steps)
        elif self._step_counter < self.on_timestep_count:
            self._step_counter += 1
            self._force = self.p_force
        else:
            self._force = 0.0

        return self._force


class StepController(Controller):
    """ステップコントローラクラス (Step Controller Class)"""

    def __init__(self, config: dict) -> None:
        """StepControllerを初期化する (Initializes StepController)

        Args:
            config (dict): ステップコントローラ設定辞書 (Step controller configuration dictionary)

        Raises:
            KeyError: 必要なキーが設定辞書に存在しない場合に発生
              (If required keys are missing in the configuration dictionary)
        """
        super().__init__(config)

        # ステップ推力 (step force)
        try:
            _s_force: float = self._config["step_force_N"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'step_force_N' in motion profile "
                f"configuration: {type(e)} {e}"
            )
        self.s_force: float = _s_force

        # 遅延時間 (delay time)
        try:
            _delay_s: float = self._config["delay_s"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'delay_s' in motion profile " f"configuration: {type(e)} {e}"
            )
        self.delay_s: float = _delay_s

    def reset(self) -> None:
        """コントローラの状態をリセットする (Resets the controller state)"""
        pass

    def calculate_force(
        self,
        t: float,
        cmd_vel: float,
        cmd_pos: float,
        plant_vel: float,
        plant_pos: float,
    ) -> float:
        """制御力を計算する (Calculates the control force)

        Args:
            t (float): 現在の経過時間 [s] (current elapsed time)
            cmd_vel (float): 指令速度 [m/s] (command velocity)
            cmd_pos (float): 指令位置 [m] (command position)
            plant_vel (float): プラントの現在速度 [m/s] (current velocity of the plant)
            plant_pos (float): プラントの現在位置 [m] (current position of the plant)

        Returns:
            float: 計算された制御力 [N] (calculated control force)
        """

        if t < self.delay_s:
            # 遅延時間中はゼロを返す (return zero during delay time)
            self._force = 0.0
        else:
            # 遅延時間後はステップ値を返す (return step value after delay time)
            self._force = self.s_force

        return self._force


class SinusoidalController(Controller):
    """サイン波コントローラクラス (Sinusoidal Controller Class)"""

    def __init__(self, config: dict) -> None:
        """SinusoidalControllerを初期化する (Initializes SinusoidalController)

        Args:
            config (dict): サイン波コントローラ設定辞書 (Sinusoidal controller configuration dictionary)

        Raises:
            KeyError: 必要なキーが設定辞書に存在しない場合に発生
              (If required keys are missing in the configuration dictionary)
        """
        super().__init__(config)

        # サイン波振幅 (sinusoidal amplitude)
        try:
            _amplitude: float = self._config["amplitude_N"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'amplitude_N' in motion profile "
                f"configuration: {type(e)} {e}"
            )
        self.amplitude: float = _amplitude

        # サイン波周波数 (sinusoidal frequency)
        try:
            _frequency: float = self._config["frequency_Hz"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'frequency_Hz' in motion profile "
                f"configuration: {type(e)} {e}"
            )
        self.frequency: float = _frequency

    def reset(self) -> None:
        """コントローラの状態をリセットする (Resets the controller state)"""
        pass

    def calculate_force(
        self,
        t: float,
        cmd_vel: float,
        cmd_pos: float,
        plant_vel: float,
        plant_pos: float,
    ) -> float:
        """制御力を計算する (Calculates the control force)

        Args:
            t (float): 現在の経過時間 [s] (current elapsed time)
            cmd_vel (float): 指令速度 [m/s] (command velocity)
            cmd_pos (float): 指令位置 [m] (command position)
            plant_vel (float): プラントの現在速度 [m/s] (current velocity of the plant)
            plant_pos (float): プラントの現在位置 [m] (current position of the plant)

        Returns:
            float: 計算された制御力 [N] (calculated control force)"""

        # サイン波推力計算 (sinusoidal force calculation)
        self._force = self.amplitude * np.sin(2 * np.pi * self.frequency * t)
        return self._force
