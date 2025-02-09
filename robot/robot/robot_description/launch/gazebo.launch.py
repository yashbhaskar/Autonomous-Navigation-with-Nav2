import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
from launch_ros.actions import Node
import os


def generate_launch_description():
    pkg_gazebo_ros = launch_ros.substitutions.FindPackageShare(package='robot_description').find('robot_description')
    use_sim_time = LaunchConfiguration('use_sim_time')
    world_file_path=os.path.join(pkg_gazebo_ros, 'worlds/terrain.sdf')

    return launch.LaunchDescription([
        launch.actions.ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 
                                            'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so',world_file_path], 
                                           output='screen'),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                description='Flag to enable use_sim_time and use Gazebo Time'),
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-entity', 'robot', '-topic', 'robot_description'],
            parameters= [{'use_sim_time': use_sim_time}],
            output='screen'),
    ])
    
