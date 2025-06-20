# Copyright (c) 2022-2025, The Isaac Lab Project Developers.
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from isaaclab_assets import H1_CFG

import isaaclab.sim as sim_utils
from isaaclab.assets import ArticulationCfg
from isaaclab.envs import DirectRLEnvCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.sim import SimulationCfg
from isaaclab.terrains import TerrainImporterCfg
from isaaclab.utils import configclass

from isaaclab_tasks.direct.locomotion.locomotion_env import LocomotionEnv


@configclass
class H1EnvCfg(DirectRLEnvCfg):
    # env
    episode_length_s = 15.0
    decimation = 2
    action_scale = 0.750
    action_space = 19
    observation_space = 69
    state_space = 0

    # simulation
    sim: SimulationCfg = SimulationCfg(dt=1 / 120, render_interval=decimation)
    terrain = TerrainImporterCfg(
        prim_path="/World/ground",
        terrain_type="plane",
        collision_group=-1,
        physics_material=sim_utils.RigidBodyMaterialCfg(
            friction_combine_mode="average",
            restitution_combine_mode="average",
            static_friction=1.0,
            dynamic_friction=1.0,
            restitution=0.0,
        ),
        debug_vis=False,
    )

    # scene
    scene: InteractiveSceneCfg = InteractiveSceneCfg(num_envs=4096, env_spacing=4.0, replicate_physics=True)

    # robot
    robot: ArticulationCfg = H1_CFG.replace(prim_path="/World/envs/env_.*/Robot")
    joint_gears: list = [
        100.0,  # left_hip_yaw
        100.0,  # right_hip_yaw
        100.0,   # torso
        120.0,  # left_hip_roll
        120.0,  # right_hip_roll
        75.0,   # left_shoulder_pitch
        75.0,   # right_shoulder_pitch
        100.0,  # left_hip_pitch
        100.0,  # right_hip_pitch
        75.0,   # left_shoulder_roll
        75.0,   # right_shoulder_roll
        90.0,   # left_knee
        90.0,   # right_knee
        75.0,   # left_shoulder_yaw
        75.0,   # right_shoulder_yaw
        90.0,   # left_ankle
        90.0,   # right_ankle
        50.0,   # left_elbow
        50.0,   # right_elbow
    ]

    heading_weight: float = 2.5
    up_weight: float = 0.5

    energy_cost_scale: float = 0.08
    actions_cost_scale: float = 0.05
    alive_reward_scale: float = 5.0
    dof_vel_scale: float = 2.5

    death_cost: float = -2.0
    termination_height: float = 1.0

    angular_velocity_scale: float = 1.0
    contact_force_scale: float = 0.5
    smoothness_scale: float = 0.1
    limping_scale: float = 0.2
    alternating_scale: float = 3.0
    arm_movement_scale: float = 0.75


class H1Env(LocomotionEnv):
    cfg: H1EnvCfg

    def __init__(self, cfg: H1EnvCfg, render_mode: str | None = None, **kwargs):
        super().__init__(cfg, render_mode, **kwargs)
