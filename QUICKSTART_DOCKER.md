# Docker Quick Start Guide

## 🚀 One-Line Setup

### Linux/macOS
```bash
cd ~/ros_projects/ros2_ws && chmod +x docker_manager.sh && \
./docker_manager.sh build && ./docker_manager.sh start && ./docker_manager.sh sim
```

### Windows (PowerShell)
```powershell
cd C:\Users\dchik\Documents\ros_projects\ros2_ws
docker build -t ros2_taskboard:latest -f Dockerfile .
docker-compose up -d
docker exec -it ros2_taskboard bash -c "source /opt/ros/humble/setup.bash && source /root/ros2_ws/install/setup.bash && ros2 launch board_hardware_bridge complete_simulation_with_bridge_launch.py"
```

## 📋 3-Step Setup

### Step 1: Build Image
```bash
./docker_manager.sh build
# This takes 5-10 minutes on first run
```

### Step 2: Start Containers
```bash
./docker_manager.sh start
# Verify: docker ps (should show ros2_taskboard, micro_ros_agent, rosbridge_ws)
```

### Step 3: Run Simulation
```bash
./docker_manager.sh sim
# Should show MuJoCo window and bridge running
```

## 🔍 Common Commands

### Monitor Bridge Status
```bash
docker exec -it ros2_taskboard bash -c \
  "source /opt/ros/humble/setup.bash && \
   source /root/ros2_ws/install/setup.bash && \
   ros2 topic echo board/bridge_status"
```

### Check Probe Detection
```bash
docker exec -it ros2_taskboard bash -c \
  "source /opt/ros/humble/setup.bash && \
   source /root/ros2_ws/install/setup.bash && \
   ros2 topic hz hardware/probe_inserted"
```

### Open Shell
```bash
./docker_manager.sh shell
# Now you're inside container with full access
```

### Stop Everything
```bash
./docker_manager.sh stop
```

## 🔧 Hardware Mode

```bash
# Connect to real board at 192.168.1.100
./docker_manager.sh hw 192.168.1.100 8888
```

## ✅ Verify Success

Run in separate terminals:

**Terminal 1:** Check bridge is running
```bash
docker exec -it ros2_taskboard bash -c \
  "source /opt/ros/humble/setup.bash && \
   source /root/ros2_ws/install/setup.bash && \
   ros2 topic list | grep hardware"
```

Expected output:
```
hardware/cable_plugged
hardware/probe_inserted
hardware/state
```

**Terminal 2:** Monitor state
```bash
docker exec -it ros2_taskboard bash -c \
  "source /opt/ros/humble/setup.bash && \
   source /root/ros2_ws/install/setup.bash && \
   ros2 topic echo hardware/state"
```

Should show continuous stream of position data.

## 🆘 Troubleshooting

### Build fails
```bash
# Clean and rebuild
docker system prune -a
./docker_manager.sh build
```

### Port already in use
```bash
# Find and kill process using port 8888
lsof -i :8888
kill -9 <PID>
```

### No X11 display
```bash
# Linux: Make sure X server running
export DISPLAY=:0

# macOS: Start XQuartz
open -a XQuartz

# Windows: Use WSL2 with vcxsrv or similar
```

## 📦 What's Inside

✅ ROS2 Humble (complete)  
✅ MuJoCo >=2.2.0  
✅ All task board packages  
✅ micro-ROS agent  
✅ Rosbridge WebSocket server  
✅ Development tools (git, cmake, pip3)  
✅ Visualization tools (RViz, MuJoCo viewer)

## 🎯 Next Steps

1. Explore the bridge topics:
   ```bash
   docker exec -it ros2_taskboard bash -c \
     "source /opt/ros/humble/setup.bash && \
      source /root/ros2_ws/install/setup.bash && \
      ros2 topic hz -w 5 hardware/state"
   ```

2. Test model validation:
   ```bash
   ./docker_manager.sh test
   ```

3. Check documentation:
   - [Full Docker Guide](DOCKER_GUIDE.md)
   - [Hardware Bridge Guide](../src/board_hardware_bridge/docs/HARDWARE_INTEGRATION.md)
   - [MuJoCo Guide](../src/board_mujoco_sim/docs/MUJOCO_INTEGRATION_GUIDE.md)

## ⏱️ Timing

| Operation | Time |
|-----------|------|
| Build (first) | 5-10 min |
| Build (cached) | 30 sec |
| Start containers | 3-5 sec |
| First simulation | <5 sec |
| Model validation | <10 sec |

---

**You're ready to go! 🤖**

For more details, see [DOCKER_GUIDE.md](DOCKER_GUIDE.md)
