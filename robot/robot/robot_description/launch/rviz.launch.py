import launch
import os
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
from launch_ros.descriptions import ParameterValue

def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package='robot_description').find('robot_description')
    default_model_path = os.path.join(pkg_share, 'models/urdf/robot.xacro')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/robot.rviz')
    use_sim_time = LaunchConfiguration('use_sim_time')

    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')],
        parameters= [{'use_sim_time': use_sim_time}],

    )


    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='False',
                                    description='Flag to enable use_sim_time'),
        
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                            description='Absolute path to rviz config file'),

        
        rviz_node
    ])
    