# MuJoCo Integration Guide for Task Board Project

##執行概要 / Executive Summary

This document provides a comprehensive guide for integrating MuJoCo physics simulation into the ROS2-based task board digital twin project.

## Quick Start

### 1. Install MuJoCo
```bash
pip install mujoco>=2.2.0
```

### 2. Build ROS2 Packages
```bash
cd ~/ros_projects/ros2_ws
colcon build --packages-select board_description board_mujoco_sim
source install/setup.bash
```

### 3. Run Simulation
```bash
# Start simulator and visualizer
ros2 launch board_mujoco_sim mujoco_complete_launch.py

# Or run separately:
ros2 launch board_mujoco_sim mujoco_simulator_launch.py      # Terminal 1
ros2 launch board_mujoco_sim mujoco_visualizer_launch.py     # Terminal 2
```

### 4. Validate Model
```bash
python3 src/board_mujoco_sim/board_mujoco_sim/test_model.py
```

## Architecture Overview

```
┌─────────────────────────────────────────────┐
│     ROS2 Task Board Digital Twin            │
└─────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼────┐   ┌─────▼──────┐   ┌──┴───────┐
   │ MuJoCo  │   │ Visualizer │   │ Recorder │
   │Simulator│   │(Interactive)   │          │
   └────┬────┘   └──────┬──────┘   └──────────┘
        │                │
        └────────┬───────┘
                 │
          ┌──────▼──────┐
          │  ROS2 Node  │
          │ Interface   │
          └──────┬──────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼───┐  ┌────▼────┐  ┌────▼────┐
│Topics │  │Services │  │Parameters│
└───────┘  └─────────┘  └──────────┘
```

## File Structure

```
board_mujoco_sim/
├── board_mujoco_sim/
│   ├── __init__.py
│   ├── mujoco_simulator.py      # Main simulator node
│   ├── mujoco_visualizer.py     # Visualization node
│   └── test_model.py            # Model validation script
├── launch/
│   ├── mujoco_simulator_launch.py
│   ├── mujoco_visualizer_launch.py
│   └── mujoco_complete_launch.py
├── docs/
│   └── URDF_TO_MUJOCO_CONVERSION.md
├── test/
│   ├── test_copyright.py
│   ├── test_flake8.py
│   └── test_pep257.py
├── package.xml
├── setup.py
├── setup.cfg
└── README.md

board_description/urdf/
├── task_board.urdf       # Original URDF (for reference)
├── task_board.xml        # MuJoCo MJCF model (primary)
├── task_board_main.xml   # (Legacy - included in task_board.xml)
├── task_board_probe.xml  # (Legacy - included in task_board.xml)
└── task_board_cable_plug.xml # (Legacy - included in task_board.xml)
```

## Model Structure

### The Task Board Model (task_board.xml)

**Components:**
1. **Main Body** (fixed)
   - task_board_body: Primary structure (mass: 7.6 kg)
   - Contains 24 collision meshes for interaction surfaces
   - Inertial properties from CAD export

2. **Probe** (floating)
   - task_board_probe: Manipulable object (mass: 0.006 kg)
   - Has freejoint for 6-DOF motion
   - Position: [-0.10, -0.007, 0.019] m

3. **Cable Plug** (floating)
   - task_board_cable_plug: Connectable object (mass: 0.009 kg)
   - Has freejoint for 6-DOF motion
   - Position: [0.038, 0.019, 0.019] m

4. **Fixed Components**
   - Banana plugs (red and black)
   - Various mounting points and test interface

### Physics Parameters

**Default Settings in task_board.xml:**
```xml
<option timestep="0.002" integrator="RK4" gravity="0 0 -9.81">
    <flag energy="enable" contact="enable" multicoll="enable"/>
</option>
```

- **Timestep**: 0.002 s (500 Hz physics simulation)
- **Integrator**: RK4 (4th order Runge-Kutta) - good accuracy
- **Gravity**: 9.81 m/s² downward
- **Energy Tracking**: Enabled for debugging
- **Multi-collision**: Enabled for complex interactions

**Contact Parameters:**
```xml
<contact condim="4" friction="0.5 0.5 0.0001" 
         solimp="0.9 0.99 0.001" solref="0.02 1" />
```

- **Friction**: 0.5 (kinetic, static)
- **Soft contact**: Enabled for stability
- **Collision damping**: 0.0001

## ROS2 Integration

### Published Topics

| Topic | Message Type | Description |
|-------|--------------|-------------|
| `mujoco/body_states` | `std_msgs/Float64MultiArray` | Position/quaternion of all bodies |
| `mujoco/sensor_data` | `std_msgs/Float64MultiArray` | Raw sensor readings |
| `mujoco/probe_state` | `geometry_msgs/TransformStamped` | Probe transform in world frame |
| `mujoco/cable_plug_state` | `geometry_msgs/TransformStamped` | Cable plug transform in world frame |

### Subscribed Topics

| Topic | Message Type | Description |
|-------|--------------|-------------|
| `mujoco/control_command` | `std_msgs/Float64MultiArray` | Actuator control signals |

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model_path` | string | auto-detected | Path to task_board.xml |
| `sim_rate` | int | 500 | Simulation update frequency (Hz) |
| `sim_timestep` | float | 0.002 | Physics timestep (seconds) |
| `enable_rendering` | bool | false | Enable visualization |

## Usage Examples

### 1. Basic Simulation
```bash
# Start simulator (publishes on mujoco/* topics)
ros2 launch board_mujoco_sim mujoco_simulator_launch.py
```

### 2. With Visualization
```bash
# In terminal 1
ros2 launch board_mujoco_sim mujoco_simulator_launch.py

# In terminal 2
ros2 launch board_mujoco_sim mujoco_visualizer_launch.py
```

### 3. Custom Simulation Rate
```bash
# Run at 1000 Hz (0.001 s timestep)
ros2 launch board_mujoco_sim mujoco_simulator_launch.py \
    sim_rate:=1000 \
    sim_timestep:=0.001
```

### 4. Send Control Commands
```bash
# Publish control command (e.g., move actuators)
ros2 topic pub /mujoco/control_command std_msgs/Float64MultiArray \
    "data: [0.1, 0.2, 0.3]"
```

### 5. Monitor Probe Position
```bash
# Subscribe to probe state
ros2 topic echo /mujoco/probe_state
```

## Converting URDF to MuJoCo Format

### Why Convert?
- **Performance**: MuJoCo is optimized for physics simulation
- **Accuracy**: Better contact handling for complex geometries
- **Features**: Native support for constraint, actuation, sensors
- **Rendering**: Integrated visualization capabilities

### Conversion Process

See detailed guide: [URDF_TO_MUJOCO_CONVERSION.md](docs/URDF_TO_MUJOCO_CONVERSION.md)

**Key Steps:**
1. Parse URDF XML structure
2. Convert body hierarchy to nested bodies
3. Transform geometry (visual → no collision, collision → collision)
4. Update mesh file paths
5. Add physics parameters (friction, contact)
6. Define sensors
7. Validate model

### Original Files (Reference)
- `task_board.urdf`: Complete URDF model (reference only)
- `*.urdf.xacro`: URDF macro files

## Sensor Data

### Available Sensors

The model includes sensors for:
- **Position** (framepos): Body center-of-mass position
- **Orientation** (framequat): Body orientation as quaternion
- **Linear Velocity** (framelinvel): Body linear velocity
- **Angular Velocity** (frameangvel): Body angular velocity

### Accessing Sensor Data in Python

```python
import mujoco

# Load model and data
model = mujoco.MjModel.from_xml_path('task_board.xml')
data = mujoco.MjData(model)

# Step simulation
mujoco.mj_step(model, data)

# Get body position
probe_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, 'task_board_probe')
probe_pos = data.xpos[probe_id]  # [x, y, z]
probe_quat = data.xquat[probe_id]  # [w, x, y, z]

# Get all sensor readings
for i in range(model.nsensor):
    sensor = model.sensor(i)
    adr = sensor.adr
    dim = sensor.dim
    sensor_value = data.sensordata[adr:adr+dim]
```

## Performance Optimization

### Simulation Speed

**Typical Performance:**
- **Simulation**: 1-2x real-time on modern CPU
- **Rendering**: 60 FPS with visualization
- **Update Rate**: Configurable (default 500 Hz = 2ms timestep)

### Optimization Tips

1. **Reduce Collision Meshes**
   - Disable visual-only meshes from collision
   - Use simpler collision primitives where possible

2. **Adjust Timestep**
   - Larger timestep = faster but less accurate
   - Smaller timestep = slower but more accurate
   - Default 0.002 s is good balance

3. **Use Faster Integrator** (if acceptable accuracy)
   - "Euler": Fastest but less stable
   - "RK4": Default, good accuracy
   - "implicit": Most stable but slowest

4. **Batch Operations**
   - Publish sensor data less frequently if not needed
   - Use decimation in launch parameters

## Troubleshooting

### Model Won't Load
```bash
# Check model path
echo "Model path: $(ros2 pkg prefix board_description)/share/board_description/urdf/task_board.xml"

# Validate XML
python3 -c "import mujoco; mujoco.MjModel.from_xml_path('task_board.xml')"
```

### Simulation Diverges (NaN values)
- Check inertia tensor (must be positive-definite)
- Reduce timestep
- Adjust contact parameters
- Check for overlapping meshes

### Performance Issues
- Reduce simulation rate
- Disable visualization while recording data
- Check CPU usage: `top` or system monitor
- Profile with: `python3 -m cProfile simulator.py`

### Visualization Not Starting
- Ensure X11 forwarding enabled (SSH)
- Check MuJoCo rendering requirements
- Update graphics drivers
- Try headless mode if remote

## Advanced Topics

### Adding Custom Sensors

Edit `task_board.xml` in `<sensor>` section:
```xml
<sensor>
    <!-- Add custom sensor -->
    <accelerometer name="probe_accel" body="task_board_probe"/>
    <gyro name="probe_gyro" body="task_board_probe"/>
    <force name="contact_force" site="contact_point"/>
</sensor>
```

### Adding Actuators

```xml
<actuator>
    <motor name="probe_motor" joint="probe_joint" gear="1.0" />
</actuator>
```

### Custom Constraints

```xml
<equality>
    <!-- Constraint definitions -->
    <weld body1="body1" body2="body2" />
    <connect body1="body1" body2="body2" />
</equality>
```

## Integration with Other ROS2 Nodes

### Connection Points

1. **board_recorder**: Subscribe to `mujoco/sensor_data` for recording
2. **board_joint_pub**: Publish to `mujoco/control_command`
3. **Custom controllers**: Use topics for feedback control

### Example Integration
```
board_controller → publishes on mujoco/control_command
                 → board_mujoco_sim consumes commands
board_mujoco_sim → publishes on mujoco/probe_state
                 → board_recorder subscribes
                 → custom_controller subscribes
```

## Resources

- [MuJoCo Official Docs](https://mujoco.readthedocs.io/)
- [MJCF Format Reference](https://mujoco.readthedocs.io/en/latest/XMLreference.html)
- [ROS2 Documentation](https://docs.ros.org/en/humble/)
- [URDF Specification](http://wiki.ros.org/urdf/XML)

## Support and Debugging

### Enable Debug Logging
```bash
# Set ROS2 log level
ros2 run board_mujoco_sim mujoco_simulator --ros-args --log-level DEBUG
```

### Check System Status
```bash
# Monitor topics
ros2 topic list
ros2 topic hz /mujoco/sensor_data

# Check parameter values
ros2 param list /board_mujoco_simulator
ros2 param get /board_mujoco_simulator sim_rate
```

## Future Enhancements

- [ ] Contact force feedback
- [ ] Advanced constraint simulation
- [ ] Real-time reconfiguration
- [ ] Hardware-in-the-loop capability
- [ ] Gazebo integration layer
- [ ] RViz plugin for visualization

---

**Project**: Task Board Digital Twin  
**Framework**: ROS2 + MuJoCo  
**Last Updated**: 2024  
**Status**: Active Development
