# Copyright (c) 2020 OUXT Polaris
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from ament_index_python.packages import get_package_share_directory
import launch
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import xacro

from pathlib import Path

share_dir_path = os.path.join(get_package_share_directory('miniv_description'))
xacro_path = os.path.join(share_dir_path, 'urdf', 'miniv.urdf.xacro')


def generate_launch_description():
    doc = xacro.process_file(xacro_path)
    robot_description = {"robot_description": doc.toxml()}
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[robot_description])
    with_rviz = LaunchConfiguration('with_rviz', default=False)
    with_rviz_arg = DeclareLaunchArgument(
                'with_rviz', default_value=with_rviz,
                description="if true, launch Autoware with given rviz configuration.")
    rviz = Node(
                package='rviz2',
                executable='rviz2',
                name='rviz2',
                output={
                    'stderr': 'log',
                    'stdout': 'log',
                    },
                condition=IfCondition(with_rviz),
                arguments=[
                    '-d', str(
                        Path(get_package_share_directory('miniv_description')) /
                        'miniv.rviz')])

    return launch.LaunchDescription(
        [
            robot_state_publisher,
            with_rviz_arg,
            rviz
        ]
    )
