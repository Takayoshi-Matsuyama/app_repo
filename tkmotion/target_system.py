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

from tkmotion.physical_object import PhysicalObject


class TargetSystem:
    """Target System Class"""

    def __init__(self, config: dict) -> None:
        """Initialize TargetSystem with given configuration."""
        self.config: dict = config
        self.physical_object: PhysicalObject = PhysicalObject(config["physical_object"])

    def get_config(self) -> dict:
        """Return the configuration dictionary."""
        return self.config
