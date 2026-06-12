"""
Complete launch file for MuJoCo simulation with hardware bridge and visualization
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():
    """Generate complete launch description for simulation with bridge."""
    
    # Get package directories
    board_mujoco_sim_dir = get_package_share_directory('board_mujoco_sim')
    board_hardware_bridge_dir = get_package_share_directory('board_hardware_bridge')
    
    # Default config path
    default_config = os.path.join(
        board_hardware_bridge_dir,
        'config',
        'default_bridge_config.json'
    )
    
    # Launch arguments
    config_file_arg = DeclareLaunchArgument(
        'config_file',
        default_value=default_config,
        description='Hardware bridge configuration file'
    )
    
    sim_rate_arg = DeclareLaunchArgument(
        'sim_rate',
        default_value='500',
        description='Simulation update rate (Hz)'
    )
    
    enable_visualization_arg = DeclareLaunchArgument(
        'enable_visualization',
        default_value='true',
        description='Enable MuJoCo visualization'
    )
    
    # Include MuJoCo simulator launch
    mujoco_simulator = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(board_mujoco_sim_dir, 'launch', 'mujoco_simulator_launch.py')
        ),
        launch_arguments={
            'sim_rate': LaunchConfiguration('sim_rate'),
        }.items()
    )
    
    # Include visualization if enabled
    mujoco_visualizer = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(board_mujoco_sim_dir, 'launch', 'mujoco_visualizer_launch.py')
        )
    )
    
    # Hardware bridge
    hardware_bridge_node = Node(
        package='board_hardware_bridge',
        executable='hardware_bridge',
        name='board_hardware_bridge',
        parameters=[
            {
                'mode': 'simulation',
                'config_file': LaunchConfiguration('config_file'),
            }
        ],
        output='screen'
    )
    
    # Simulation hardware adapter
    sim_hardware_adapter_node = Node(
        package='board_hardware_bridge',
        executable='sim_hardware_adapter',
        name='sim_hardware_adapter',
        parameters=[
            {
                'publish_rate': 50,
            }
        ],
        output='screen'
    )
    
    return LaunchDescription([
        config_file_arg,
        sim_rate_arg,
        enable_visualization_arg,
        mujoco_simulator,
        mujoco_visualizer,
        hardware_bridge_node,
        sim_hardware_adapter_node,
    ])
