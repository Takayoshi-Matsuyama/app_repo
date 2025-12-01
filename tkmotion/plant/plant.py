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

from tkmotion.plant.physical_object import PhysicalObject
from tkmotion.util.utility import Utility
from tkmotion.util.utility import ConfigVersionIncompatibleError


# プラントモジュールのバージョン情報
# (plant module version information)
module_version = "0.1.0"


class PlantLoader:
    """プラント読込クラス (Plant Loader Class)"""

    def __init__(self):
        """PlantLoaderを初期化する
        (Initialize the PlantLoader)"""
        pass

    @property
    def module_version(self) -> str:
        """プラントモジュールのバージョンを返す
        (Returns the plant module version)"""
        return module_version

    def load(self, filepath="tkmotion/plant/default_plant.json") -> Plant | None:
        """プラント設定をJSONファイルから読み込む
        (Load Plant settings from a JSON file)"""
        try:
            with open(filepath, "r") as f:
                config = json.load(f)
                is_compatible = Utility.is_config_compatible(
                    module_version, config[0]["plant"][0]["version"]
                )
                if not is_compatible:
                    raise ConfigVersionIncompatibleError(
                        f"Incompatible plant config version: "
                        f"module_version={module_version}, "
                        f"config_version={config[0]['plant'][0]['version']}"
                    )
                return Plant(config[0]["plant"])
        except Exception as e:
            print(f"Error loading plant: {type(e)} {e}")
        return None


class Plant:
    """プラント (制御対象) (Plant (Target System)) Class"""

    def __init__(self, config: dict) -> None:
        """Plantを初期化する
        (Initialize Plant with given configuration)"""
        self._config: dict = config
        try:
            self._physical_object: PhysicalObject = PhysicalObject(
                self._config[0]["physical_object"]
            )
        except KeyError as e:
            raise ValueError(
                f"Missing 'physical_object' in configuration: {type(e)} {e}"
            )

    @property
    def module_version(self) -> str:
        """プラントモジュールのバージョンを返す
        (Returns the plant module version)"""
        return module_version

    @property
    def config_version(self) -> str:
        """プラント設定のバージョンを返す
        (Returns the plant configuration version)"""
        try:
            return self._config[0]["version"]
        except KeyError as e:
            raise KeyError(f"Missing 'version' in plant configuration: {type(e)} {e}")

    @property
    def physical_obj(self) -> PhysicalObject:
        """プラントの物理オブジェクトを返す
        (Return the physical object of the plant)"""
        return self._physical_object

    def get_config(self) -> dict:
        """設定辞書を返す
        (Return the configuration dictionary)"""
        return self._config
