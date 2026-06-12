"""
Launch file for MuJoCo simulation of the task board
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():
    """Generate launch description for MuJoCo simulator."""
    
    # Get package directory
    board_description_dir = get_package_share_directory('board_description')
    board_mujoco_sim_dir = get_package_share_directory('board_mujoco_sim')
    
    # Model path
    model_path = os.path.join(board_description_dir, 'urdf', 'task_board.xml')
    
    # Launch arguments
    sim_rate_arg = DeclareLaunchArgument(
        'sim_rate',
        default_value='500',
        description='Simulation update rate in Hz'
    )
    
    sim_timestep_arg = DeclareLaunchArgument(
        'sim_timestep',
        default_value='0.002',
        description='Physics simulation timestep in seconds'
    )
    
    enable_rendering_arg = DeclareLaunchArgument(
        'enable_rendering',
        default_value='false',
        description='Enable visualization rendering'
    )
    
    # Nodes
    mujoco_simulator_node = Node(
        package='board_mujoco_sim',
        executable='mujoco_simulator',
        name='board_mujoco_simulator',
        parameters=[
            {
                'model_path': model_path,
                'sim_rate': LaunchConfiguration('sim_rate'),
                'sim_timestep': LaunchConfiguration('sim_timestep'),
                'enable_rendering': LaunchConfiguration('enable_rendering'),
            }
        ],
        output='screen'
    )
    
    return LaunchDescription([
        sim_rate_arg,
        sim_timestep_arg,
        enable_rendering_arg,
        mujoco_simulator_node,
    ])
