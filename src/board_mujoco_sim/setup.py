from setuptools import find_packages, setup

package_name = 'board_mujoco_sim'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'mujoco>=2.2.0'],
    zip_safe=True,
    author='ROS2 Team',
    author_email='robotics@example.com',
    maintainer='ROS2 Team',
    maintainer_email='robotics@example.com',
    url='https://github.com/robotics/board_mujoco_sim',
    download_url='https://github.com/robotics/board_mujoco_sim/releases',
    keywords=['ROS', 'MuJoCo', 'simulation'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description='MuJoCo simulation for task board digital twin',
    long_description='Integration of MuJoCo physics simulation with ROS2 for the task board project',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'mujoco_simulator = board_mujoco_sim.mujoco_simulator:main',
            'mujoco_visualizer = board_mujoco_sim.mujoco_visualizer:main',
        ],
    },
)
