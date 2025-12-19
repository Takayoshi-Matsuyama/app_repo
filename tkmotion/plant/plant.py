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
from tkmotion.plant.physical_object import MDSPhysicalObject
from tkmotion.util.utility import Utility
from tkmotion.util.utility import ConfigVersionIncompatibleError


# プラントモジュールのバージョン情報
# (plant module version information)
module_version = "0.3.0"


class PlantLoader:
    """プラント読込クラス (Plant Loader Class)"""

    def __init__(self):
        """PlantLoaderを初期化する (Initializes the PlantLoader)"""
        pass

    @property
    def module_version(self) -> str:
        """プラントモジュールのバージョン (Plant module version)"""
        return module_version

    def load(
        self,
        filepath="tkmotion/plant/default_plant_config.json",
        plant_index=0,
        phyobj_index=0,
    ) -> Plant | None:
        """プラント設定をJSONファイルから読み込む (Loads Plant configuration from a JSON file)

        Args:
            filepath (str): JSONファイルのパス (Path to the JSON file)
            plant_index (int): プラント設定辞書のインデックス (Index of the plant setting dictionary)
            phyobj_index (int): 物理オブジェクト設定辞書のインデックス (Index of the physical object setting dictionary)
        """
        try:
            with open(filepath, "r") as f:
                config = json.load(f)
                # 設定バージョン互換性確認 (Check configuration version compatibility)
                is_compatible = Utility.is_config_compatible(
                    module_version, config[0]["plant"][plant_index]["version"]
                )
                if not is_compatible:
                    raise ConfigVersionIncompatibleError(
                        f"Incompatible plant config version: "
                        f"module_version={module_version}, "
                        f"config_version={config[0]['plant'][plant_index]['version']}"
                    )
                # プラントオブジェクト作成 (Create Plant object)
                return Plant(config[0]["plant"][plant_index], phyobj_index)
        except Exception as e:
            print(f"Error loading plant: {type(e)} {e}")
        return None


class Plant:
    """プラント (制御対象) (Plant (Target System)) Class"""

    def __init__(self, config: dict, phyobj_index=0) -> None:
        """Plantを初期化する (Initializes the Plant with given configuration)

        Args:
            config (dict): プラント設定辞書 (Plant configuration dictionary)
            phyobj_index (int): 物理オブジェクト設定辞書のインデックス (Index of the physical object setting dictionary)

        Raises:
            KeyError: プラント設定辞書に'physical_object'が存在しない場合に発生
              (If 'physical_object' does not exist in the plant configuration dictionary)
        """
        self._config: dict = config
        self._physical_object: PhysicalObject
        try:
            match self._config["physical_object"][phyobj_index]["type"]:
                case "MDS":
                    self._physical_object = MDSPhysicalObject(
                        self._config["physical_object"][phyobj_index]
                    )
                case _:
                    self._physical_object = PhysicalObject(
                        self._config["physical_object"][phyobj_index]
                    )
        except KeyError as e:
            raise KeyError(f"Missing 'physical_object' in configuration: {type(e)} {e}")

    @property
    def module_version(self) -> str:
        """プラントモジュールのバージョン (Plant module version)"""
        return module_version

    @property
    def config_version(self) -> str:
        """プラント設定のバージョン (Plant configuration version)

        Raises:
            KeyError: プラント設定辞書に'version'が存在しない場合に発生
              (If 'version' does not exist in the plant configuration dictionary)
        """
        try:
            return self._config["version"]
        except KeyError as e:
            raise KeyError(f"Missing 'version' in plant configuration: {type(e)} {e}")

    @property
    def physical_obj(self) -> PhysicalObject:
        """プラントの物理オブジェクト (Physical object of the plant)"""
        return self._physical_object

    def get_config(self) -> dict:
        """設定辞書を返す (Returns the configuration dictionary)"""
        return self._config
