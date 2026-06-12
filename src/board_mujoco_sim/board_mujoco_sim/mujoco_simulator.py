#!/usr/bin/env python3
"""
MuJoCo Simulator Node for Task Board Digital Twin

This module provides the main simulator node that integrates MuJoCo physics engine
with ROS2 for real-time simulation of the task board.
"""

import os
import sys
from pathlib import Path

import mujoco
import rclpy
from geometry_msgs.msg import TransformStamped, Twist, Point
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, Int32


class TaskBoardMuJoCoSimulator(Node):
    """
    Main simulator node that manages MuJoCo physics simulation for the task board.
    
    This node:
    - Loads the task board MJCF model
    - Runs physics simulation at specified frequency
    - Publishes body states and sensor data
    - Subscribes to control commands
    """
    
    def __init__(self):
        super().__init__('board_mujoco_simulator')
        
        # Declare parameters
        self.declare_parameter('model_path', '')
        self.declare_parameter('sim_timestep', 0.002)
        self.declare_parameter('sim_rate', 500)  # Hz
        self.declare_parameter('enable_rendering', False)
        
        # Get parameters
        model_path = self.get_parameter('model_path').value
        self.sim_timestep = self.get_parameter('sim_timestep').value
        sim_rate = self.get_parameter('sim_rate').value
        
        # Find model path if not specified
        if not model_path:
            # Try to find the model in the board_description package
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
        self.get_logger().info(f"Loading MuJoCo model from: {model_path}")
        try:
            self.model = mujoco.MjModel.from_xml_file(model_path)
            self.data = mujoco.MjData(self.model)
            self.get_logger().info("MuJoCo model loaded successfully")
        except Exception as e:
            self.get_logger().error(f"Failed to load MuJoCo model: {e}")
            raise
        
        # Physics parameters
        self.model.opt.timestep = self.sim_timestep
        
        # Create publishers
        self.body_states_pub = self.create_publisher(
            Float64MultiArray, 
            'mujoco/body_states', 
            10
        )
        
        self.sensor_data_pub = self.create_publisher(
            Float64MultiArray,
            'mujoco/sensor_data',
            10
        )
        
        self.probe_state_pub = self.create_publisher(
            TransformStamped,
            'mujoco/probe_state',
            10
        )
        
        self.cable_plug_state_pub = self.create_publisher(
            TransformStamped,
            'mujoco/cable_plug_state',
            10
        )
        
        # Create subscriber for control commands
        self.control_sub = self.create_subscription(
            Float64MultiArray,
            'mujoco/control_command',
            self.control_callback,
            10
        )
        
        # Timer for simulation loop
        self.sim_period = 1.0 / sim_rate
        self.timer = self.create_timer(
            self.sim_period,
            self.simulation_step
        )
        
        self.get_logger().info(f"MuJoCo Simulator initialized (rate: {sim_rate} Hz)")
        
        # Step counter for logging
        self.step_count = 0
        
    def simulation_step(self):
        """
        Execute one step of MuJoCo simulation and publish results.
        """
        try:
            # Step the simulation
            mujoco.mj_step(self.model, self.data)
            
            # Publish sensor data
            self.publish_sensor_data()
            
            # Publish body states (every 10 steps for efficiency)
            if self.step_count % 10 == 0:
                self.publish_body_states()
            
            self.step_count += 1
            
        except Exception as e:
            self.get_logger().error(f"Simulation step failed: {e}")
    
    def publish_sensor_data(self):
        """
        Publish sensor readings from MuJoCo simulation.
        """
        try:
            # Get sensor data
            sensor_data = Float64MultiArray()
            
            # Collect all sensor readings
            sensor_readings = []
            for i in range(self.model.nsensor):
                sensor = self.model.sensor(i)
                adr = sensor.adr
                dim = sensor.dim
                sensor_readings.extend(self.data.sensordata[adr:adr + dim])
            
            sensor_data.data = sensor_readings
            self.sensor_data_pub.publish(sensor_data)
            
        except Exception as e:
            self.get_logger().debug(f"Could not publish sensor data: {e}")
    
    def publish_body_states(self):
        """
        Publish states of all bodies in the simulation.
        """
        try:
            body_states = Float64MultiArray()
            state_data = []
            
            # Get state for probe and cable plug (main points of interest)
            probe_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, 'task_board_probe')
            cable_plug_id = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, 'task_board_cable_plug')
            
            # Probe state (position and quaternion)
            if probe_id >= 0:
                probe_xpos = self.data.xpos[probe_id]
                probe_xquat = self.data.xquat[probe_id]
                self.publish_transform(probe_xpos, probe_xquat, 'task_board_probe', self.probe_state_pub)
                state_data.extend(probe_xpos)
                state_data.extend(probe_xquat)
            
            # Cable plug state
            if cable_plug_id >= 0:
                cable_xpos = self.data.xpos[cable_plug_id]
                cable_xquat = self.data.xquat[cable_plug_id]
                self.publish_transform(cable_xpos, cable_xquat, 'task_board_cable_plug', self.cable_plug_state_pub)
                state_data.extend(cable_xpos)
                state_data.extend(cable_xquat)
            
            body_states.data = state_data
            self.body_states_pub.publish(body_states)
            
        except Exception as e:
            self.get_logger().debug(f"Could not publish body states: {e}")
    
    def publish_transform(self, position, quaternion, frame_name, publisher):
        """
        Publish a transform for a body.
        
        Args:
            position: [x, y, z] position
            quaternion: [w, x, y, z] quaternion
            frame_name: Name of the body frame
            publisher: ROS2 publisher for the transform
        """
        try:
            transform = TransformStamped()
            transform.header.stamp = self.get_clock().now().to_msg()
            transform.header.frame_id = 'world'
            transform.child_frame_id = frame_name
            
            # Position
            transform.transform.translation.x = float(position[0])
            transform.transform.translation.y = float(position[1])
            transform.transform.translation.z = float(position[2])
            
            # Quaternion (MuJoCo uses [w, x, y, z])
            transform.transform.rotation.w = float(quaternion[0])
            transform.transform.rotation.x = float(quaternion[1])
            transform.transform.rotation.y = float(quaternion[2])
            transform.transform.rotation.z = float(quaternion[3])
            
            publisher.publish(transform)
        except Exception as e:
            self.get_logger().debug(f"Could not publish transform: {e}")
    
    def control_callback(self, msg):
        """
        Callback for control commands.
        
        Args:
            msg: Float64MultiArray with control values
        """
        try:
            # Apply control signals to actuators
            if len(msg.data) > 0:
                # Limit to number of actuators
                num_actuators = min(len(msg.data), self.model.nu)
                self.data.ctrl[:num_actuators] = msg.data[:num_actuators]
        except Exception as e:
            self.get_logger().warn(f"Control command failed: {e}")


def main(args=None):
    """Main entry point for the MuJoCo simulator node."""
    rclpy.init(args=args)
    
    try:
        simulator = TaskBoardMuJoCoSimulator()
        rclpy.spin(simulator)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
