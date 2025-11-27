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


class PhysicalObject:
    """Physical Object Class"""

    def __init__(self, config: dict) -> None:
        """Initialize PhysicalObject with mass."""
        self.config: dict = config
        try:
            self._mass: float = float(config[0]["mass"])
        except KeyError:
            raise KeyError("Missing 'mass' in configuration")
        except ValueError:
            raise ValueError("'mass' must be a number")

        self._acc = 0.0
        self._prev_acc = 0.0
        self._vel = 0.0
        self._prev_vel = 0.0
        self._pos = 0.0
        self._prev_pos = 0.0

    @property
    def mass(self) -> float:
        """Return the mass of the physical object."""
        return self._mass

    @property
    def acc(self) -> float:
        """Return the acceleration of the physical object."""
        return self._acc

    @acc.setter
    def acc(self, value: float) -> None:
        """Set the acceleration of the physical object."""
        self._prev_acc = self._acc  # 前の値を保存
        self._acc = value

    @property
    def prev_acc(self) -> float:
        """Return the previous acceleration of the physical object."""
        return self._prev_acc

    @property
    def vel(self) -> float:
        """Return the velocity of the physical object."""
        return self._vel

    @vel.setter
    def vel(self, value: float) -> None:
        """Set the velocity of the physical object."""
        self._prev_vel = self._vel  # 前の値を保存
        self._vel = value

    @property
    def prev_vel(self) -> float:
        """Return the previous velocity of the physical object."""
        return self._prev_vel

    @property
    def pos(self) -> float:
        """Return the position of the physical object."""
        return self._pos

    @pos.setter
    def pos(self, value: float) -> None:
        """Set the position of the physical object."""
        self._pos = value

    @property
    def prev_pos(self) -> float:
        """Return the previous position of the physical object."""
        return self._prev_pos

    def get_config(self) -> dict:
        """Return the configuration dictionary."""
        return self.config
