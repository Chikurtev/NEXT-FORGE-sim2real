#!/usr/bin/env python3
"""
MuJoCo Visualizer Node for Task Board

This module provides real-time visualization of the MuJoCo simulation
using MuJoCo's native rendering capabilities.
"""

import os
from pathlib import Path

import mujoco
import mujoco.viewer
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class TaskBoardMuJoCoVisualizer(Node):
    """
    Visualizer node for MuJoCo simulation of the task board.
    
    Provides real-time rendering of the simulation using MuJoCo's viewer.
    """
    
    def __init__(self):
        super().__init__('board_mujoco_visualizer')
        
        # Declare parameters
        self.declare_parameter('model_path', '')
        self.declare_parameter('width', 1600)
        self.declare_parameter('height', 1200)
        
        # Get parameters
        model_path = self.get_parameter('model_path').value
        self.width = self.get_parameter('width').value
        self.height = self.get_parameter('height').value
        
        # Find model path if not specified
        if not model_path:
            try:
                from ament_index_python.packages import get_package_share_directory
                board_description_dir = get_package_share_directory('board_description')
                model_path = os.path.join(
                    board_description_dir,
                    'urdf',
                    'task_board.xml'
                )
            except Exception as e:
                self.get_logger().error(f"Could not find board_description package: {e}")
                model_path = './src/board_description/urdf/task_board.xml'
        
        # Load MuJoCo model
        self.get_logger().info(f"Loading MuJoCo model for visualization: {model_path}")
        try:
            self.model = mujoco.MjModel.from_xml_file(model_path)
            self.data = mujoco.MjData(self.model)
            self.get_logger().info("MuJoCo model loaded successfully for visualization")
        except Exception as e:
            self.get_logger().error(f"Failed to load MuJoCo model: {e}")
            raise
        
        # Subscriber for simulation state
        self.sim_state_sub = self.create_subscription(
            Float64MultiArray,
            'mujoco/body_states',
            self.state_callback,
            10
        )
        
        self.get_logger().info("MuJoCo Visualizer initialized")
    
    def state_callback(self, msg):
        """
        Callback for simulation state updates.
        
        Args:
            msg: Float64MultiArray with body states
        """
        try:
            # Update visualization based on state
            # This is a placeholder - actual visualization is handled by MuJoCo viewer
            pass
        except Exception as e:
            self.get_logger().warn(f"State update failed: {e}")


def main(args=None):
    """Main entry point for the MuJoCo visualizer node."""
    rclpy.init(args=args)
    
    visualizer = TaskBoardMuJoCoVisualizer()
    
    # Load the model for visualization
    model = visualizer.model
    data = visualizer.data
    
    try:
        # Create and run the viewer
        with mujoco.viewer.launch_passive(model, data) as viewer:
            visualizer.get_logger().info("MuJoCo viewer launched - use mouse to interact")
            visualizer.get_logger().info("Ctrl+C to exit")
            
            # Run the viewer loop
            while viewer.is_running():
                # Step the simulation
                mujoco.mj_step(model, data)
                viewer.sync()
    
    except KeyboardInterrupt:
        visualizer.get_logger().info("Visualization stopped by user")
    except Exception as e:
        visualizer.get_logger().error(f"Visualization error: {e}")
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
