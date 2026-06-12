# URDF to MuJoCo Conversion Guide

## Overview
This document describes the process of converting URDF files to MuJoCo MJCF format for the task board project.

## Key Differences Between URDF and MuJoCo MJCF

### 1. File Structure
```
URDF Format:
<robot name="...">
  <link>...</link>
  <joint>...</joint>
  ...
</robot>

MuJoCo MJCF Format:
<mujoco model="...">
  <compiler>...</compiler>
  <asset>...</asset>
  <default>...</default>
  <worldbody>
    <body>...</body>
  </worldbody>
  <sensor>...</sensor>
</mujoco>
```

### 2. Link to Body Conversion
```
URDF Link:
<link name="body_name">
  <inertial>
    <mass value="1.0"/>
    <inertia .../>
  </inertial>
  <visual>...</visual>
  <collision>...</collision>
</link>

MuJoCo Body:
<body name="body_name">
  <inertial mass="1.0" pos="..." quat="..."/>
  <geom name="visual" class="visual" type="mesh" mesh="..."/>
  <geom name="collision" class="collision" type="mesh" mesh="..."/>
</body>
```

### 3. Joint Conversion
```
URDF Joint:
<joint name="joint_name" type="fixed">
  <parent link="parent_link"/>
  <child link="child_link"/>
  <origin xyz="..." rpy="..."/>
</joint>

MuJoCo Hierarchy:
<body name="parent_link">
  <body name="child_link" pos="..." quat="...">
    <!-- Child content -->
  </body>
</body>
```

### 4. Mesh Path Handling
```
URDF (uses ROS package references):
<mesh filename="package://board_description/meshes/stl/file.stl"/>

MuJoCo (uses relative or absolute paths):
<asset>
  <mesh name="MeshName" file="stl/file.stl"/>
</asset>
<geom type="mesh" mesh="MeshName"/>
```

## Conversion Steps for Task Board

### Step 1: Analyze URDF Structure
- Parse the URDF tree hierarchy
- Identify all links, joints, and collision/visual geometries
- Extract inertial properties (mass, inertia tensor)

### Step 2: Create MJCF Header
```xml
<?xml version="1.0" ?>
<mujoco model="task_board">
  <compiler meshdir="meshes" texturedir="textures" angle="radian" autolimits="false" balanceinertia="false" />
```

### Step 3: Define Assets
- List all mesh files with proper file paths
- Create material definitions if needed
- Specify texture references

```xml
<asset>
  <mesh name="TaskBoardBody" file="stl/TaskBoardMain.stl" scale="1.0 1.0 1.0"/>
  <!-- More meshes... -->
</asset>
```

### Step 4: Define Defaults
- Collision properties (friction, damping)
- Visual properties (colors, transparency)
- Contact parameters

```xml
<default>
  <default class="task_board_visual">
    <geom contype="0" conaffinity="0"/>
  </default>
  <default class="task_board_collision">
    <geom rgba="0.9 0.9 0.9 1.0" group="3"/>
  </default>
</default>
```

### Step 5: Build Body Hierarchy
- Convert URDF tree to nested body elements
- Apply transformations (positions, quaternions)
- Flatten fixed joints into hierarchy

### Step 6: Convert Geometries
- Visual geometries use `contype="0" conaffinity="0"` (no collision)
- Collision geometries use proper contact parameters
- Convert quaternion format if needed

### Step 7: Add Sensors
- Frame position sensors
- Frame quaternion sensors
- Velocity sensors
- Force/torque sensors

```xml
<sensor>
  <framepos name="body_pos" objtype="body" objname="body_name"/>
  <framequat name="body_quat" objtype="body" objname="body_name"/>
  <framelinvel name="body_linvel" objtype="body" objname="body_name"/>
  <frameangvel name="body_angvel" objtype="body" objname="body_name"/>
</sensor>
```

## Specific Conversions for Task Board

### Main Body (Fixed)
```
URDF:
- task_board_main: parent
  - task_board_body: child with mass ~7.6 kg

MuJoCo:
<body name="task_board_body" pos="0 0 0">
  <inertial mass="7.616941928863525" pos="..." quat="..."/>
  <!-- Visual and collision geometries -->
</body>
```

### Probe (Floating Object)
```
URDF:
- task_board_probe: floating link

MuJoCo:
<body name="task_board_probe" pos="-0.101844 -0.007 0.019">
  <freejoint/>
  <inertial mass="0.00623..." pos="..." quat="..."/>
  <!-- Geometries -->
</body>
```

### Cable Plug (Floating Object)
```
URDF:
- task_board_cable_plug: floating link

MuJoCo:
<body name="task_board_cable_plug" pos="0.03844... 0.01890... 0.019">
  <freejoint/>
  <inertial mass="0.00914..." pos="..." quat="..."/>
  <!-- Geometries -->
</body>
```

## Physics Parameter Mapping

### Timestep
```
URDF: Typically not specified
MuJoCo: <option timestep="0.002"/> (500 Hz)
```

### Gravity
```
URDF: <gravity xyz="0 0 -9.81"/> (if specified)
MuJoCo: <option gravity="0 0 -9.81"/>
```

### Friction
```
URDF: Typically in contact properties
MuJoCo: <contact friction="0.5 0.5 0.0001"/>
```

### Inertia Tensor
```
URDF: ixx, iyy, izz (diagonal components only)
MuJoCo: diaginertia="ixx iyy izz"
Note: Off-diagonal components set to 0 in both
```

## Quaternion Format Handling

### URDF Roll-Pitch-Yaw (RPY)
```
rpy = [roll, pitch, yaw]
Converted to quaternion [w, x, y, z]
```

### MuJoCo Quaternion
```
quat = [w, x, y, z]
Used directly from URDF conversion
```

## Common Issues and Solutions

### Issue 1: Mesh Not Found
**Cause**: Incorrect mesh paths
**Solution**: Ensure meshdir is set correctly and mesh files exist

### Issue 2: Model Too Heavy
**Cause**: Excessive contact geometries or high gravity
**Solution**: Reduce collision mesh count, tune timestep

### Issue 3: Unstable Simulation
**Cause**: Poor contact parameters or incorrect inertia
**Solution**: Use balanceinertia="true", tune solimp/solref

### Issue 4: Rendering Issues
**Cause**: Mesh scale or orientation problems
**Solution**: Verify mesh scale and quaternion values

## Validation Checklist

- [ ] All mesh files referenced and found
- [ ] Quaternions are normalized (magnitude = 1)
- [ ] Inertia tensors are positive definite
- [ ] Contact parameters are physically reasonable
- [ ] Body hierarchy matches intended structure
- [ ] Floating objects have freejoint
- [ ] Sensors are properly defined

## Tools and Scripts

### Utility Functions (in Python)
```python
import mujoco

# Load and validate model
model = mujoco.MjModel.from_xml_file('task_board.xml')
data = mujoco.MjData(model)

# Check model statistics
print(f"Bodies: {model.nbody}")
print(f"Joints: {model.njnt}")
print(f"Sensors: {model.nsensor}")
print(f"Geoms: {model.ngeom}")
```

## References

- [MuJoCo XML Documentation](https://mujoco.readthedocs.io/en/latest/XMLreference.html)
- [URDF Specification](http://wiki.ros.org/urdf/XML)
- [Quaternion Mathematics](https://en.wikipedia.org/wiki/Quaternion)
