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


class Controller:
    """コントローラクラス (Controller Class)"""

    def __init__(self, config: dict) -> None:
        """コントローラを初期化する
        (Initialize Controller with given configuration)"""
        self._config: dict = config

    @property
    def version(self) -> str:
        """コントローラのバージョンを返す
        (Returns the controller version)"""
        return self._config["version"]

    @property
    def type(self) -> str:
        """コントローラタイプを返す
        (Returns the controller type)"""
        return self._config["controller"][0]["type"]

    def get_config(self) -> dict:
        """設定辞書を返す
        (Return the configuration dictionary)"""
        return self._config


class PIDController(Controller):
    """PIDコントローラクラス (PID Controller Class)"""

    def __init__(self, config: dict) -> None:
        """PIDControllerを初期化する
        (Initialize PIDController with given configuration)"""
        super().__init__(config)
        try:
            self._kvp: float = float(config["controller"][0]["kvp_N_(m_s)"])
            self._kvi: float = float(config["controller"][0]["kvi_N_(m_s)"])
            self._kvd: float = float(config["controller"][0]["kvd_N_(m_s)"])
            self._kpp: float = float(config["controller"][0]["kpp_N_m"])
            self._kpi: float = float(config["controller"][0]["kpi_N_m"])
            self._kpd: float = float(config["controller"][0]["kpd_N_m"])
        except KeyError as e:
            raise KeyError(f"Missing PID parameter in configuration: {e}")
        except ValueError:
            raise ValueError("PID parameters must be numbers")

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
