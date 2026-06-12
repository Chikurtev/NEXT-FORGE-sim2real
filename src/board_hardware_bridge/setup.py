from setuptools import find_packages, setup

package_name = 'board_hardware_bridge'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='ROS2 Team',
    author_email='robotics@example.com',
    maintainer='ROS2 Team',
    maintainer_email='robotics@example.com',
    url='https://github.com/robotics/board_hardware_bridge',
    keywords=['ROS', 'MuJoCo', 'Hardware Bridge'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    description='Hardware bridge for task board digital twin',
    long_description='Connects MuJoCo simulation with real task board hardware via ROS2',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hardware_bridge = board_hardware_bridge.hardware_bridge:main',
            'sim_hardware_adapter = board_hardware_bridge.sim_hardware_adapter:main',
        ],
    },
)
