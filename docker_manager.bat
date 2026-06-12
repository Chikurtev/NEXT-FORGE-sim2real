@echo off
REM Windows batch script for Docker management

setlocal enabledelayedexpansion

REM Colors (requires Windows 10+)
set "BLUE=[0;34m"
set "GREEN=[0;32m"
set "RED=[0;31m"
set "YELLOW=[1;33m"
set "NC=[0m"

REM Get script directory
for /f "delims=" %%A in ('cd /d "%~dp0" ^& cd') do set "SCRIPT_DIR=%%A"

REM Check if Docker is installed
where docker >nul 2>nul
if errorlevel 1 (
    echo Docker is not installed or not in PATH
    echo Install Docker Desktop from: https://www.docker.com/products/docker-desktop
    exit /b 1
)

REM Parse command
set "command=%1"
if "%command%"=="" set "command=help"

if "%command%"=="build" goto build
if "%command%"=="start" goto start
if "%command%"=="stop" goto stop
if "%command%"=="sim" goto sim
if "%command%"=="hw" goto hw
if "%command%"=="shell" goto shell
if "%command%"=="test" goto test
if "%command%"=="topics" goto topics
if "%command%"=="logs" goto logs
if "%command%"=="help" goto help

echo Unknown command: %command%
goto help

:build
echo Building Docker Image...
cd /d "%SCRIPT_DIR%"
docker build -t ros2_taskboard:latest -f Dockerfile .
echo Build complete!
goto end

:start
echo Starting Containers...
cd /d "%SCRIPT_DIR%"
docker-compose up -d
timeout /t 2
echo Containers started!
docker ps | findstr ros2_taskboard
goto end

:stop
echo Stopping Containers...
cd /d "%SCRIPT_DIR%"
docker-compose down
echo Containers stopped!
goto end

:sim
echo Running MuJoCo Simulation...
docker exec -it ros2_taskboard bash -c "source /opt/ros/humble/setup.bash && source /root/ros2_ws/install/setup.bash && ros2 launch board_hardware_bridge complete_simulation_with_bridge_launch.py"
goto end

:hw
set "address=%2"
set "port=%3"
if "%address%"=="" set "address=localhost"
if "%port%"=="" set "port=8888"
echo Running Hardware Mode - Board: %address%:%port%
docker exec -it ros2_taskboard bash -c "source /opt/ros/humble/setup.bash && source /root/ros2_ws/install/setup.bash && ros2 launch board_hardware_bridge hardware_bridge_launch.py hardware_address:=%address% hardware_port:=%port%"
goto end

:shell
echo Opening Interactive Shell...
docker exec -it ros2_taskboard bash -c "source /opt/ros/humble/setup.bash && source /root/ros2_ws/install/setup.bash && bash"
goto end

:test
echo Testing MuJoCo Model...
docker exec -it ros2_taskboard bash -c "source /opt/ros/humble/setup.bash && source /root/ros2_ws/install/setup.bash && python3 src/board_mujoco_sim/board_mujoco_sim/test_model.py"
goto end

:topics
echo Listing ROS2 Topics...
docker exec -it ros2_taskboard bash -c "source /opt/ros/humble/setup.bash && source /root/ros2_ws/install/setup.bash && ros2 topic list"
goto end

:logs
docker-compose logs -f
goto end

:help
echo.
echo ROS2 Task Board Docker Manager
echo.
echo Usage: docker_manager.bat [command] [options]
echo.
echo Commands:
echo   build          Build Docker image
echo   start          Start containers
echo   stop           Stop containers
echo   sim            Run MuJoCo simulation with bridge
echo   hw             Run hardware mode
echo   shell          Open interactive bash shell
echo   test           Test MuJoCo model
echo   topics         List ROS2 topics
echo   logs           Show container logs
echo   help           Show this help message
echo.
echo Examples:
echo   docker_manager.bat build
echo   docker_manager.bat start
echo   docker_manager.bat sim
echo   docker_manager.bat hw 192.168.1.100 8888
echo   docker_manager.bat shell
echo.
goto end

:end
endlocal
