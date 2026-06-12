#!/usr/bin/env python3
"""
Utility Scripts for Hardware Bridge

Quick reference for common operations:
- Switch between simulation and hardware
- Monitor performance
- Test connections
"""

import argparse
import subprocess
import sys
import json
import os
from datetime import datetime


def switch_to_simulation():
    """Switch to simulation mode."""
    print("Switching to MuJoCo simulation mode...")
    
    cmd = [
        'ros2', 'launch', 'board_hardware_bridge',
        'complete_simulation_with_bridge_launch.py'
    ]
    
    print(f"Running: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    
    return True


def switch_to_hardware(address='localhost', port=8888):
    """Switch to real hardware mode."""
    print(f"Switching to hardware mode...")
    print(f"Board Address: {address}:{port}")
    
    cmd = [
        'ros2', 'launch', 'board_hardware_bridge',
        'hardware_bridge_launch.py',
        f'hardware_address:={address}',
        f'hardware_port:={port}'
    ]
    
    print(f"Running: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    
    return True


def monitor_bridge():
    """Monitor bridge operation and performance."""
    print("Monitoring hardware bridge...")
    print("(Ctrl+C to stop)\n")
    
    cmd = ['ros2', 'topic', 'hz', 'hardware/state']
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nMonitoring stopped")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False
    
    return True


def test_connection(address='localhost', port=8888):
    """Test connection to task board."""
    print(f"Testing connection to {address}:{port}...")
    
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)
    
    try:
        sock.sendto(b'ping', (address, port))
        data, addr = sock.recvfrom(1024)
        print(f"✓ Connection successful!")
        print(f"  Received from {addr}: {data}")
        return True
    except socket.timeout:
        print(f"✗ Connection timeout")
        return False
    except Exception as e:
        print(f"✗ Connection error: {e}")
        return False
    finally:
        sock.close()


def show_config(config_file=None):
    """Display current bridge configuration."""
    if not config_file:
        config_file = os.path.join(
            os.path.expanduser('~'),
            'ros_projects/ros2_ws/src/board_hardware_bridge',
            'board_hardware_bridge/config/default_bridge_config.json'
        )
    
    if not os.path.exists(config_file):
        print(f"Configuration file not found: {config_file}")
        return False
    
    print(f"Loading configuration from: {config_file}\n")
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print("=" * 60)
        print("Hardware Bridge Configuration")
        print("=" * 60)
        print(json.dumps(config, indent=2))
        print("=" * 60)
        
        return True
    except Exception as e:
        print(f"Error reading configuration: {e}")
        return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Hardware Bridge Utility Script'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Switch command
    switch_parser = subparsers.add_parser(
        'switch',
        help='Switch between simulation and hardware modes'
    )
    switch_parser.add_argument(
        'mode',
        choices=['sim', 'hw'],
        help='Mode: sim (simulation) or hw (hardware)'
    )
    switch_parser.add_argument(
        '--address',
        default='localhost',
        help='Hardware board address (for hw mode)'
    )
    switch_parser.add_argument(
        '--port',
        type=int,
        default=8888,
        help='Hardware board port (for hw mode)'
    )
    
    # Monitor command
    subparsers.add_parser('monitor', help='Monitor bridge performance')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test hardware connection')
    test_parser.add_argument(
        '--address',
        default='localhost',
        help='Hardware board address'
    )
    test_parser.add_argument(
        '--port',
        type=int,
        default=8888,
        help='Hardware board port'
    )
    
    # Config command
    config_parser = subparsers.add_parser('config', help='Show configuration')
    config_parser.add_argument(
        '--file',
        help='Configuration file path'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    if args.command == 'switch':
        if args.mode == 'sim':
            return 0 if switch_to_simulation() else 1
        else:
            return 0 if switch_to_hardware(args.address, args.port) else 1
    
    elif args.command == 'monitor':
        return 0 if monitor_bridge() else 1
    
    elif args.command == 'test':
        return 0 if test_connection(args.address, args.port) else 1
    
    elif args.command == 'config':
        return 0 if show_config(args.file) else 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
