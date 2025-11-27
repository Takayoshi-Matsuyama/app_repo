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

from tkmotion.controller import Controller
from tkmotion.controller import PIDController

import json


class ControllerLoader:
    """コントローラ読込クラス (Controller Loader Class)"""

    def __init__(self):
        """ControllerLoaderを初期化する
        (Initialize the ControllerLoader)"""
        pass

    def load(self, filepath="tkmotion/default_controller.json"):
        """コントローラ設定をJSONファイルから読み込む
        (Load Controller settings from a JSON file)"""
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
