"""
Launch file for MuJoCo visualization of the task board
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():
    """Generate launch description for MuJoCo visualizer."""
    
    # Get package directory
    board_description_dir = get_package_share_directory('board_description')
    
    # Model path
    model_path = os.path.join(board_description_dir, 'urdf', 'task_board.xml')
    
    # Launch arguments
    width_arg = DeclareLaunchArgument(
        'width',
        default_value='1600',
        description='Visualization window width'
    )
    
    height_arg = DeclareLaunchArgument(
        'height',
        default_value='1200',
        description='Visualization window height'
    )
    
    # Nodes
    mujoco_visualizer_node = Node(
        package='board_mujoco_sim',
        executable='mujoco_visualizer',
        name='board_mujoco_visualizer',
        parameters=[
            {
                'model_path': model_path,
                'width': LaunchConfiguration('width'),
                'height': LaunchConfiguration('height'),
            }
        ],
        output='screen'
    )
    
    return LaunchDescription([
        width_arg,
        height_arg,
        mujoco_visualizer_node,
    ])
