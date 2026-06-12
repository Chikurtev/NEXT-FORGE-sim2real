#!/bin/bash

# Docker Build and Run Script for ROS2 Task Board

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        echo "Install Docker from: https://docs.docker.com/get-docker/"
        exit 1
    fi
    print_success "Docker found"
}

# Build Docker image
build_image() {
    print_header "Building Docker Image"
    
    cd "$SCRIPT_DIR"
    docker build -t ros2_taskboard:latest -f Dockerfile .
    
    print_success "Docker image built successfully"
}

# Start containers
start_containers() {
    print_header "Starting Containers"
    
    cd "$SCRIPT_DIR"
    
    # Check if containers already running
    if docker ps | grep -q ros2_taskboard; then
        print_warning "ros2_taskboard container already running"
        return
    fi
    
    docker-compose up -d
    
    sleep 2
    print_success "Containers started"
    
    docker ps | grep -E "(ros2_taskboard|micro_ros_agent|rosbridge_ws)" || true
}

# Stop containers
stop_containers() {
    print_header "Stopping Containers"
    
    cd "$SCRIPT_DIR"
    docker-compose down
    
    print_success "Containers stopped"
}

# Run simulation
run_simulation() {
    print_header "Running MuJoCo Simulation with Hardware Bridge"
    
    docker exec -it ros2_taskboard bash -c \
        "source /opt/ros/humble/setup.bash && \
         source /root/ros2_ws/install/setup.bash && \
         ros2 launch board_hardware_bridge complete_simulation_with_bridge_launch.py"
}

# Run hardware mode
run_hardware() {
    local address=${1:-"localhost"}
    local port=${2:-"8888"}
    
    print_header "Running in Hardware Mode"
    print_warning "Board Address: $address:$port"
    
    docker exec -it ros2_taskboard bash -c \
        "source /opt/ros/humble/setup.bash && \
         source /root/ros2_ws/install/setup.bash && \
         ros2 launch board_hardware_bridge hardware_bridge_launch.py \
             hardware_address:=$address \
             hardware_port:=$port"
}

# Open interactive shell
shell() {
    print_header "Opening Interactive Shell"
    
    docker exec -it ros2_taskboard bash -c \
        "source /opt/ros/humble/setup.bash && \
         source /root/ros2_ws/install/setup.bash && \
         bash"
}

# Show logs
show_logs() {
    docker-compose logs -f "$@"
}

# Test model
test_model() {
    print_header "Testing MuJoCo Model"
    
    docker exec -it ros2_taskboard bash -c \
        "source /opt/ros/humble/setup.bash && \
         source /root/ros2_ws/install/setup.bash && \
         python3 src/board_mujoco_sim/board_mujoco_sim/test_model.py"
}

# Monitor topics
monitor_topics() {
    docker exec -it ros2_taskboard bash -c \
        "source /opt/ros/humble/setup.bash && \
         source /root/ros2_ws/install/setup.bash && \
         ros2 topic list"
}

# Show help
show_help() {
    cat << EOF
${BLUE}ROS2 Task Board Docker Manager${NC}

Usage: $0 <command> [options]

Commands:
  ${GREEN}build${NC}          Build Docker image
  ${GREEN}start${NC}          Start containers (docker-compose up)
  ${GREEN}stop${NC}           Stop containers (docker-compose down)
  ${GREEN}sim${NC}            Run MuJoCo simulation with bridge
  ${GREEN}hw${NC}             Run hardware mode (requires address/port)
  ${GREEN}shell${NC}          Open interactive bash shell
  ${GREEN}test${NC}           Test MuJoCo model
  ${GREEN}topics${NC}         List ROS2 topics
  ${GREEN}logs${NC}           Show container logs
  ${GREEN}help${NC}           Show this help message

Examples:
  # Build and start
  $0 build
  $0 start
  
  # Run simulation
  $0 sim
  
  # Run hardware mode
  $0 hw 192.168.1.100 8888
  
  # Open shell
  $0 shell
  
  # Check topics
  $0 topics

Quick Start:
  1. $0 build              # Build image (one time)
  2. $0 start              # Start containers
  3. $0 sim                # Run simulation in new terminal
  4. $0 shell              # Open another shell for monitoring

${YELLOW}Note:${NC} For visualization (MuJoCo viewer), run with X11 forwarding enabled.

EOF
}

# Main logic
main() {
    local command=${1:-help}
    
    case "$command" in
        build)
            check_docker
            build_image
            ;;
        start)
            check_docker
            start_containers
            ;;
        stop)
            check_docker
            stop_containers
            ;;
        sim)
            check_docker
            run_simulation
            ;;
        hw)
            check_docker
            run_hardware "$2" "$3"
            ;;
        shell)
            check_docker
            shell
            ;;
        test)
            check_docker
            test_model
            ;;
        topics)
            check_docker
            monitor_topics
            ;;
        logs)
            check_docker
            show_logs "$@"
            ;;
        help)
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
