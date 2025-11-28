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

# 物理オブジェクトモジュールのバージョン情報
# (physical object module version information)
module_version = "0.0.1"


class PhysicalObject:
    """物理オブジェクトクラス (Physical Object Class)"""

    def __init__(self, config: dict) -> None:
        """PhysicalObjectを初期化する
        (Initialize PhysicalObject)"""
        self._config: dict = config
        try:
            self._mass: float = float(config[0]["mass_kg"])
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
    def module_version(self) -> str:
        """物理オブジェクトモジュールのバージョンを返す
        (Returns the physical object module version)"""
        return module_version

    @property
    def mass(self) -> float:
        """物理オブジェクトの質量 [kg]
        (Return the mass of the physical object)"""
        return self._mass

    @property
    def acc(self) -> float:
        """物理オブジェクトの加速度 [m/s^2]
        (Return the acceleration of the physical object)"""
        return self._acc

    @acc.setter
    def acc(self, value: float) -> None:
        """物理オブジェクトの加速度を設定 [m/s^2]
        (Set the acceleration of the physical object)"""
        self._prev_acc = self._acc  # 前の値を保存
        self._acc = value

    @property
    def prev_acc(self) -> float:
        """物理オブジェクトの前回の加速度 [m/s^2]
        (Return the previous acceleration of the physical object)"""
        return self._prev_acc

    @property
    def vel(self) -> float:
        """物理オブジェクトの速度 [m/s]
        (Return the velocity of the physical object)"""
        return self._vel

    @vel.setter
    def vel(self, value: float) -> None:
        """物理オブジェクトの速度を設定 [m/s]
        (Set the velocity of the physical object)"""
        self._prev_vel = self._vel  # 前の値を保存
        self._vel = value

    @property
    def prev_vel(self) -> float:
        """物理オブジェクトの前回の速度 [m/s]
        (Return the previous velocity of the physical object)"""
        return self._prev_vel

    @property
    def pos(self) -> float:
        """物理オブジェクトの位置 [m]
        (Return the position of the physical object)"""
        return self._pos

    @pos.setter
    def pos(self, value: float) -> None:
        """物理オブジェクトの位置を設定 [m]
        (Set the position of the physical object)"""
        self._prev_pos = self._pos  # 前の値を保存
        self._pos = value

    @property
    def prev_pos(self) -> float:
        """物理オブジェクトの前回の位置 [m]
        (Return the previous position of the physical object)"""
        return self._prev_pos

    def get_config(self) -> dict:
        """設定辞書を返す
        (Return the configuration dictionary)"""
        return self._config

    def reset(self) -> None:
        """物理オブジェクトの状態をリセットする
        (Reset the state of the physical object)"""
        self._acc = 0.0
        self._prev_acc = 0.0
        self._vel = 0.0
        self._prev_vel = 0.0
        self._pos = 0.0
        self._prev_pos = 0.0

    def apply_force(self, force: float, dt: float) -> None:
        """物理オブジェクトに力を適用し、状態を更新する
        (Apply force to the physical object and update status)"""

        # 力Fを与えると、質量mの物体に加速度aが生じる (F = m*a より a = F/m)
        # (when force F is applied, acceleration a occurs in mass m object)
        self.acc = force / self.mass

        # 加速度aが生じると、速度vが変化 (v = u + a*t)
        # (when acceleration a occurs, velocity v changes)
        self.vel += self.acc * dt

        # 速度vが変化すると、位置xが変化 (x = x0 + v*t)
        # (when velocity v changes, position x changes)
        # 前回速度による変化分 + 今回加速度による変化分
        # (position changes due to previous velocity
        #  + position changes due to current acceleration)
        self.pos += self.prev_vel * dt + 0.5 * self.acc * (dt**2)
