import os
import launch
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PythonExpression,Command
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable,IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
import launch_ros
from launch_ros.descriptions import ParameterValue

def generate_launch_description():
  pkg_share = launch_ros.substitutions.FindPackageShare(package='robot_description').find('robot_description')
  navigation_dir = os.path.join(get_package_share_directory('robot_navigation'), 'launch')
  rviz_launch_dir=os.path.join(get_package_share_directory('robot_description'), 'launch')
  #gazebo_launch_dir=os.path.join(get_package_share_directory('robot_description'), 'launch')
  cartographer_launch_dir=os.path.join(get_package_share_directory('robot_slam'), 'launch')
  prefix_address = get_package_share_directory('robot_navigation') 
  default_model_path = os.path.join(pkg_share, 'models/urdf/robot.xacro')
  
  params_file_sim = os.path.join(prefix_address, 'config', 'nav2_params_simulation.yaml')
  params_file_robot = os.path.join(prefix_address, 'config', 'nav2_params_robot.yaml')
  
  map_file=LaunchConfiguration('map')
  map_directory = os.path.join(get_package_share_directory(
        'robot_bringup'), 'maps','map.yaml')
  use_sim_time=LaunchConfiguration('use_sim_time')
  exploration=LaunchConfiguration('exploration')   
  rviz_launch_cmd=IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(rviz_launch_dir, 'rviz.launch.py')),
            condition=IfCondition(use_sim_time),
            launch_arguments={'use_sim_time':use_sim_time}.items())

  state_publisher_launch_cmd=IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(rviz_launch_dir, 'state_publisher.launch.py')),
            launch_arguments={'use_sim_time':use_sim_time}.items())

  #gazebo_launch_cmd=IncludeLaunchDescription(
  #      PythonLaunchDescriptionSource(
  #          os.path.join(gazebo_launch_dir, 'gazebo.launch.py')),
  #          condition=IfCondition(use_sim_time),
  #          launch_arguments={'use_sim_time':use_sim_time}.items())

  navigation_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(navigation_dir, 'navigation.launch.py')),
        launch_arguments={'params_file': params_file_robot}.items())
  
  cartographer_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(cartographer_launch_dir, 'cartographer.launch.py')),
        launch_arguments={'params_file': params_file_robot,
                          'exploration': exploration,
                          'use_sim_time': use_sim_time}.items())  



  robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time': use_sim_time},{'robot_description': ParameterValue(Command(['xacro ', LaunchConfiguration('model')]),value_type=str)}]
    )

  joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters= [{'use_sim_time': use_sim_time}],
    )
  return LaunchDescription([

    SetEnvironmentVariable('RCUTILS_LOGGING_BUFFERED_STREAM', '1'),
    launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='False',
                                            description='Flag to enable use_sim_time'),
    launch.actions.DeclareLaunchArgument(name='exploration', default_value='True',
                                            description='Flag to enable use_sim_time'),
    launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                          description='Absolute path to robot urdf file'),
    launch.actions.DeclareLaunchArgument(name='map',default_value=map_directory,
                                          description='Map to be used'),
 Node(
        package='nav2_map_server',
        condition=IfCondition(PythonExpression(['not ', exploration])),
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time},
                    {'yaml_filename': map_file}
                    ]),
    Node(
        package='nav2_lifecycle_manager',
        condition=IfCondition(PythonExpression(['not ', exploration])),
        executable='lifecycle_manager',
        name='lifecycle_manager_mapper',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time},
                    {'autostart': True},
                    {'node_names': ['map_server']}]),

    rviz_launch_cmd,
    state_publisher_launch_cmd,
    robot_state_publisher_node,
    joint_state_publisher_node,
    navigation_launch_cmd, 
    cartographer_launch_cmd

  ]
)

