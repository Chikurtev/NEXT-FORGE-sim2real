# Hardware Bridge and Real Hardware Integration

## Overview

The Hardware Bridge package enables seamless integration between the MuJoCo simulation and the real Robothon Task Board hardware. It provides a unified interface that allows the same ROS2 nodes to work with either simulated or real hardware.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              ROS2 Application Nodes                      │
│  (Controllers, Recorders, Planners, etc.)                │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐    ┌────▼─────┐  ┌───▼───┐
   │Hardware │    │Simulator │  │Adapter│
   │Bridge   │    │          │  │       │
   │(mode)   │    │          │  │       │
   └────┬────┘    └────┬─────┘  └───┬───┘
        │              │            │
   ┌────▼───────────────┼────────────┴───┐
   │                    │                │
   │            ┌───────▼────────┐   ┌──▼─────┐
   │            │ MuJoCo Topics  │   │ HW API │
   │            │ (simulation)   │   │(real)  │
   │            └────────────────┘   └────────┘
```

## Mode Operation

### Simulation Mode

When `mode: simulation`, the bridge:
1. Subscribes to MuJoCo simulation topics
2. Adapts simulation state to hardware-like sensor readings
3. Provides a hardware-like interface to ROS2 nodes

**Topics:**
- Input: `mujoco/probe_state`, `mujoco/cable_plug_state`, `mujoco/body_states`
- Output: `hardware/probe_inserted`, `hardware/cable_plugged`, `hardware/state`

**Flow:**
```
MuJoCo Simulator
       │
       ├──→ probe_state (TransformStamped)
       │
       ├──→ cable_plug_state (TransformStamped)
       │
       └──→ body_states (Float64MultiArray)
             │
             ▼
    Sim Hardware Adapter
             │
             ├──→ hardware/probe_inserted (Bool)
             │
             ├──→ hardware/cable_plugged (Bool)
             │
             └──→ hardware/state (Float64MultiArray)
```

### Hardware Mode

When `mode: hardware`, the bridge:
1. Connects to real task board via micro-ROS
2. Subscribes to real hardware sensors
3. Bridges commands to real hardware

**Topics (from real board):**
- `/robothon_taskboard_status` - Task board status
- `/robothon_task_status` - Current task status
- Custom sensor topics

**Configuration:**
```json
{
  "hardware": {
    "address": "192.168.1.100",
    "port": 8888,
    "timeout": 5.0
  }
}
```

## Real Hardware Integration

### Prerequisites

1. **Task Board Hardware Setup:**
   - M5Stack StickC Plus2 or M5Stack CORE2
   - Robothon firmware installed (from peterso/robotlearningblock)
   - WiFi connected and provisioned

2. **ROS2 Environment:**
   - ROS2 Humble or compatible
   - micro-ROS Agent running and connected to the task board

3. **Network:**
   - Task board and ROS2 host on same network or routable network

### Connecting to Real Hardware

#### Step 1: Start micro-ROS Agent

```bash
# Option 1: Using Docker
docker run -it --rm --privileged --net=host --ipc host \
    microros/micro-ros-agent:humble udp4 --port 8888 -v4

# Option 2: Built locally
source microros_agent_ws/install/local_setup.bash
ros2 run micro_ros_agent micro_ros_agent udp4 --port 8888 -v5
```

#### Step 2: Configure Task Board

Connect to task board WiFi provisioning interface:
- SSID: "Robothon Task Board" + last 3 MAC chars
- Open browser to board IP
- Configure micro-ROS Agent address/port

Or use button combinations:
- **Reset WiFi**: RED_BUTTON + BLUE_BUTTON during boot
- **Local mode**: BUTTON_A during boot
- **Start task**: BUTTON_B

#### Step 3: Start Hardware Bridge

```bash
# With real task board on default network
ros2 launch board_hardware_bridge hardware_bridge_launch.py

# With custom address/port
ros2 launch board_hardware_bridge hardware_bridge_launch.py \
    hardware_address:=192.168.1.100 \
    hardware_port:=8888
```

#### Step 4: Verify Connection

```bash
# Check if bridge is operational
ros2 topic echo board/bridge_status

# Monitor hardware state
ros2 topic echo hardware/state

# Check for real board topics
ros2 topic list | grep robothon
```

## ROS2 Topic Mapping

### Simulation Mode Topics

| Topic | Type | Direction | Description |
|-------|------|-----------|-------------|
| `mujoco/probe_state` | TransformStamped | Input | Probe position/orientation from MuJoCo |
| `mujoco/cable_plug_state` | TransformStamped | Input | Cable plug position/orientation |
| `mujoco/body_states` | Float64MultiArray | Input | All body states |
| `hardware/probe_inserted` | Bool | Output | Probe detection status |
| `hardware/cable_plugged` | Bool | Output | Cable connection status |
| `hardware/state` | Float64MultiArray | Output | Unified hardware state |
| `board/bridge_status` | String (JSON) | Output | Bridge operational status |

### Hardware Mode Topics

| Topic | Type | Direction | Description |
|-------|------|-----------|-------------|
| `robothon_taskboard_status` | TaskBoardStatus | Input | Real board status |
| `robothon_task_status` | TaskStatus | Input | Real task status |
| `/taskboard_execute_task` | ExecuteTask (action) | Bidirectional | Execute task action |

## Configuration File

**Location:** `board_hardware_bridge/config/default_bridge_config.json`

```json
{
  "bridge": {
    "mode": "simulation",        // "simulation" or "hardware"
    "log_level": "INFO"
  },
  "simulation": {
    "model_path": "task_board.xml",
    "timestep": 0.002,
    "update_rate": 500
  },
  "hardware": {
    "address": "localhost",
    "port": 8888,
    "timeout": 5.0
  },
  "sensors": {
    "probe": {
      "detection_threshold": 0.01,
      "frame": "probe_link"
    },
    "cable": {
      "connector_position": [0.038, 0.019, 0.0],
      "detection_threshold": 0.01,
      "frame": "cable_link"
    }
  }
}
```

## Switching Modes

### To Switch from Simulation to Hardware

1. Stop simulation bridge:
   ```bash
   ros2 launch board_hardware_bridge complete_simulation_with_bridge_launch.py
   # Ctrl+C to stop
   ```

2. Ensure hardware is ready:
   ```bash
   # Verify micro-ROS Agent running
   docker ps | grep micro-ros-agent
   
   # Check network connectivity
   ping <task-board-ip>
   ```

3. Start hardware bridge:
   ```bash
   ros2 launch board_hardware_bridge hardware_bridge_launch.py \
       hardware_address:=<task-board-ip>
   ```

### To Switch from Hardware to Simulation

1. Stop hardware bridge:
   ```bash
   # Ctrl+C to stop the running launch
   ```

2. Start simulation:
   ```bash
   ros2 launch board_hardware_bridge complete_simulation_with_bridge_launch.py
   ```

## Sensor Mapping

### Probe Detection

**Simulation:** Position-based detection
- Detected if z > -0.01m (above board surface)

**Hardware:** Real proximity/contact sensors
- Hardware provides actual sensor reading via ROS2

### Cable Connection

**Simulation:** Distance-based detection
- Connected if distance to connector < 0.01m
- Position within valid z range

**Hardware:** Real connector sensors
- Hardware provides actual connection status

## Troubleshooting

### Bridge Not Connecting to Hardware

```bash
# Check if board is reachable
ping <task-board-ip>

# Check if micro-ROS Agent is running
docker logs <agent-container-id>
# or
ros2 daemon stop && ros2 daemon start
ros2 topic list | grep robothon
```

### Topics Not Publishing

```bash
# Check bridge status
ros2 topic echo board/bridge_status

# Verify mode
ros2 param get /board_hardware_bridge mode

# Check hardware connectivity
ros2 topic list | grep hardware
```

### Simulation State Not Updating

```bash
# Verify MuJoCo simulator is running
ros2 topic list | grep mujoco

# Check adapter status
ros2 node info /sim_hardware_adapter
```

## Advanced Usage

### Custom Configuration

Create your own config file:

```bash
cp board_hardware_bridge/config/default_bridge_config.json \
   my_board_config.json

# Edit my_board_config.json with your settings

# Use custom config
ros2 launch board_hardware_bridge simulation_bridge_launch.py \
    config_file:=$(pwd)/my_board_config.json
```

### Monitoring Bridge Performance

```bash
# Monitor topic frequencies
ros2 topic hz hardware/state

# Check latency
ros2 topic echo --include-all /hardware/state | head -20

# Monitor CPU usage
top -p $(pgrep -f hardware_bridge)
```

### Recording Hardware Behavior

```bash
# Record all topics
ros2 bag record -a --output hardware_recording

# Record specific topics
ros2 bag record hardware/state hardware/probe_inserted hardware/cable_plugged
```

## References

- [Robothon Task Board Firmware](https://github.com/peterso/robotlearningblock/tree/main/idf/taskboard)
- [micro-ROS Documentation](https://micro.ros.org/)
- [ROS2 Topic Documentation](https://docs.ros.org/en/humble/Concepts/Intermediate/About-Topics.html)
