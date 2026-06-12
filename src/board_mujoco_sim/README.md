# Board MuJoCo Simulator

MuJoCo integration package for the task board digital twin ROS2 simulation.

## Overview

This package provides a complete MuJoCo physics simulation environment for the task board project. It includes:

- **Physics Simulation**: Real-time MuJoCo physics engine integration
- **ROS2 Integration**: Full ROS2 node interface with topic-based communication
- **Sensor Simulation**: Simulated sensors for monitoring task board state
- **Visualization**: Native MuJoCo viewer for interactive simulation visualization
- **Control Interface**: ROS2-based control command interface

## Features

### Physics Simulation
- Accurate rigid body dynamics
- Contact detection and response
- Support for floating objects (probe, cable plug)
- Configurable timestep and integration method

### ROS2 Integration
- `mujoco_simulator`: Main physics simulation node
- `mujoco_visualizer`: Interactive visualization node
- Topic-based state and sensor publishing
- Command-based control interface

### Supported Objects
- Task board body (fixed)
- Probe (floating, can be grasped)
- Cable plug (floating, can be connected)
- Banana plugs (fixed components)

## Installation

### Prerequisites
```bash
# MuJoCo (Python bindings)
pip install mujoco>=2.2.0

# ROS2 dependencies
sudo apt install ros-humble-geometry-msgs ros-humble-sensor-msgs
```

### Build from Source
```bash
cd ~/ros_projects/ros2_ws
colcon build --packages-select board_mujoco_sim board_description
```

## Usage

### Launch MuJoCo Simulator Only
```bash
ros2 launch board_mujoco_sim mujoco_simulator_launch.py
```

### Launch MuJoCo Visualizer Only
```bash
ros2 launch board_mujoco_sim mujoco_visualizer_launch.py
```

### Launch Complete Simulation (Simulator + Visualizer)
```bash
ros2 launch board_mujoco_sim mujoco_complete_launch.py
```

### Launch with Custom Parameters
```bash
# Custom simulation rate (Hz)
ros2 launch board_mujoco_sim mujoco_simulator_launch.py sim_rate:=1000

# Custom timestep (seconds)
ros2 launch board_mujoco_sim mujoco_simulator_launch.py sim_timestep:=0.001
```

## ROS2 Topics

### Published Topics

#### Simulation State
- `mujoco/body_states` (`std_msgs/Float64MultiArray`)
  - Contains position and quaternion of floating bodies
  - Published at reduced rate (50 Hz) for efficiency

- `mujoco/sensor_data` (`std_msgs/Float64MultiArray`)
  - Sensor readings from MuJoCo simulation
  - Position, velocity, orientation data

#### Body Transforms
- `mujoco/probe_state` (`geometry_msgs/TransformStamped`)
  - Position and orientation of the probe

- `mujoco/cable_plug_state` (`geometry_msgs/TransformStamped`)
  - Position and orientation of the cable plug

### Subscribed Topics

#### Control
- `mujoco/control_command` (`std_msgs/Float64MultiArray`)
  - Control commands for actuators
  - Values mapped to MuJoCo actuators

## Model Structure

The MuJoCo model (`task_board.xml`) includes:

```
task_board (root)
├── task_board_main
│   ├── task_board_body (main structure, fixed)
│   ├── task_board_probe (floating, with freejoint)
│   └── task_board_cable_plug (floating, with freejoint)
```

### URDF to MuJoCo Conversion

Original URDF files have been converted to MuJoCo MJCF format:
- `task_board.urdf` → `task_board.xml`
- Mesh paths updated for relative reference
- Physics parameters optimized for MuJoCo
- Added contact and friction parameters

## Physics Parameters

Key MuJoCo simulation parameters (in `task_board.xml`):

```xml
<option timestep="0.002" integrator="RK4" gravity="0 0 -9.81">
    <flag energy="enable" contact="enable" multicoll="enable"/>
</option>
```

- **Timestep**: 2ms (500 Hz simulation)
- **Integrator**: RK4 (4th order Runge-Kutta)
- **Gravity**: 9.81 m/s² downward

## Contact & Friction

Default contact parameters:
```xml
<contact condim="4" friction="0.5 0.5 0.0001" 
         solimp="0.9 0.99 0.001" solref="0.02 1" />
```

- **Friction**: 0.5 (lateral and torsional)
- **Soft contacts**: Enabled for stability

## Performance

Typical performance metrics:
- **Simulation Speed**: 1-2x real-time on modern hardware
- **Update Rate**: Configurable (default 500 Hz)
- **Rendering**: 60 Hz visualization when enabled

## Troubleshooting

### Model Not Found
If you get "Model not found" error:
1. Ensure `board_description` package is built and sourced
2. Check model path: `ros2 pkg prefix board_description`
3. Verify `task_board.xml` exists in urdf directory

### MuJoCo Not Installed
```bash
pip install --upgrade mujoco
```

### Visualization Not Starting
- Ensure you have X11 forwarding enabled (on Linux)
- Check MuJoCo viewer requirements
- Verify graphics drivers are up to date

## Development

### Adding New Sensors
Edit `task_board.xml` in the `<sensor>` section:
```xml
<sensor>
    <framepos name="custom_sensor" objtype="body" objname="body_name"/>
</sensor>
```

### Modifying Physics Parameters
Edit `<option>` and `<default>` sections in `task_board.xml`

### Adding New Objects
1. Add mesh to `<asset>` section
2. Create body in `<worldbody>`
3. Add corresponding ROS2 publisher in `mujoco_simulator.py`

## References

- [MuJoCo Documentation](https://mujoco.readthedocs.io/)
- [MuJoCo MJCF Format](https://mujoco.readthedocs.io/en/latest/XMLreference.html)
- [ROS2 Launch System](https://docs.ros.org/en/humble/Concepts/Basic/About-Launch.html)

## License

BSD-3-Clause License

## Author

ROS2 Team - Task Board Digital Twin Project
