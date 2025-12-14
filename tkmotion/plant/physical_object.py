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
        (Mass of the physical object)"""
        return self._mass

    @mass.setter
    def mass(self, value: float) -> None:
        """物理オブジェクトの質量 [kg]
        (Mass of the physical object)"""
        self._mass = value

    @property
    def acc(self) -> float:
        """物理オブジェクトの加速度 [m/s^2]
        (Acceleration of the physical object)"""
        return self._acc

    @acc.setter
    def acc(self, value: float) -> None:
        """物理オブジェクトの加速度 [m/s^2]
        (Acceleration of the physical object)"""
        self._prev_acc = self._acc  # 前の値を保存
        self._acc = value

    @property
    def prev_acc(self) -> float:
        """物理オブジェクトの前回の加速度 [m/s^2]
        (Previous acceleration of the physical object)"""
        return self._prev_acc

    @property
    def vel(self) -> float:
        """物理オブジェクトの速度 [m/s]
        (Velocity of the physical object)"""
        return self._vel

    @vel.setter
    def vel(self, value: float) -> None:
        """物理オブジェクトの速度 [m/s]
        (Velocity of the physical object)"""
        self._prev_vel = self._vel  # 前の値を保存
        self._vel = value

    @property
    def prev_vel(self) -> float:
        """物理オブジェクトの前回の速度 [m/s]
        (Previous velocity of the physical object)"""
        return self._prev_vel

    @property
    def pos(self) -> float:
        """物理オブジェクトの位置 [m]
        (Position of the physical object)"""
        return self._pos

    @pos.setter
    def pos(self, value: float) -> None:
        """物理オブジェクトの位置 [m]
        (Position of the physical object)"""
        self._prev_pos = self._pos  # 前の値を保存
        self._pos = value

    @property
    def prev_pos(self) -> float:
        """物理オブジェクトの前回の位置 [m]
        (Previous position of the physical object)"""
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

    def set_state(self, acc: float, vel: float, pos: float) -> None:
        """物理オブジェクトの状態を設定する
        (Set the state of the physical object)

        Args:
            acc (float): 加速度 [m/s^2] (acceleration)
            vel (float): 速度 [m/s] (velocity)
            pos (float): 位置 [m] (position)

        Returns: None
        """
        self.acc = acc
        self._prev_acc = acc
        self.vel = vel
        self._prev_vel = vel
        self.pos = pos
        self._prev_pos = pos

    def get_observer(self) -> "PhysicalObjectObserver":
        """物理オブジェクトの観測者を取得する
        (Get the observer of the physical object)

        Returns:
            PhysicalObjectObserver: 物理オブジェクトの観測者
            (Observer of the physical object)
        """
        return PhysicalObjectObserver(self)

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


class PhysicalObjectObserver:
    """物理オブジェクト観測クラス
    (Physical Object Observer Class)"""

    def __init__(self, physical_obj: PhysicalObject | MDSPhysicalObject) -> None:
        """PhysicalObjectObserverを初期化する
        (Initialize PhysicalObjectObserver)"""
        self._physical_obj: PhysicalObject | MDSPhysicalObject = physical_obj
        self._obj_acc_list: list[float] = []
        self._obj_vel_list: list[float] = []
        self._obj_pos_list: list[float] = []

    @property
    def physical_obj(self) -> PhysicalObject | MDSPhysicalObject:
        """観測対象の物理オブジェクトを返す
        (Return the observed physical object)"""
        return self._physical_obj

    def reset(self) -> None:
        """観測データをリセットする
        (Reset observation data)"""
        self._obj_acc_list.clear()
        self._obj_vel_list.clear()
        self._obj_pos_list.clear()

    def observe(self) -> None:
        """物理オブジェクトの状態を観測し、データリストに追加する
        (Observe the state of the physical object and add to data list)"""
        self._obj_acc_list.append(self._physical_obj.acc)
        self._obj_vel_list.append(self._physical_obj.vel)
        self._obj_pos_list.append(self._physical_obj.pos)

    def get_observation_data(self) -> dict:
        """観測データリストを返す
        (Return the observation data list)

        Returns:
            list: 観測データリスト
            (Observation data list)
        """
        return {
            "obj_acceleration_m_s2": self._obj_acc_list,
            "obj_velocity_m_s": self._obj_vel_list,
            "obj_position_m": self._obj_pos_list,
        }


class MDSPhysicalObject(PhysicalObject):
    """質量・減衰器・ばね 物理オブジェクトクラス
    (Mass-Damper-Spring Physical Object Class)"""

    def __init__(self, config: dict) -> None:
        """MDSPhysicalObjectを初期化する
        (Initialize MDSPhysicalObject)"""
        super().__init__(config)
        try:
            # ダンパ係数 (damper coefficient)
            try:
                self._damper: float = float(self._config["damper_Ns_m"])
            except KeyError as e:
                raise KeyError(
                    f"Missing 'damper_Ns_m' in MDS physical object configuration: {type(e)} {e}"
                )

            # ばね係数 (spring coefficient)
            try:
                self._spring: float = float(self._config["spring_N_m"])
            except KeyError as e:
                raise KeyError(
                    f"Missing 'spring_N_m' in MDS physical object configuration: {type(e)} {e}"
                )

            # ばね平衡位置 (spring balance position)
            try:
                self._spring_balance_pos: float = float(
                    self._config["spring_balance_pos_m"]
                )
            except KeyError as e:
                raise KeyError(
                    f"Missing 'spring_balance_pos_m' in MDS physical object configuration: {type(e)} {e}"
                )

            # 静止摩擦係数 (static friction coefficient)
            try:
                self._static_friction_coeff: float = float(
                    self._config["static_friction_coeff"]
                )
            except KeyError as e:
                raise KeyError(
                    f"Missing 'static_friction_coeff' in MDS physical object configuration: {type(e)} {e}"
                )

            # 動摩擦係数 (dynamic friction coefficient)
            try:
                self._dynamic_friction_coeff: float = float(
                    self._config["dynamic_friction_coeff"]
                )
            except KeyError as e:
                raise KeyError(
                    f"Missing 'dynamic_friction_coeff' in MDS physical object configuration: {type(e)} {e}"
                )

            self._damper_force = 0.0
            self._spring_force = 0.0
            self._net_force = 0.0

        except Exception as e:
            print(f"Error initializing MDS physical object: {type(e)} {e}")
            raise e

    @property
    def damper(self) -> float:
        """物理オブジェクトのダンパ係数 [Ns/m]
        (Damper coefficient of the physical object)"""
        return self._damper

    @damper.setter
    def damper(self, value: float):
        """物理オブジェクトのダンパ係数 [Ns/m]
        (Damper coefficient of the physical object)"""
        self._damper = value

    @property
    def spring(self) -> float:
        """物理オブジェクトのばね係数 [N/m]
        (Spring coefficient of the physical object)"""
        return self._spring

    @spring.setter
    def spring(self, value: float):
        """物理オブジェクトのばね係数 [N/m]
        (Spring coefficient of the physical object)"""
        self._spring = value

    @property
    def spring_balance_pos(self) -> float:
        """物理オブジェクトのばね平衡位置 [m]
        (Spring balance position of the physical object)"""
        return self._spring_balance_pos

    @spring_balance_pos.setter
    def spring_balance_pos(self, value: float):
        """物理オブジェクトのばね平衡位置 [m]
        (Spring balance position of the physical object)"""
        self._spring_balance_pos = value

    @property
    def static_friction_coeff(self) -> float:
        """物理オブジェクトの静止摩擦係数
        (Static friction coefficient of the physical object)"""
        return self._static_friction_coeff

    @static_friction_coeff.setter
    def static_friction_coeff(self, value: float):
        """物理オブジェクトの静止摩擦係数
        (Static friction coefficient of the physical object)"""
        self._static_friction_coeff = value

    @property
    def dynamic_friction_coeff(self) -> float:
        """物理オブジェクトの動摩擦係数
        (Dynamic friction coefficient of the physical object)"""
        return self._dynamic_friction_coeff

    @dynamic_friction_coeff.setter
    def dynamic_friction_coeff(self, value: float):
        """物理オブジェクトの動摩擦係数
        (Dynamic friction coefficient of the physical object)"""
        self._dynamic_friction_coeff = value

    def reset(self) -> None:
        """物理オブジェクトの状態をリセットする
        (Reset the state of the physical object)"""
        super().reset()
        self._damper_force = 0.0
        self._spring_force = 0.0
        self._net_force = 0.0

    def get_observer(self):
        """物理オブジェクトの観測者を取得する
        (Get the observer of the physical object)

        Returns:
            MDSPhysicalObjectObserver: 物理オブジェクトの観測者
            (Observer of the physical object)
        """
        return MDSPhysicalObjectObserver(self)

    def apply_force(self, ex_force: float, dt: float) -> None:
        """物理オブジェクトに力を適用し、状態を更新する
        (Apply force to the physical object and update status)"""

        # 減衰器による力Fd = -c*v
        # (force by damper Fd = -c*v)
        self._damper_force = -self.damper * self.vel

        # ばねによる力Fs = -k*x
        # (force by spring Fs = -k*x)
        self._spring_force = -self.spring * (self.pos - self.spring_balance_pos)

        # 合力F = 外力 + 減衰器力 + ばね力
        # (net force F = external force + damper force + spring force)
        self._net_force = ex_force + self._damper_force + self._spring_force

        # 力Fを与えると、質量mの物体に加速度aが生じる (F = m*a より a = F/m)
        # (when force F is applied, acceleration a occurs in mass m object)
        self.acc = self._net_force / self.mass

        # 加速度aが生じると、速度vが変化 (v = u + a*t)
        # (when acceleration a occurs, velocity v changes)
        self.vel += self.acc * dt

        # 速度vが変化すると、位置xが変化 (x = x0 + v*t)
        # (when velocity v changes, position x changes)
        # 前回速度による変化分 + 今回加速度による変化分
        # (position changes due to previous velocity
        #  + position changes due to current acceleration)
        self.pos += self.prev_vel * dt + 0.5 * self.acc * (dt**2)

    # TODO: 理論特性値（固有振動数、減衰比など）を計算するメソッドを追加


class MDSPhysicalObjectObserver(PhysicalObjectObserver):
    """質量・減衰器・ばね 物理オブジェクト観測クラス
    (Mass-Damper-Spring Physical Object Observer Class)"""

    def __init__(self, physical_obj: MDSPhysicalObject) -> None:
        """MDSPhysicalObjectObserverを初期化する
        (Initialize MDSPhysicalObjectObserver)"""
        super().__init__(physical_obj)
        self._damper_force_list: list[float] = []
        self._spring_force_list: list[float] = []
        self._net_force_list: list[float] = []

    def reset(self) -> None:
        """観測データをリセットする
        (Reset observation data)"""
        super().reset()
        self._damper_force_list.clear()
        self._spring_force_list.clear()
        self._net_force_list.clear()

    def observe(self) -> None:
        """物理オブジェクトの状態を観測し、データリストに追加する
        (Observe the state of the physical object and add to data list)"""
        super().observe()
        self._damper_force_list.append(self.physical_obj._damper_force)
        self._spring_force_list.append(self.physical_obj._spring_force)
        self._net_force_list.append(self.physical_obj._net_force)

    def get_observation_data(self) -> dict:
        """観測データリストを返す
        (Return the observation data list)

        Returns:
            list: 観測データリスト
            (Observation data list)
        """
        return {
            "obj_acceleration_m_s2": self._obj_acc_list,
            "obj_velocity_m_s": self._obj_vel_list,
            "obj_position_m": self._obj_pos_list,
            "damper_force_N": self._damper_force_list,
            "spring_force_N": self._spring_force_list,
            "net_force_N": self._net_force_list,
        }
