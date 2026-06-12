# Docker Integration Guide

## Overview

Complete Docker containerization for the ROS2 Task Board Digital Twin project. This enables:

- ✅ **One-command setup** - No local dependencies needed
- ✅ **Isolation** - System dependencies contained
- ✅ **Reproducibility** - Same environment everywhere
- ✅ **Easy switching** - Simulation ↔ Hardware mode
- ✅ **Cross-platform** - Linux, macOS, Windows

## Prerequisites

### System Requirements

- **Docker**: 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose**: 1.29+ (included with Docker Desktop)
- **4GB RAM minimum** (8GB+ recommended)
- **10GB disk space** for image and containers

### Verify Installation

```bash
docker --version
docker-compose --version
```

## Quick Start

### 1. Build Docker Image

**Linux/macOS:**
```bash
cd ~/ros_projects/ros2_ws
chmod +x docker_manager.sh
./docker_manager.sh build
```

**Windows (PowerShell):**
```powershell
cd C:\Users\dchik\Documents\ros_projects\ros2_ws
docker build -t ros2_taskboard:latest -f Dockerfile .
```

**Or directly:**
```bash
docker build -t ros2_taskboard:latest -f Dockerfile .
```

### 2. Start Containers

```bash
docker-compose up -d
```

Verify containers are running:
```bash
docker ps
```

Expected output:
- `ros2_taskboard` - Main ROS2 container
- `micro_ros_agent` - Micro-ROS for hardware communication
- `rosbridge_ws` - WebSocket server for web visualization

### 3. Run Simulation

**In new terminal:**

**Linux/macOS:**
```bash
./docker_manager.sh sim
```

**Windows:**
```powershell
docker_manager.bat sim
```

**Or directly:**
```bash
docker exec -it ros2_taskboard bash -c \
  "source /opt/ros/humble/setup.bash && \
   source /root/ros2_ws/install/setup.bash && \
   ros2 launch board_hardware_bridge complete_simulation_with_bridge_launch.py"
```

### 4. Monitor Topics

**In another terminal:**
```bash
docker exec -it ros2_taskboard bash -c \
  "source /opt/ros/humble/setup.bash && \
   source /root/ros2_ws/install/setup.bash && \
   ros2 topic echo hardware/state"
```

## Docker Manager Scripts

### Bash Script (Linux/macOS)

```bash
./docker_manager.sh build      # Build image
./docker_manager.sh start      # Start containers
./docker_manager.sh stop       # Stop containers
./docker_manager.sh sim        # Run simulation
./docker_manager.sh hw <ip>    # Run hardware mode
./docker_manager.sh shell      # Interactive shell
./docker_manager.sh test       # Test model
./docker_manager.sh topics     # List topics
./docker_manager.sh logs       # Show logs
./docker_manager.sh help       # Show help
```

### Batch Script (Windows)

```batch
docker_manager.bat build
docker_manager.bat start
docker_manager.bat stop
docker_manager.bat sim
docker_manager.bat hw 192.168.1.100 8888
docker_manager.bat shell
docker_manager.bat help
```

## Docker Compose Services

### Service: `ros2_taskboard`

**Main ROS2 container** with all packages and dependencies.

Configuration:
- Image: Built from Dockerfile
- Volumes: 
  - `./src` - Source code (read-write)
  - `./install` - Built packages (read-only)
  - `./build` - Build artifacts (read-write)
  - `./recordings` - Recorded data (read-write)
  - `./board_configs` - Configuration files (read-write)
- Network: Host network (direct access to ports)
- X11: Enabled for visualization

### Service: `micro_ros_agent`

**Micro-ROS Agent** for hardware communication.

- Image: `microros/micro-ros-agent:humble`
- Port: 8888 (UDP)
- Purpose: Bridges ROS2 with real task board hardware

### Service: `rosbridge_ws`

**WebSocket bridge** for web-based visualization.

- Image: ROS2 Humble
- Ports: 9090 (WebSocket)
- Certificates: Self-signed SSL/TLS
- Purpose: Web clients can connect via secure WebSocket

## Container Volumes

Mount points for data persistence:

```
Host                              Container
├── ./src/                     →   /root/ros2_ws/src/
├── ./install/                 →   /root/ros2_ws/install/
├── ./build/                   →   /root/ros2_ws/build/
├── ./recordings/              →   /root/ros2_ws/recordings/
├── ./board_configs/           →   /root/ros2_ws/board_configs/
├── ./launch/                  →   /root/ros2_ws/launch/
├── /tmp/.X11-unix             →   /tmp/.X11-unix (visualization)
└── ~/.Xauthority              →   /root/.Xauthority (X11 auth)
```

## Usage Patterns

### Development Workflow

```bash
# 1. Build image (first time)
./docker_manager.sh build

# 2. Start containers
./docker_manager.sh start

# 3. In terminal 1: Run simulation
./docker_manager.sh sim

# 4. In terminal 2: Monitor topics
docker exec -it ros2_taskboard bash -c \
  "source /opt/ros/humble/setup.bash && \
   source /root/ros2_ws/install/setup.bash && \
   ros2 topic hz hardware/state"

# 5. In terminal 3: Edit code
# (Changes in ./src/ are immediately visible in container)

# 6. Rebuild packages
docker exec -it ros2_taskboard bash -c \
  "cd /root/ros2_ws && \
   source /opt/ros/humble/setup.bash && \
   colcon build"

# 7. Restart simulation
# (Go back to terminal 1, Ctrl+C, run again)
```

### Testing Environment

```bash
# Build fresh image
./docker_manager.sh build

# Start containers
./docker_manager.sh start

# Run tests
docker exec -it ros2_taskboard bash -c \
  "cd /root/ros2_ws && \
   source /opt/ros/humble/setup.bash && \
   colcon build --packages-select board_hardware_bridge && \
   colcon test --packages-select board_hardware_bridge"

# Check results
docker exec -it ros2_taskboard bash -c \
  "cd /root/ros2_ws && \
   colcon test-result --verbose"
```

### Real Hardware Deployment

```bash
# 1. Make sure task board is powered and provisioned
ping 192.168.1.100

# 2. Start containers
./docker_manager.sh start

# 3. Run hardware bridge
./docker_manager.sh hw 192.168.1.100 8888

# 4. Monitor in another terminal
docker exec -it ros2_taskboard bash -c \
  "source /opt/ros/humble/setup.bash && \
   source /root/ros2_ws/install/setup.bash && \
   ros2 topic echo hardware/probe_inserted"
```

## Environment Variables

Set in docker-compose.yml or pass via `-e`:

```bash
# ROS2 domain (for multi-machine ROS2)
ROS_DOMAIN_ID=0

# Display server for X11 forwarding
DISPLAY=:0  # Unix/Linux
DISPLAY=host.docker.internal:0  # macOS/Windows
```

## Building and Deployment

### Build for Different Platforms

```bash
# Build for current platform
docker build -t ros2_taskboard:latest -f Dockerfile .

# Build for specific platform (cross-compile)
docker build --platform linux/amd64 -t ros2_taskboard:amd64 .
docker build --platform linux/arm64 -t ros2_taskboard:arm64 .
```

### Push to Registry

```bash
# Tag image
docker tag ros2_taskboard:latest myregistry/ros2_taskboard:latest

# Login to registry
docker login myregistry

# Push
docker push myregistry/ros2_taskboard:latest
```

## Troubleshooting

### Container fails to start

```bash
# Check logs
docker-compose logs ros2_taskboard

# Check if port 8888 is available (micro-ROS)
netstat -an | grep 8888

# Kill conflicting process
lsof -i :8888
```

### MuJoCo visualization not working

```bash
# Ensure X11 forwarding enabled
echo $DISPLAY

# On macOS with XQuartz:
defaults write org.xquartz.X11 nolisten_tcp -boolean false
killall Xvfb

# Restart XQuartz
open -a XQuartz
```

### Topics not visible between containers

```bash
# Check ROS_DOMAIN_ID
docker exec -it ros2_taskboard bash -c "echo \$ROS_DOMAIN_ID"

# Restart daemon
docker exec -it ros2_taskboard bash -c \
  "source /opt/ros/humble/setup.bash && \
   ros2 daemon stop && \
   ros2 daemon start"
```

### Disk space issues

```bash
# Clean up Docker
docker system prune -a

# Remove specific image
docker rmi ros2_taskboard:latest

# Check disk usage
docker system df
```

## Advanced Configuration

### Custom Dockerfile

Edit `Dockerfile` to:
- Add additional ROS2 packages
- Install system dependencies
- Set different base image

```dockerfile
# Example: Add additional packages
RUN apt-get update && apt-get install -y \
    ros-humble-package-name \
    && rm -rf /var/lib/apt/lists/*
```

### Custom docker-compose

Edit `docker-compose.yml` to:
- Add additional services
- Mount different volumes
- Configure networking

```yaml
services:
  custom_service:
    image: some-image
    depends_on:
      - ros2_taskboard
```

### Environment-specific configs

```bash
# Create .env file
echo "ROS_DOMAIN_ID=1" > .env
echo "DISPLAY=host.docker.internal:0" >> .env

# Use in docker-compose
docker-compose --env-file .env up -d
```

## Performance Optimization

### Reduce image size

```dockerfile
# Use multi-stage builds
FROM ros:humble AS builder
# ... build steps ...

FROM ros:humble-ros-core
# Copy only necessary files
COPY --from=builder /build /app
```

### Improve build speed

```bash
# Use BuildKit
DOCKER_BUILDKIT=1 docker build -t ros2_taskboard:latest .

# Cache optimization
docker build --cache-from ros2_taskboard:latest -t ros2_taskboard:latest .
```

### Resource limits

```yaml
services:
  ros2_taskboard:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

## Networking

### Expose Services

```yaml
ports:
  - "8888:8888/udp"  # Micro-ROS
  - "9090:9090"      # Rosbridge WebSocket
```

### Host Network

```yaml
network_mode: host  # Direct access to host network
```

### Custom Network

```yaml
networks:
  taskboard_net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

## Backup and Recovery

### Save container state

```bash
# Create backup
docker commit ros2_taskboard ros2_taskboard:backup

# Save image to file
docker save ros2_taskboard:backup | gzip > taskboard_backup.tar.gz
```

### Restore from backup

```bash
# Load from file
docker load < taskboard_backup.tar.gz

# Run from backup
docker run -it ros2_taskboard:backup bash
```

## Security Considerations

- ⚠️ Containers run with default security settings
- ⚠️ Privileged mode enabled for hardware access
- ⚠️ Host network mode - no isolation
- ⚠️ Self-signed certificates for Rosbridge

For production:
- Use secrets management
- Implement network policies
- Enable user namespaces
- Use signed images

## Next Steps

1. ✅ Build image: `./docker_manager.sh build`
2. ✅ Start containers: `./docker_manager.sh start`
3. ✅ Run simulation: `./docker_manager.sh sim`
4. ✅ Monitor topics: `docker exec -it ros2_taskboard ros2 topic echo hardware/state`

## References

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [ROS 2 Docker](https://docs.ros.org/en/humble/How-To-Guides/Run-ROS2-in-Docker.html)
- [MuJoCo Docker](https://mujoco.readthedocs.io/en/latest/python.html)

---

**Quick Commands Reference:**

```bash
# Build
docker build -t ros2_taskboard:latest -f Dockerfile .

# Start
docker-compose up -d

# Stop
docker-compose down

# Run simulation
docker exec -it ros2_taskboard ros2 launch board_hardware_bridge complete_simulation_with_bridge_launch.py

# Shell
docker exec -it ros2_taskboard bash

# Logs
docker-compose logs -f

# Test model
docker exec -it ros2_taskboard python3 src/board_mujoco_sim/board_mujoco_sim/test_model.py

# List images
docker image ls

# Remove image
docker rmi ros2_taskboard:latest
```

---

For detailed documentation on each component, see:
- [MuJoCo Integration Guide](src/board_mujoco_sim/docs/MUJOCO_INTEGRATION_GUIDE.md)
- [Hardware Bridge Integration](src/board_hardware_bridge/docs/HARDWARE_INTEGRATION.md)
- [Project README](README.md)
