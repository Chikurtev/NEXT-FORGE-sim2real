# Hardware Bridge Documentation

Hardware bridge package for the task board digital twin. Provides seamless switching
between MuJoCo simulation and real hardware.

## Features

- **Dual Mode Operation**: Simulation or real hardware
- **Transparent Interface**: Single interface for both modes
- **State Bridging**: Translates simulation state to hardware sensors
- **Configuration Driven**: JSON-based configuration

## Quick Start

### Simulation Mode
```bash
ros2 launch board_hardware_bridge complete_simulation_with_bridge_launch.py
```

### Hardware Mode
```bash
ros2 launch board_hardware_bridge hardware_bridge_launch.py \
    hardware_address:=192.168.1.100 \
    hardware_port:=8888
```

## Configuration

See `board_hardware_bridge/config/default_bridge_config.json` for configuration options.
