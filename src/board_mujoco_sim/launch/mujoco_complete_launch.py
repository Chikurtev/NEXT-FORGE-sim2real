"""
Combined launch file for MuJoCo simulator and visualizer
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():
    """Generate launch description for complete MuJoCo simulation setup."""
    
    # Get package directories
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
    
    enable_visualization_arg = DeclareLaunchArgument(
        'enable_visualization',
        default_value='true',
        description='Enable MuJoCo visualization'
    )
    
    # Simulator node
    simulator_node = Node(
        package='board_mujoco_sim',
        executable='mujoco_simulator',
        name='board_mujoco_simulator',
        parameters=[
            {
                'model_path': model_path,
                'sim_rate': LaunchConfiguration('sim_rate'),
                'sim_timestep': LaunchConfiguration('sim_timestep'),
            }
        ],
        output='screen'
    )
    
    # Visualizer node
    visualizer_node = Node(
        package='board_mujoco_sim',
        executable='mujoco_visualizer',
        name='board_mujoco_visualizer',
        parameters=[
            {
                'model_path': model_path,
                'width': '1600',
                'height': '1200',
            }
        ],
        output='screen'
    )
    
    return LaunchDescription([
        sim_rate_arg,
        sim_timestep_arg,
        enable_visualization_arg,
        simulator_node,
        visualizer_node,
    ])
