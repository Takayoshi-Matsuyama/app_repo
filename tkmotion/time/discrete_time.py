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

from tkmotion.util.utility import Utility
from tkmotion.util.utility import ConfigVersionIncompatibleError


# 離散時間モジュールのバージョン情報
# (discrete time module version information)
module_version = "0.3.0"


class DiscreteTimeLoader:
    """離散時間設定の読込クラス (Loader for DiscreteTime)"""

    def __init__(self):
        """DiscreteTimeLoaderを初期化する
        (Initialize the DiscreteTimeLoader)"""
        pass

    @property
    def module_version(self) -> str:
        """離散時間モジュールのバージョンを返す
        (Returns the discrete time module version)"""
        return module_version

    def load(
        self, filepath="tkmotion/time/default_discrete_time_config.json", dtime_index=0
    ) -> DiscreteTime | None:
        """離散時間設定をJSONファイルから読み込む
        (Load configuration from a JSON file)

        Args:
            filepath (str): JSONファイルのパス (Path to the JSON file)
            dtime_index (int): 離散時間設定辞書のインデックス (Index of the discrete time setting dictionary)
        Returns:
            DiscreteTime | None: 離散時間オブジェクト (DiscreteTime object)
        """

        try:
            with open(filepath, "r") as f:
                config = json.load(f)
                # 設定バージョン互換性確認 (Check configuration version compatibility)
                is_compatible = Utility.is_config_compatible(
                    module_version, config[0]["discrete_time"][dtime_index]["version"]
                )
                if not is_compatible:
                    raise ConfigVersionIncompatibleError(
                        f"Incompatible discrete time config version: "
                        f"module_version={module_version}, "
                        f"config_version={config[0]['discrete_time'][dtime_index]['version']}"
                    )
                return DiscreteTime(config[0]["discrete_time"][dtime_index])
        except Exception as e:
            print(f"Error loading discrete time configuration: {type(e)} {e}")
        return None


class DiscreteTime:
    """離散時間クラス (Discrete Time Class)"""

    def __init__(self, config: dict):
        """離散時間設定を初期化する
        (Initialize DiscreteTime with given configuration)"""

        self._config: dict = config
        try:
            self._dt: float = float(self._config["time_step_us"]) / 1000000.0  # 秒単位
        except KeyError as e:
            raise KeyError(f"Missing 'time_step_us' in configuration: {type(e)} {e}")
        except ValueError as e:
            raise ValueError(f"'time_step_us' must be a number: {type(e)} {e}")
        try:
            self._duration_s: float = float(self._config["duration_s"])
        except KeyError as e:
            raise ValueError(f"Missing 'duration_s' in configuration: {type(e)} {e}")
        except ValueError as e:
            raise ValueError(f"'duration_s' must be a number: {type(e)} {e}")

    @property
    def module_version(self) -> str:
        """離散時間モジュールのバージョンを返す
        (Returns the discrete time module version)"""
        return module_version

    @property
    def config_version(self):
        """離散時間設定のバージョンを返す
        (Returns the version of the discrete time configurations)"""
        try:
            return self._config["version"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'version' in discrete time configuration: {type(e)} {e}"
            )

    @property
    def dt(self) -> float:
        """離散時間ステップ [s]
        (Returns the discrete time step [s])"""
        return self._dt

    @dt.setter
    def dt(self, value: float):
        """離散時間ステップ [s]
        (Set the discrete time step [s])"""
        if value <= 0:
            raise ValueError("dt must be a positive number.")
        self._dt = value

    @property
    def duration(self) -> float:
        """離散時間の継続時間 [s]
        (Returns the duration of the discrete time [s])"""
        return self._duration_s

    @duration.setter
    def duration(self, value: float):
        """離散時間の継続時間 [s]
        (Set the duration of the discrete time [s])"""
        if value <= 0:
            raise ValueError("duration must be a positive number.")
        self._duration_s = value

    def get_config(self) -> dict:
        """設定辞書を返す
        (Return the configuration dictionary)"""
        return self._config

    def get_time_step_generator(self):
        """時間ステップ生成器を返す (時間ステップを0からdurationまでdt刻みで生成する)
        (Generator that yields time steps from 0 to duration with step dt.)"""
        t = 0.0
        while t <= self._duration_s:
            yield t
            t += self._dt
