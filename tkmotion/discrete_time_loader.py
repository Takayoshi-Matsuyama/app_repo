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

import json
from tkmotion.discrete_time import DiscreteTime


class DiscreteTimeLoader:
    """離散時間設定の読込クラス (Loader for DiscreteTime)"""

    def __init__(self):
        """DiscreteTimeLoaderを初期化する
        (Initialize the DiscreteTimeLoader)"""
        pass

    def load(self, filepath="tkmotion/default_discrete_time.json"):
        """離散時間設定をJSONファイルから読み込む
        (Load configuration from a JSON file)"""

        try:
            with open(filepath, "r") as f:
                config = json.load(f)
                # リスト先頭のディクショナリを渡す
                return DiscreteTime(config[0])
        except Exception as e:
            print(f"Error loading discrete time configuration: {e}")
        return None
