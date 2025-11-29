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

from tkmotion.utility import Utility

# 離散時間モジュールのバージョン情報
# (discrete time module version information)
module_version = "0.0.1"


class DiscreteTimeLoader:
    """離散時間設定の読込クラス (Loader for DiscreteTime)"""

    def __init__(self):
        """DiscreteTimeLoaderを初期化する
        (Initialize the DiscreteTimeLoader)"""
        pass

    def load(
        self, filepath="tkmotion/default_discrete_time.json"
    ) -> DiscreteTime | None:
        """離散時間設定をJSONファイルから読み込む
        (Load configuration from a JSON file)"""

        try:
            with open(filepath, "r") as f:
                config = json.load(f)
                is_compatible = Utility.is_config_compatible(
                    module_version, config[0]["discrete_time"][0]["version"]
                )
                if not is_compatible:
                    raise ValueError(
                        f"Incompatible discrete time config version: "
                        f"module_version={module_version}, "
                        f"config_version={config[0]['discrete_time'][0]['version']}"
                    )
                return DiscreteTime(config[0]["discrete_time"])
        except Exception as e:
            print(f"Error loading discrete time configuration: {e}")
        return None

    @property
    def module_version(self) -> str:
        """離散時間モジュールのバージョンを返す
        (Returns the discrete time module version)"""
        return module_version


class DiscreteTime:
    """離散時間クラス (Discrete Time Class)"""

    def __init__(self, config: dict):
        """離散時間設定を初期化する
        (Initialize DiscreteTime with given configuration)"""

        self._config: dict = config
        try:
            self._dt: float = (
                float(self._config[0]["time_step_us"]) / 1000000.0
            )  # 秒単位
        except KeyError:
            raise KeyError("Missing 'time_step_us' in configuration")
        except ValueError:
            raise ValueError("'time_step_us' must be a number")
        try:
            self._duration_s: float = float(self._config[0]["duration_s"])
        except KeyError:
            raise ValueError("Missing 'duration_s' in configuration")
        except ValueError:
            raise ValueError("'duration_s' must be a number")

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
            return self._config[0]["version"]
        except KeyError:
            raise KeyError("Missing 'version' in discrete time configuration")

    @property
    def dt(self) -> float:
        """離散時間ステップを秒単位で返す
        (Returns the discrete time step in seconds)"""
        return self._dt

    @property
    def duration(self) -> float:
        """離散時間の継続時間を秒単位で返す
        (Returns the duration of the discrete time in seconds)"""
        return self._duration_s

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
