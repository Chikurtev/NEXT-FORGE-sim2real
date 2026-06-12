#!/usr/bin/env python3
"""
Hardware Bridge Node

This node bridges communication between the ROS2 ecosystem and the task board.
It can work with either:
1. Real hardware (via micro-ROS on the board)
2. MuJoCo simulation (via board_mujoco_sim package)

The bridge translates between:
- High-level task commands/status
- Simulation state/commands
- Real hardware interface
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import TransformStamped, Twist
from std_msgs.msg import Float64MultiArray, Bool, String
import json
import os


class HardwareBridge(Node):
    """
    Main hardware bridge node that coordinates between simulation and real hardware.
    """
    
    def __init__(self):
        super().__init__('board_hardware_bridge')
        
        # Declare parameters
        self.declare_parameter('mode', 'simulation')  # 'simulation' or 'hardware'
        self.declare_parameter('config_file', '')
        self.declare_parameter('hardware_address', 'localhost')
        self.declare_parameter('hardware_port', 8888)
        
        # Get parameters
        self.mode = self.get_parameter('mode').value
        config_file = self.get_parameter('config_file').value
        self.hardware_address = self.get_parameter('hardware_address').value
        self.hardware_port = self.get_parameter('hardware_port').value
        
        self.get_logger().info(f"Hardware Bridge started in {self.mode} mode")
        
        # Load configuration
        self.config = self.load_config(config_file)
        
        # Topic mappings
        self.sim_to_hw_mapping = {}
        self.hw_to_sim_mapping = {}
        
        # Create subscribers for simulation topics
        self.probe_state_sub = self.create_subscription(
            TransformStamped,
            'mujoco/probe_state',
            self.probe_state_callback,
            10
        )
        
        self.cable_plug_state_sub = self.create_subscription(
            TransformStamped,
            'mujoco/cable_plug_state',
            self.cable_plug_state_callback,
            10
        )
        
        self.body_states_sub = self.create_subscription(
            Float64MultiArray,
            'mujoco/body_states',
            self.body_states_callback,
            10
        )
        
        # Create publishers for hardware state
        self.sim_state_pub = self.create_publisher(
            Float64MultiArray,
            'board/simulation_state',
            10
        )
        
        self.status_pub = self.create_publisher(
            String,
            'board/bridge_status',
            10
        )
        
        # Timer for periodic status update
        self.timer = self.create_timer(5.0, self.publish_status)
        
        self.get_logger().info("Hardware Bridge initialized")
    
    def load_config(self, config_file):
        """Load bridge configuration from file."""
        if not config_file:
            config_file = os.path.join(
                os.path.dirname(__file__),
                'config',
                'default_bridge_config.json'
            )
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            self.get_logger().info(f"Loaded config from {config_file}")
            return config
        except FileNotFoundError:
            self.get_logger().warn(f"Config file not found: {config_file}")
            return {}
        except json.JSONDecodeError as e:
            self.get_logger().error(f"Invalid JSON in config: {e}")
            return {}
    
    def probe_state_callback(self, msg):
        """Handle probe state from simulation."""
        if self.mode == 'simulation':
            # Extract probe position and orientation
            pos = [
                msg.transform.translation.x,
                msg.transform.translation.y,
                msg.transform.translation.z,
            ]
            quat = [
                msg.transform.rotation.w,
                msg.transform.rotation.x,
                msg.transform.rotation.y,
                msg.transform.rotation.z,
            ]
            
            self.get_logger().debug(
                f"Probe state - Position: {pos}, Quat: {quat}"
            )
    
    def cable_plug_state_callback(self, msg):
        """Handle cable plug state from simulation."""
        if self.mode == 'simulation':
            # Extract cable plug position and orientation
            pos = [
                msg.transform.translation.x,
                msg.transform.translation.y,
                msg.transform.translation.z,
            ]
            quat = [
                msg.transform.rotation.w,
                msg.transform.rotation.x,
                msg.transform.rotation.y,
                msg.transform.rotation.z,
            ]
            
            self.get_logger().debug(
                f"Cable plug state - Position: {pos}, Quat: {quat}"
            )
    
    def body_states_callback(self, msg):
        """Handle all body states from simulation."""
        if self.mode == 'simulation':
            # Publish to board state topic
            self.sim_state_pub.publish(msg)
    
    def publish_status(self):
        """Publish bridge status periodically."""
        status_msg = String()
        status_msg.data = json.dumps({
            'mode': self.mode,
            'status': 'operational',
            'hardware_address': self.hardware_address if self.mode == 'hardware' else 'N/A',
            'timestamp': self.get_clock().now().nanoseconds / 1e9,
        })
        self.status_pub.publish(status_msg)


def main(args=None):
    """Main entry point for hardware bridge node."""
    rclpy.init(args=args)
    
    try:
        bridge = HardwareBridge()
        rclpy.spin(bridge)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
