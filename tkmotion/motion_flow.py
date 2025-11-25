import pandas as pd
from tkmotion.motion_flow_config import MotionFlowConfig
from tkmotion.motion_profile import MotionProfile
from tkmotion.config_loader import ConfigLoader
from tkmotion.motion_profile_loader import MotionProfileLoader


class MotionFlow:
    """A class to handle motion flow operations."""

    def __init__(self) -> None:
        """Initialize the MotionFlow."""
        self._motion_flow_config: MotionFlowConfig | None = None
        self._motion_profile: MotionProfile | None = None

    @property
    def config(self) -> MotionFlowConfig | None:
        """Returns the motion flow configuration."""
        return self._motion_flow_config

    @property
    def mprof(self) -> MotionProfile | None:
        """Returns the motion profile."""
        return self._motion_profile

    def load_config(self) -> None:
        """Load configuration using ConfigLoader."""

        loader = ConfigLoader()
        self._motion_flow_config = loader.load()

    def load_motion_profile(self) -> None:
        """Load motion profile using MotionProfileLoader."""

        profile_loader = MotionProfileLoader()
        self._motion_profile = profile_loader.load()

    def execute(self) -> pd.DataFrame:
        print("Executing motion flow...")

        if self._motion_flow_config is None:
            raise ValueError(
                "Motion flow configuration not loaded. Call load_config() first."
            )

        if self._motion_flow_config.discrete_time is None:
            raise ValueError("Discrete time configuration not available.")

        if self._motion_profile is None:
            raise ValueError(
                "Motion profile not loaded. Call load_motion_profile() first."
            )

        motion_profile = self._motion_profile

        time_steps_gen = (
            self._motion_flow_config.discrete_time.get_time_step_generator()
        )
        time_list = []
        vel_list = []
        pos_list = []
        for t in time_steps_gen:
            time_list.append(t)

            # Get velocity and position from motion profile
            vel, pos = motion_profile.cmd_vel_pos(t)
            vel_list.append(vel)
            pos_list.append(pos)

        df = pd.DataFrame(
            {
                "time_s": time_list,
                "velocity_m_s": vel_list,
                "position_m": pos_list,
            }
        )

        print(f"Generated {len(time_list)} time steps.")

        # TODO: サーボ推力計算 (PID制御)

        # TODO: 力 --> 速度 --> 位置変換 (仮想現在位置 更新)

        return df
