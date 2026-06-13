# Use ROS 2 Humble base image
FROM ros:humble-ros-core-jammy

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    ROS_DISTRO=humble \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8

# Update and install system dependencies
RUN apt-get update && apt-get install -y software-properties-common && \
    add-apt-repository universe && \
    apt-get update && apt-get install -y \
    # Build tools
    build-essential \
    git \
    curl \
    wget \
    cmake \
    python3-pip \
    python3-dev \
    python3-venv \
    # ROS 2 tools
    ros-humble-desktop \
    ros-humble-launch \
    ros-humble-urdf-launch \
    ros-humble-xacro \
    python3-colcon-common-extensions \
    ros-dev-tools \
    # Webots and dependencies
    ros-humble-webots-ros2 \
    # rosbridge for WebSocket
    ros-humble-rosbridge-suite \
    # Additional utilities
    nano \
    vim \
    htop \
    tmux \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# Install MuJoCo
RUN pip3 install --no-cache-dir mujoco>=2.2.0

# Fallback: ensure colcon extensions available via pip if apt package not found
RUN pip3 install --no-cache-dir -U colcon-common-extensions || true

# Install Python dependencies for the project
RUN pip3 install --no-cache-dir \
    numpy \
    scipy \
    matplotlib \
    pytest \
    flake8 \
    pydocstyle

# Create workspace
WORKDIR /root/ros2_ws

# Copy the entire workspace (including src, scripts, etc.)
COPY . .

# Build the ROS2 packages
RUN . /opt/ros/humble/setup.sh && \
    colcon build --packages-skip board_webots_sim

# Create a startup script
RUN echo '#!/bin/bash\n\
. /opt/ros/humble/setup.bash\n\
. /root/ros2_ws/install/setup.bash\n\
exec "$@"' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Default command
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
