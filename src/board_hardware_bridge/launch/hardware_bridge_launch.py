"""
Launch file for hardware mode with real task board
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():
    """Generate launch description for real hardware with bridge."""
    
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
    
    hardware_address_arg = DeclareLaunchArgument(
        'hardware_address',
        default_value='localhost',
        description='Task board hardware IP address'
    )
    
    hardware_port_arg = DeclareLaunchArgument(
        'hardware_port',
        default_value='8888',
        description='Task board micro-ROS agent port'
    )
    
    # Nodes
    hardware_bridge_node = Node(
        package='board_hardware_bridge',
        executable='hardware_bridge',
        name='board_hardware_bridge',
        parameters=[
            {
                'mode': 'hardware',
                'config_file': LaunchConfiguration('config_file'),
                'hardware_address': LaunchConfiguration('hardware_address'),
                'hardware_port': LaunchConfiguration('hardware_port'),
            }
        ],
        output='screen'
    )
    
    return LaunchDescription([
        config_file_arg,
        hardware_address_arg,
        hardware_port_arg,
        hardware_bridge_node,
    ])
