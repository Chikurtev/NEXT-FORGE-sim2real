# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-12

### Added

#### Phase 1: MuJoCo Physics Simulation
- New `board_mujoco_sim` ROS2 package with complete physics simulation
- `mujoco_simulator.py` - Main simulator node (500 Hz publish rate)
- `mujoco_visualizer.py` - Interactive MuJoCo viewer with native rendering
- `test_model.py` - Model validation and inspection script
- Unified `task_board.xml` MJCF model with all geometries
- Physics parameters: RK4 integrator, soft contacts, friction=0.5
- Comprehensive sensor system: framepos, framequat, framelinvel, frameangvel
- Launch files: simulator, visualizer, complete stack
- Documentation: MUJOCO_INTEGRATION_GUIDE.md, URDF_TO_MUJOCO_CONVERSION.md

#### Phase 2: Hardware Bridge
- New `board_hardware_bridge` ROS2 package for seamless hardware switching
- `hardware_bridge.py` - Dual-mode bridge (simulation/hardware)
- `sim_hardware_adapter.py` - Simulation state to hardware translation
- JSON-based configuration system (default_bridge_config.json)
- Probe detection algorithm (z-coordinate based)
- Cable connection detection (distance-based)
- Launch files for all operational modes
- Example client code (examples/example_client.py)
- Utility scripts (scripts/bridge_utils.py)
- Documentation: HARDWARE_INTEGRATION.md

#### Phase 3: Docker Containerization
- Complete Docker setup for one-command deployment
- `Dockerfile` - ROS2 Humble + MuJoCo + all packages
- `docker-compose.yml` - 3-service orchestration
  - ros2_taskboard: Main environment
  - micro_ros_agent: Hardware communication
  - rosbridge_ws: Web visualization
- Management scripts: docker_manager.sh (bash), docker_manager.bat (batch)
- Cross-platform support: Linux, macOS, Windows
- Documentation: DOCKER_GUIDE.md, QUICKSTART_DOCKER.md

#### Documentation
- MUJOCO_INTEGRATION_GUIDE.md (300+ lines)
- URDF_TO_MUJOCO_CONVERSION.md (conversion details)
- HARDWARE_INTEGRATION.md (300+ lines, complete hardware guide)
- DOCKER_GUIDE.md (500+ lines, comprehensive Docker guide)
- QUICKSTART_DOCKER.md (quick start for Docker)
- QUICKSTART_HARDWARE_BRIDGE.md (bridge quick start)
- PROJECT_STRUCTURE.md (architecture overview)
- DOCKER_INTEGRATION_SUMMARY.md (Docker summary)
- PROJECT_COMPLETION.md (project overview)
- CONTRIBUTING.md (contribution guidelines)
- .gitignore (optimized for ROS2/Docker)
- LICENSE (Apache 2.0)

#### Features
- 500 Hz physics simulation rate
- Real-time MuJoCo visualization
- Seamless simulation ↔ hardware switching
- Transparent hardware interface
- Configuration-driven architecture
- Health monitoring and status reporting
- 50 Hz hardware adapter rate
- WebSocket support for web visualization
- Cross-platform Docker support

### Changed

- Updated main README.md with Docker and bridge sections
- Enhanced quick start guide with Docker option (recommended)
- Project structure organized for production deployment

### Technical Specifications

- **MuJoCo Version**: >=2.2.0
- **ROS2 Version**: Humble (compatible with Jazzy)
- **Python**: 3.10+
- **Physics Timestep**: 0.002 seconds (500 Hz)
- **Integrator**: RK4 (4th-order Runge-Kutta)
- **Docker Image Size**: ~3.5 GB
- **Build Time (first)**: 5-10 minutes
- **Build Time (cached)**: 30 seconds

### Performance

- MuJoCo simulation: 500 Hz
- Hardware adapter: 50 Hz (configurable)
- Bridge status updates: 5 seconds
- Model validation: <10 seconds
- Container startup: 3-5 seconds

### Fixed

- Mesh path references in MJCF files
- MJCF file consolidation (multiple includes → unified model)
- Hardware interface normalization
- Docker build optimization

### Security

- Self-signed SSL certificates for rosbridge
- Privileged mode for hardware access
- Network isolation via docker-compose
- Host network mode for direct access

### Documentation

- 2000+ lines of comprehensive documentation
- Quick start guides for multiple entry points
- Architecture diagrams and explanations
- Troubleshooting guides
- Examples and use cases

---

## Future Versions

### [1.1.0] - Planned

- [ ] Multi-architecture Docker builds (ARM64, AMD64)
- [ ] CI/CD pipeline integration (GitHub Actions)
- [ ] Advanced sensor simulation (IMU, force/torque)
- [ ] Web-based control interface
- [ ] Performance optimization and benchmarking
- [ ] Kubernetes deployment manifests

### [1.2.0] - Planned

- [ ] Cloud deployment guides
- [ ] AI/ML integration for control
- [ ] Real-time rendering pipeline
- [ ] Advanced visualization options
- [ ] Extended logging and debugging

### [2.0.0] - Vision

- [ ] Multi-robot support
- [ ] Distributed simulation
- [ ] Production deployment ready
- [ ] Enterprise features (authentication, access control)

---

## Migration Guide

### From Native to Docker

If you were using the native installation:

1. Build Docker image: `./docker_manager.sh build`
2. Start containers: `./docker_manager.sh start`
3. Run simulation: `./docker_manager.sh sim`

No code changes needed - everything works the same!

### Updating from Earlier Versions

(This is version 1.0.0 - first release)

---

## Known Issues

None currently - please report issues on GitHub!

---

## Support

- Issues: GitHub Issues
- Discussions: GitHub Discussions
- Documentation: See docs/ and .md files
- Contributing: See CONTRIBUTING.md

---

## Contributors

See GitHub for contributor list.

---

## License

All changes are licensed under Apache 2.0 License.
