# MuJoCo Hardware Bridge - Quick Reference Guide

## 🚀 What You've Built

A complete **hardware abstraction layer** that enables seamless switching between:
- **MuJoCo Physics Simulation** (local, fast, deterministic)
- **Real Task Board Hardware** (M5Stack + micro-ROS)

Same ROS2 nodes work with **either mode** - no code changes needed!

## 📋 System Components

```
MuJoCo Simulator (500 Hz) ← Simulation Path
       ↓
Probe/Cable State Topics
       ↓
SimHardware Adapter  ← Detection algorithms
       ↓
Hardware-like Topics (50 Hz) ← Unified Interface
       ↑
Real Board Topics ← Hardware Path (if connected)
```

## 🎯 Three Launch Options

### Option 1: Simulation Only
```bash
ros2 launch board_mujoco_sim mujoco_simulator_launch.py
```
- Just the physics simulation
- No hardware bridge
- Good for testing physics only

### Option 2: Simulation with Bridge (RECOMMENDED)
```bash
ros2 launch board_hardware_bridge complete_simulation_with_bridge_launch.py
```
- ✅ MuJoCo simulator (500 Hz)
- ✅ MuJoCo visualizer
- ✅ Hardware adapter (50 Hz)
- ✅ Hardware bridge
- **Use this for most testing!**

### Option 3: Real Hardware Mode
```bash
# 1. Start micro-ROS Agent in terminal 1:
docker run -it --rm --privileged --net=host microros/micro-ros-agent:humble udp4 --port 8888

# 2. Configure task board (WiFi, provisioning)

# 3. Launch bridge in terminal 2:
ros2 launch board_hardware_bridge hardware_bridge_launch.py \
    hardware_address:=192.168.1.100 \
    hardware_port:=8888
```

## 📊 Topic Quick Reference

### Simulation Topics (from MuJoCo)
- `mujoco/probe_state` → TransformStamped
- `mujoco/cable_plug_state` → TransformStamped  
- `mujoco/body_states` → Float64MultiArray

### Hardware-like Topics (from bridge/adapter)
- `hardware/probe_inserted` → Bool (True/False)
- `hardware/cable_plugged` → Bool (True/False)
- `hardware/state` → Float64MultiArray (positions)
- `board/bridge_status` → JSON status

### Real Board Topics (when connected)
- `robothon_taskboard_status`
- `robothon_task_status`
- `/taskboard_execute_task` (action)

## 🧪 Testing the Bridge

### Monitor Bridge Status
```bash
# In one terminal:
ros2 topic echo board/bridge_status

# Output: mode="simulation" or mode="hardware"
```

### Monitor Probe Detection
```bash
ros2 topic hz hardware/probe_inserted
ros2 topic echo hardware/probe_inserted
```

### Monitor Cable Connection
```bash
ros2 topic hz hardware/cable_plugged
ros2 topic echo hardware/cable_plugged
```

### Check Full Hardware State
```bash
ros2 topic hz hardware/state
ros2 topic echo hardware/state
```

## ⚙️ Configuration

Edit `board_hardware_bridge/config/default_bridge_config.json`:

```json
{
  "bridge": {
    "mode": "simulation"     // ← Change to "hardware"
  },
  "hardware": {
    "address": "localhost",  // ← Set board IP
    "port": 8888             // ← micro-ROS port
  },
  "sensors": {
    "probe": {
      "detection_threshold": 0.01  // ← 1 cm
    },
    "cable": {
      "detection_threshold": 0.01  // ← 1 cm
    }
  }
}
```

## 🔄 Switching Modes

**Simulation → Hardware:**
1. Stop simulation: `Ctrl+C`
2. Start micro-ROS Agent
3. Launch hardware bridge

**Hardware → Simulation:**
1. Stop hardware bridge: `Ctrl+C`
2. Launch simulation with bridge

## 📊 Performance

| Aspect | Value |
|--------|-------|
| MuJoCo Simulation Rate | 500 Hz |
| Hardware Adapter Rate | 50 Hz |
| Bridge Status Update | 5 sec |
| Latency (sim→adapter) | <20 ms |

## 🐛 Troubleshooting

### Bridge not starting
```bash
# Check dependencies
ros2 pkg list | grep board_
ros2 topic list | grep mujoco

# Rebuild if needed
cd ~/ros_projects/ros2_ws
colcon build --packages-select board_hardware_bridge
```

### Topics not publishing
```bash
# Check bridge is running
ros2 node list | grep bridge

# Check adapter is running
ros2 node list | grep adapter

# Check message rates
ros2 topic hz hardware/state
```

### Hardware connection failing
```bash
# Test network connectivity
ping 192.168.1.100

# Verify micro-ROS Agent running
docker ps

# Check ROS2 discovery
ROS_DOMAIN_ID=0 ros2 daemon stop
ROS_DOMAIN_ID=0 ros2 daemon start
ros2 topic list
```

## 📚 Full Documentation

- 📖 [Hardware Integration Guide](../docs/HARDWARE_INTEGRATION.md)
- 📖 [MuJoCo Integration Guide](../board_mujoco_sim/docs/MUJOCO_INTEGRATION_GUIDE.md)
- 📖 [URDF to MuJoCo Conversion](../board_mujoco_sim/docs/URDF_TO_MUJOCO_CONVERSION.md)

## 🎓 Example Code

```python
import rclpy
from std_msgs.msg import Bool

def probe_callback(msg):
    if msg.data:
        print("Probe detected on board!")
    else:
        print("Probe not detected")

rclpy.init()
node = rclpy.create_node('my_app')
node.create_subscription(Bool, 'hardware/probe_inserted', probe_callback, 10)
rclpy.spin(node)
```

See `examples/example_client.py` for complete example.

## 🚦 Next Steps

1. **Test Simulation** (recommended first)
   ```bash
   ros2 launch board_hardware_bridge complete_simulation_with_bridge_launch.py
   ```

2. **Monitor Topics**
   ```bash
   ros2 topic echo hardware/state
   ```

3. **Connect to Real Hardware** (when ready)
   ```bash
   ros2 launch board_hardware_bridge hardware_bridge_launch.py \
       hardware_address:=<board-ip>
   ```

4. **Run Your Application**
   Your nodes work identically with either mode!

---

**Happy robotics! 🤖**
