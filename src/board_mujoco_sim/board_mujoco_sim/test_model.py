#!/usr/bin/env python3
"""
Test script for MuJoCo task board model validation
"""

import os
import sys
from pathlib import Path

try:
    import mujoco
except ImportError:
    print("ERROR: MuJoCo not installed. Install with:")
    print("  pip install mujoco>=2.2.0")
    sys.exit(1)


def find_model_path():
    """Find the task_board.xml model file."""
    # Try multiple possible locations
    possible_paths = [
        Path("./src/board_description/urdf/task_board.xml"),
        Path("../src/board_description/urdf/task_board.xml"),
        Path("../../src/board_description/urdf/task_board.xml"),
        Path("/home/*/ros_projects/ros2_ws/src/board_description/urdf/task_board.xml"),
    ]
    
    for path in possible_paths:
        if path.exists():
            return str(path.resolve())
    
    return None


def validate_model(model_path):
    """Validate the MuJoCo model."""
    print(f"\n{'='*60}")
    print("MuJoCo Task Board Model Validation")
    print(f"{'='*60}\n")
    
    # Load model
    print(f"Loading model from: {model_path}")
    try:
        model = mujoco.MjModel.from_xml_path(model_path)
        data = mujoco.MjData(model)
        print("✓ Model loaded successfully")
    except Exception as e:
        print(f"✗ Failed to load model: {e}")
        return False
    
    # Display model statistics
    print(f"\n{'='*60}")
    print("Model Statistics")
    print(f"{'='*60}")
    print(f"Bodies:        {model.nbody}")
    print(f"Joints:        {model.njnt}")
    print(f"Geoms:         {model.ngeom}")
    print(f"Sensors:       {model.nsensor}")
    print(f"Actuators:     {model.nu}")
    print(f"Degrees of Freedom (dofs): {model.nv}")
    
    # Display body information
    print(f"\n{'='*60}")
    print("Bodies")
    print(f"{'='*60}")
    for i in range(model.nbody):
        body = model.body(i)
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_BODY, i)
        print(f"{i:2d}. {name:40s} | Mass: {body.mass[0]:8.4f} kg")
    
    # Display joint information
    print(f"\n{'='*60}")
    print("Joints")
    print(f"{'='*60}")
    for i in range(model.njnt):
        joint = model.jnt(i)
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i)
        joint_type = ["free", "ball", "slide", "hinge"][joint.type]
        print(f"{i:2d}. {name:40s} | Type: {joint_type:6s}")
    
    # Display sensor information
    print(f"\n{'='*60}")
    print("Sensors")
    print(f"{'='*60}")
    for i in range(model.nsensor):
        sensor = model.sensor(i)
        name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_SENSOR, i)
        sensor_type = ["position", "velocity", "accelerometer", "gyro", "force", "torque"][sensor.type]
        print(f"{i:2d}. {name:40s} | Type: {sensor_type:12s}")
    
    # Test simulation step
    print(f"\n{'='*60}")
    print("Simulation Test")
    print(f"{'='*60}")
    print(f"Initial timestep: {model.opt.timestep} seconds")
    print(f"Integrator: {['Euler', 'RK4', 'implicit'][model.opt.integrator]}")
    print(f"Gravity: {model.opt.gravity}")
    
    try:
        print("\nRunning 100 simulation steps...")
        for step in range(100):
            mujoco.mj_step(model, data)
        print("✓ Simulation steps completed successfully")
        
        # Check for NaN values
        if any(any(v != v for v in row) if hasattr(row, '__iter__') 
               else row != row for row in [data.qpos, data.qvel, data.xpos]):
            print("✗ Warning: NaN values detected in simulation state!")
            return False
        else:
            print("✓ No NaN values detected in simulation state")
    except Exception as e:
        print(f"✗ Simulation failed: {e}")
        return False
    
    # Display key body states after simulation
    print(f"\n{'='*60}")
    print("Body States After Simulation")
    print(f"{'='*60}")
    
    probe_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "task_board_probe")
    cable_plug_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "task_board_cable_plug")
    main_body_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, "task_board_body")
    
    if probe_id >= 0:
        pos = data.xpos[probe_id]
        print(f"Probe position:       [{pos[0]:8.4f}, {pos[1]:8.4f}, {pos[2]:8.4f}] m")
    
    if cable_plug_id >= 0:
        pos = data.xpos[cable_plug_id]
        print(f"Cable plug position:  [{pos[0]:8.4f}, {pos[1]:8.4f}, {pos[2]:8.4f}] m")
    
    if main_body_id >= 0:
        pos = data.xpos[main_body_id]
        print(f"Main body position:   [{pos[0]:8.4f}, {pos[1]:8.4f}, {pos[2]:8.4f}] m")
    
    print(f"\n{'='*60}")
    print("✓ Model validation completed successfully!")
    print(f"{'='*60}\n")
    
    return True


def main():
    """Main entry point."""
    model_path = find_model_path()
    
    if not model_path:
        print("ERROR: Could not find task_board.xml model file")
        print("\nSearched in:")
        print("  ./src/board_description/urdf/task_board.xml")
        print("  ../src/board_description/urdf/task_board.xml")
        print("  ../../src/board_description/urdf/task_board.xml")
        sys.exit(1)
    
    success = validate_model(model_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
