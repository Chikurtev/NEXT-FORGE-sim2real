# NEXT-FORGE-sim2real Setup Guide for GitHub

This document explains how to set up and deploy NEXT-FORGE-sim2real after cloning from GitHub.

## Quick Clone & Setup

### Clone the Repository

```bash
git clone https://github.com/USERNAME/NEXT-FORGE-sim2real.git
cd NEXT-FORGE-sim2real
```

### Choose Your Setup Method

## Option 1: Docker (Recommended)

**No local dependencies needed!**

```bash
# Make scripts executable
chmod +x docker_manager.sh

# Build Docker image
./docker_manager.sh build

# Start containers
./docker_manager.sh start

# Run simulation
./docker_manager.sh sim
```

**On Windows:**
```powershell
docker build -t ros2_taskboard:latest -f Dockerfile .
docker-compose up -d
docker exec -it ros2_taskboard bash -c "source /opt/ros/humble/setup.bash && source /root/ros2_ws/install/setup.bash && ros2 launch board_hardware_bridge complete_simulation_with_bridge_launch.py"
```

**Verify it's working:**
```bash
# In another terminal
docker exec -it ros2_taskboard bash -c \
  "source /opt/ros/humble/setup.bash && \
   source /root/ros2_ws/install/setup.bash && \
   ros2 topic echo hardware/state"
```

## Option 2: Native Installation

### Prerequisites

- Ubuntu 22.04 LTS or 24.04 LTS
- 8GB RAM recommended
- Git and basic build tools

### Install ROS2 Humble

```bash
# Follow official ROS2 installation
# https://docs.ros.org/en/humble/Installation.html
```

### Build Project

```bash
cd NEXT-FORGE-sim2real
chmod +x scripts/initial_build.bash
./scripts/initial_build.bash
source install/setup.bash
```

### Run Simulation

```bash
ros2 launch board_hardware_bridge complete_simulation_with_bridge_launch.py
```

## Project Structure

```
NEXT-FORGE-sim2real/
├── src/
│   ├── board_mujoco_sim/              # Physics simulator package
│   ├── board_hardware_bridge/         # Hardware bridge package
│   ├── board_description/             # URDF and MuJoCo models
│   └── [other packages]
├── launch/                            # ROS2 launch files
├── scripts/                           # Utility scripts
├── docs/                              # Additional documentation
├── Dockerfile                         # Container definition
├── docker-compose.yml                 # Multi-service setup
├── docker_manager.sh                  # Docker management script
├── README.md                          # Main documentation
├── CONTRIBUTING.md                    # Contribution guidelines
├── CHANGELOG.md                       # Version history
├── LICENSE                            # Apache 2.0 License
└── [other config files]
```

## Quick Commands

### Docker Commands

```bash
# Build image
./docker_manager.sh build

# Start services
./docker_manager.sh start

# Stop services
./docker_manager.sh stop

# Run simulation
./docker_manager.sh sim

# Connect to real hardware
./docker_manager.sh hw 192.168.1.100 8888

# Open shell
./docker_manager.sh shell

# Show help
./docker_manager.sh help
```

### ROS2 Commands (after setup)

```bash
# List topics
ros2 topic list

# Monitor topic
ros2 topic echo hardware/state

# Check topic frequency
ros2 topic hz hardware/state

# Run tests
colcon test

# Build specific package
colcon build --packages-select board_hardware_bridge
```

## Documentation

Start with these in order:

1. **[README.md](README.md)** - Project overview
2. **[QUICKSTART_DOCKER.md](QUICKSTART_DOCKER.md)** - Docker quick start (recommended)
3. **[docs/DOCKER_GUIDE.md](docs/DOCKER_GUIDE.md)** - Full Docker guide
4. **[QUICKSTART_HARDWARE_BRIDGE.md](QUICKSTART_HARDWARE_BRIDGE.md)** - Hardware bridge guide
5. **[src/board_mujoco_sim/docs/MUJOCO_INTEGRATION_GUIDE.md](src/board_mujoco_sim/docs/MUJOCO_INTEGRATION_GUIDE.md)** - MuJoCo details

## Troubleshooting

### Docker build fails

```bash
# Clean Docker and rebuild
docker system prune -a
./docker_manager.sh build
```

### Port already in use

```bash
# Find and kill process
lsof -i :8888
kill -9 <PID>
```

### Topics not publishing

```bash
# Check bridge status
docker exec -it ros2_taskboard bash -c \
  "source /opt/ros/humble/setup.bash && \
   source /root/ros2_ws/install/setup.bash && \
   ros2 topic list"
```

### Need help?

- Check **[CONTRIBUTING.md](CONTRIBUTING.md)** for development guide
- Open an issue on GitHub
- See documentation files in `docs/` folder

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|------------|
| RAM | 4 GB | 8+ GB |
| Disk | 10 GB | 20+ GB |
| Docker | 20.10+ | Latest |
| Python | 3.8+ | 3.10+ |

## Next Steps

1. **Explore the simulation:**
   ```bash
   ./docker_manager.sh sim
   ```

2. **Monitor topics:**
   ```bash
   docker exec -it ros2_taskboard bash -c \
     "source /opt/ros/humble/setup.bash && \
      source /root/ros2_ws/install/setup.bash && \
      ros2 topic echo hardware/state"
   ```

3. **Test the model:**
   ```bash
   ./docker_manager.sh test
   ```

4. **Connect to real hardware** (if available):
   ```bash
   ./docker_manager.sh hw 192.168.1.100 8888
   ```

## Contributing

Interested in contributing? See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under Apache 2.0 License - see [LICENSE](LICENSE) file.

## Citation

If you use this project in your research, please cite:

```bibtex
@software{nextforge2026,
  title={NEXT-FORGE-sim2real: MuJoCo Digital Twin with Hardware Bridge},
  author={Contributors},
  year={2026},
  url={https://github.com/USERNAME/NEXT-FORGE-sim2real}
}
```

## Support

- **Documentation**: See docs/ folder
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

---

**Ready to start? Follow Option 1 (Docker) above!** 🚀
