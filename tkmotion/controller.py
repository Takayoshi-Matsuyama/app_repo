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

import json

# コントローラモジュールのバージョン情報
# (Controller module version information)
module_version = "0.0.1"


class ControllerLoader:
    """コントローラ読込クラス (Controller Loader Class)"""

    def __init__(self):
        """ControllerLoaderを初期化する
        (Initialize the ControllerLoader)"""
        pass

    def load(self, filepath="tkmotion/default_controller.json") -> Controller | None:
        """コントローラ設定をJSONファイルから読み込む
        (Load Controller settings from a JSON file)

        Args:
            filepath (str): コントローラ設定のJSONファイルパス
            (Path to the JSON file for controller settings)

        Returns:
            Controller: 読み込まれたコントローラオブジェクト
            (Loaded controller object)
        """
        try:
            with open(filepath, "r") as f:
                config = json.load(f)
                # リスト先頭のディクショナリを渡す
                if config[0]["controller"][0]["type"] == "PID":
                    return PIDController(config[0])
                else:
                    return Controller(config[0])
        except Exception as e:
            print(f"Error loading controller: {e}")
        return None

    @property
    def module_version(self) -> str:
        """コントローラモジュールのバージョンを返す
        (Returns the controller module version)"""
        return module_version


class Controller:
    """コントローラクラス (Controller Class)"""

    def __init__(self, config: dict) -> None:
        """コントローラを初期化する
        (Initialize Controller with given configuration)"""
        self._config: dict = config

    @property
    def module_version(self) -> str:
        """コントローラモジュールのバージョンを返す
        (Returns the controller module version)"""
        return module_version

    @property
    def config_version(self) -> str:
        """コントローラ設定のバージョンを返す
        (Returns the controller configuration version)"""
        return self._config["version"]

    @property
    def type(self) -> str:
        """コントローラタイプを返す
        (Returns the controller type)"""
        return self._config["controller"][0]["type"]

    @property
    def vel_error(self) -> float:
        """現在の速度偏差を返す
        (Return the current velocity error)"""
        # 基本的なコントローラでは0を返す
        return 0.0

    @property
    def pos_error(self) -> float:
        """現在の位置偏差を返す
        (Return the current position error)"""
        # 基本的なコントローラでは0を返す
        return 0.0

    @property
    def vel_error_cumsum(self) -> float:
        """現在の速度偏差の累積値を返す
        (Return the current cumulative velocity error)"""
        # 基本的なコントローラでは0を返す
        return 0.0

    @property
    def pos_error_cumsum(self) -> float:
        """現在の位置偏差の累積値を返す
        (Return the current cumulative position error)"""
        # 基本的なコントローラでは0を返す
        return 0.0

    @property
    def vel_error_diff(self) -> float:
        """現在の速度偏差の微分値を返す
        (Return the current derivative of velocity error)"""
        # 基本的なコントローラでは0を返す
        return 0.0

    @property
    def pos_error_diff(self) -> float:
        """現在の位置偏差の微分値を返す
        (Return the current derivative of position error)"""
        # 基本的なコントローラでは0を返す
        return 0.0

    def get_config(self) -> dict:
        """設定辞書を返す
        (Return the configuration dictionary)"""
        return self._config

    def reset(self) -> None:
        """コントローラの状態をリセットする
        (Reset the controller state)"""
        # 基本的なコントローラでは何もしない
        pass

    def calculate_force(
        self, cmd_vel: float, cmd_pos: float, plant_vel: float, plant_pos: float
    ) -> float:
        """制御力を計算する
        (Calculate the control force)"""
        # 基本的なコントローラでは0を返す
        return 0.0


class PIDController(Controller):
    """PIDコントローラクラス (PID Controller Class)"""

    def __init__(self, config: dict) -> None:
        """PIDControllerを初期化する
        (Initialize PIDController with given configuration)"""
        super().__init__(config)
        try:
            # Kvp [N/(m/s)] 速度比例ゲイン (velocity proportional gain)
            self._kvp: float = float(config["controller"][0]["kvp_N_(m_s)"])
            # Kvi [N/(m/s)] 速度積分ゲイン (velocity integral gain)
            self._kvi: float = float(config["controller"][0]["kvi_N_(m_s)"])
            # Kvd [N/(m/s)] 速度微分ゲイン (velocityderivative gain)
            self._kvd: float = float(config["controller"][0]["kvd_N_(m_s)"])
            # Kpp [N/m] 位置比例ゲイン (position proportional gain)
            self._kpp: float = float(config["controller"][0]["kpp_N_m"])
            # Kpi [N/m] 位置積分ゲイン (position integral gain)
            self._kpi: float = float(config["controller"][0]["kpi_N_m"])
            # Kpd [N/m] 位置微分ゲイン (position derivative gain)
            self._kpd: float = float(config["controller"][0]["kpd_N_m"])
        except KeyError as e:
            raise KeyError(f"Missing PID parameter in configuration: {e}")
        except ValueError:
            raise ValueError("PID parameters must be numbers")

        # コントローラの状態をリセットする
        self.reset()

    @property
    def kvp(self) -> float:
        """速度比例ゲインを返す
        (Return the velocity proportional gain)"""
        return self._kvp

    @property
    def kvi(self) -> float:
        """速度積分ゲインを返す
        (Return the velocity integral gain)"""
        return self._kvi

    @property
    def kvd(self) -> float:
        """速度微分ゲインを返す
        (Return the velocity derivative gain)"""
        return self._kvd

    @property
    def kpp(self) -> float:
        """位置比例ゲインを返す
        (Return the position proportional gain)"""
        return self._kpp

    @property
    def kpi(self) -> float:
        """位置積分ゲインを返す
        (Return the position integral gain)"""
        return self._kpi

    @property
    def kpd(self) -> float:
        """位置微分ゲインを返す
        (Return the position derivative gain)"""
        return self._kpd

    @property
    def vel_error(self) -> float:
        """現在の速度偏差を返す
        (Return the current velocity error)"""
        return self._vel_error

    @property
    def pos_error(self) -> float:
        """現在の位置偏差を返す
        (Return the current position error)"""
        return self._pos_error

    @property
    def vel_error_cumsum(self) -> float:
        """現在の速度偏差の累積値を返す
        (Return the current cumulative velocity error)"""
        return self._vel_error_cumsum

    @property
    def pos_error_cumsum(self) -> float:
        """現在の位置偏差の累積値を返す
        (Return the current cumulative position error)"""
        return self._pos_error_cumsum

    @property
    def vel_error_diff(self) -> float:
        """現在の速度偏差の微分値を返す
        (Return the current derivative of velocity error)"""
        return self._vel_error_diff

    @property
    def pos_error_diff(self) -> float:
        """現在の位置偏差の微分値を返す
        (Return the current derivative of position error)"""
        return self._pos_error_diff

    def reset(self) -> None:
        """コントローラの状態をリセットする
        (Reset the controller state)"""
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
        self, cmd_vel: float, cmd_pos: float, plant_vel: float, plant_pos: float
    ) -> float:
        """制御力を計算する
        (Calculate the control force)

        Args:
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

        return force
