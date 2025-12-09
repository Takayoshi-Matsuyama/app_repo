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

from tkmotion.util.utility import Utility
from tkmotion.util.utility import ConfigVersionIncompatibleError


# 物理オブジェクトモジュールのバージョン情報
# (physical object module version information)
module_version = "0.2.0"


class PhysicalObject:
    """物理オブジェクトクラス (Physical Object Class)"""

    def __init__(self, config: dict) -> None:
        """PhysicalObjectを初期化する
        (Initialize PhysicalObject)"""
        self._config: dict = config
        try:
            # 設定バージョン互換性確認 (Check configuration version compatibility)
            is_compatible = Utility.is_config_compatible(
                module_version, self._config["version"]
            )
            if not is_compatible:
                raise ConfigVersionIncompatibleError(
                    f"Incompatible physical object config version: "
                    f"module_version={module_version}, "
                    f"config_version={self._config['version']}"
                )
            # 属性設定 (Set attributes)
            try:
                self._mass: float = float(self._config["mass_kg"])
            except KeyError as e:
                raise KeyError(
                    f"Missing 'mass_kg' in physical object configuration: {type(e)} {e}"
                )

            self._acc = 0.0
            self._prev_acc = 0.0
            self._vel = 0.0
            self._prev_vel = 0.0
            self._pos = 0.0
            self._prev_pos = 0.0
        except Exception as e:
            print(f"Error initializing physical object: {type(e)} {e}")
            raise e

    @property
    def module_version(self) -> str:
        """物理オブジェクトモジュールのバージョンを返す
        (Returns the physical object module version)"""
        return module_version

    @property
    def config_version(self) -> str:
        """物理オブジェクト設定のバージョンを返す
        (Returns the physical object configuration version)"""
        try:
            return self._config["version"]
        except KeyError as e:
            raise KeyError(
                f"Missing 'version' in physical object configuration: {type(e)} {e}"
            )

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


class MDSPhysicalObject(PhysicalObject):
    """質量・減衰器・ばね 物理オブジェクトクラス
    (Mass-Damper-Spring Physical Object Class)"""

    def __init__(self, config: dict) -> None:
        """MDSPhysicalObjectを初期化する
        (Initialize MDSPhysicalObject)"""
        super().__init__(config)
        try:
            # 属性設定 (Set attributes)
            try:
                self._damper: float = float(self._config["damper_Ns_m"])
            except KeyError as e:
                raise KeyError(
                    f"Missing 'damper_Ns_m' in MDS physical object configuration: {type(e)} {e}"
                )

            try:
                self._spring: float = float(self._config["spring_N_m"])
            except KeyError as e:
                raise KeyError(
                    f"Missing 'spring_N_m' in MDS physical object configuration: {type(e)} {e}"
                )

            try:
                self._spring_balance_pos: float = float(
                    self._config["spring_balance_pos_m"]
                )
            except KeyError:
                self._spring_balance_pos = (
                    0.0  # デフォルト値 0.0 m (Default value 0.0 m)
                )

        except Exception as e:
            print(f"Error initializing MDS physical object: {type(e)} {e}")
            raise e

    @property
    def damper(self) -> float:
        """物理オブジェクトの減衰器係数 [Ns/m]
        (Return the damper coefficient of the physical object)"""
        return self._damper

    @property
    def spring(self) -> float:
        """物理オブジェクトのばね係数 [N/m]
        (Return the spring coefficient of the physical object)"""
        return self._spring

    @property
    def spring_balance_pos(self) -> float:
        """物理オブジェクトのばね平衡位置 [m]
        (Return the spring balance position of the physical object)"""
        return self._spring_balance_pos

    def apply_force(self, ex_force: float, dt: float) -> None:
        """物理オブジェクトに力を適用し、状態を更新する
        (Apply force to the physical object and update status)"""

        # 力Fを与えると、質量mの物体に加速度aが生じる (F = m*a より a = F/m)
        # (when force F is applied, acceleration a occurs in mass m object)
        self.acc = ex_force / self.mass

        # 加速度aが生じると、速度vが変化 (v = u + a*t)
        # (when acceleration a occurs, velocity v changes)
        self.vel += self.acc * dt

        # 減衰器による力Fd = -c*v
        # (force by damper Fd = -c*v)
        damper_force = -self.damper * self.vel

        # ばねによる力Fs = -k*x
        # (force by spring Fs = -k*x)
        spring_force = -self.spring * (self.pos - self.spring_balance_pos)

        # 合力F = 外力 + 減衰器力 + ばね力
        # (net force F = external force + damper force + spring force)
        net_force = ex_force + damper_force + spring_force

        # 親クラスのapply_forceを呼び出して状態更新
        # (call parent class apply_force to update status)
        super().apply_force(net_force, dt)

    # TODO: 理論特性値（固有振動数、減衰比など）を計算するメソッドを追加
