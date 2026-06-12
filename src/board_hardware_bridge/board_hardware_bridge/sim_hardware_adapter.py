#!/usr/bin/env python3
"""
Simulation Hardware Adapter

This node adapts the MuJoCo simulation to provide a hardware-like interface.
It translates simulation state into hardware sensor readings and accepts
hardware-like commands.

This enables seamless switching between simulation and real hardware by
providing a consistent interface layer.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from std_msgs.msg import Float64MultiArray, Bool
from sensor_msgs.msg import JointState
import json
import math


class SimulationHardwareAdapter(Node):
    """
    Adapter that makes MuJoCo simulation appear as hardware to the ROS2 system.
    """
    
    def __init__(self):
        super().__init__('sim_hardware_adapter')
        
        # Declare parameters
        self.declare_parameter('publish_rate', 50)  # Hz
        
        self.publish_rate = self.get_parameter('publish_rate').value
        
        self.get_logger().info(
            "Simulation Hardware Adapter initialized"
        )
        
        # Subscribe to simulation topics
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
        
        # Publisher for hardware-like interface
        self.hardware_state_pub = self.create_publisher(
            Float64MultiArray,
            'hardware/state',
            10
        )
        
        self.probe_detection_pub = self.create_publisher(
            Bool,
            'hardware/probe_inserted',
            10
        )
        
        self.cable_detection_pub = self.create_publisher(
            Bool,
            'hardware/cable_plugged',
            10
        )
        
        # Store current states
        self.probe_position = [0, 0, 0]
        self.cable_position = [0, 0, 0]
        
        # Timer for periodic state publishing
        self.timer = self.create_timer(
            1.0 / self.publish_rate,
            self.publish_hardware_state
        )
        
        self.get_logger().info(
            f"Simulation Hardware Adapter started (rate: {self.publish_rate} Hz)"
        )
    
    def probe_state_callback(self, msg: TransformStamped):
        """Handle probe state from MuJoCo simulation."""
        self.probe_position = [
            msg.transform.translation.x,
            msg.transform.translation.y,
            msg.transform.translation.z,
        ]
        
        # Check if probe is in a detection zone (simple distance check)
        probe_detected = self.is_probe_in_detection_zone(self.probe_position)
        
        # Publish detection status
        detection_msg = Bool()
        detection_msg.data = probe_detected
        self.probe_detection_pub.publish(detection_msg)
    
    def cable_plug_state_callback(self, msg: TransformStamped):
        """Handle cable plug state from MuJoCo simulation."""
        self.cable_position = [
            msg.transform.translation.x,
            msg.transform.translation.y,
            msg.transform.translation.z,
        ]
        
        # Check if cable is plugged in (simple distance check)
        cable_plugged = self.is_cable_plugged(self.cable_position)
        
        # Publish plugged status
        plugged_msg = Bool()
        plugged_msg.data = cable_plugged
        self.cable_detection_pub.publish(plugged_msg)
    
    def is_probe_in_detection_zone(self, position):
        """
        Determine if probe is in a detection zone.
        
        This is a simplified detection - in real hardware this would come from
        actual proximity sensors or contact sensors.
        """
        # Define a detection zone around the task area
        # Probe detection zone (approximately where the board is)
        x, y, z = position
        
        # Simple threshold-based detection
        # If probe is near the board surface (z > -0.01), it's detected
        if z > -0.01:
            return True
        return False
    
    def is_cable_plugged(self, position):
        """
        Determine if cable is plugged in.
        
        This checks if the cable position matches the connector location.
        """
        # Define connector location (approximately)
        connector_x, connector_y = 0.038, 0.019
        
        # Cable is "plugged" if it's very close to the connector
        x, y, z = position
        distance = math.sqrt(
            (x - connector_x) ** 2 + (y - connector_y) ** 2
        )
        
        # Threshold of 0.01 meters (1 cm)
        if distance < 0.01 and z > -0.01:
            return True
        return False
    
    def publish_hardware_state(self):
        """
        Publish current hardware-like state to simulate sensor readings.
        """
        state_msg = Float64MultiArray()
        
        # Compose hardware state from simulation
        # Format: [probe_x, probe_y, probe_z, cable_x, cable_y, cable_z, ...]
        state_data = []
        
        # Probe state
        state_data.extend(self.probe_position)
        
        # Cable state
        state_data.extend(self.cable_position)
        
        state_msg.data = state_data
        self.hardware_state_pub.publish(state_msg)


def main(args=None):
    """Main entry point for simulation hardware adapter."""
    rclpy.init(args=args)
    
    try:
        adapter = SimulationHardwareAdapter()
        rclpy.spin(adapter)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
