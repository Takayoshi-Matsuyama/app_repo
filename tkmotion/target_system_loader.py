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
from tkmotion.target_system import TargetSystem


class TargetSystemLoader:
    """Target System Loader Class"""

    def __init__(self):
        """Initialize the TargetSystemLoader."""
        pass

    def load(self, filepath="tkmotion/default_target.json"):
        """Load TargetSystem from a JSON file."""

        try:
            with open(filepath, "r") as f:
                config = json.load(f)
                # リスト先頭のディクショナリを渡す
                return TargetSystem(config[0])
        except Exception as e:
            print(f"Error loading target system: {e}")
        return None
