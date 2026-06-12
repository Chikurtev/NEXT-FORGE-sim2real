#!/usr/bin/env python3
"""
Example: Using the Hardware Bridge

This example demonstrates how to use the hardware bridge to work with either
simulation or real hardware seamlessly.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from std_msgs.msg import Float64MultiArray
import json


class TaskBoardClient(Node):
    """Example client that works with both simulation and real hardware."""
    
    def __init__(self):
        super().__init__('taskboard_client')
        
        # Subscribe to hardware status topics
        self.probe_sub = self.create_subscription(
            Bool,
            'hardware/probe_inserted',
            self.probe_callback,
            10
        )
        
        self.cable_sub = self.create_subscription(
            Bool,
            'hardware/cable_plugged',
            self.cable_callback,
            10
        )
        
        self.state_sub = self.create_subscription(
            Float64MultiArray,
            'hardware/state',
            self.state_callback,
            10
        )
        
        self.bridge_status_sub = self.create_subscription(
            rclpy.msg.String,
            'board/bridge_status',
            self.bridge_status_callback,
            10
        )
        
        self.get_logger().info("TaskBoard Client initialized")
        self.get_logger().info("Waiting for hardware/bridge status...")
    
    def probe_callback(self, msg):
        """Handle probe detection status."""
        status = "DETECTED" if msg.data else "NOT_DETECTED"
        self.get_logger().info(f"Probe Status: {status}")
    
    def cable_callback(self, msg):
        """Handle cable connection status."""
        status = "PLUGGED" if msg.data else "UNPLUGGED"
        self.get_logger().info(f"Cable Status: {status}")
    
    def state_callback(self, msg):
        """Handle hardware state."""
        if len(msg.data) >= 6:
            probe_x, probe_y, probe_z = msg.data[0:3]
            cable_x, cable_y, cable_z = msg.data[3:6]
            self.get_logger().debug(
                f"Hardware State - Probe: ({probe_x:.3f}, {probe_y:.3f}, {probe_z:.3f}), "
                f"Cable: ({cable_x:.3f}, {cable_y:.3f}, {cable_z:.3f})"
            )
    
    def bridge_status_callback(self, msg):
        """Handle bridge status."""
        try:
            status_dict = json.loads(msg.data)
            mode = status_dict.get('mode', 'unknown')
            bridge_status = status_dict.get('status', 'unknown')
            self.get_logger().info(
                f"Bridge Status - Mode: {mode}, Status: {bridge_status}"
            )
        except json.JSONDecodeError:
            self.get_logger().warn(f"Could not parse status: {msg.data}")


def main():
    """Run example client."""
    rclpy.init()
    
    try:
        client = TaskBoardClient()
        print("\n" + "=" * 60)
        print("Hardware Bridge Example Client")
        print("=" * 60)
        print("\nMonitoring task board hardware interface...")
        print("(Works with both simulation and real hardware)")
        print("\nPress Ctrl+C to exit\n")
        
        rclpy.spin(client)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
