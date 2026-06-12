"""
Launch file for simulation mode with hardware bridge
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():
    """Generate launch description for simulation with hardware bridge."""
    
    # Get package directory
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
    
    # Nodes
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
        hardware_bridge_node,
        sim_hardware_adapter_node,
    ])
