import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.qos import qos_profile_sensor_data
import math
from transforms3d.euler import quat2euler
from star import convert_path_to_world_coords_in_expanded_maze


class PathFollower(Node):

    def __init__(self, path):
        super().__init__('path_follower')

        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            qos_profile_sensor_data
        )

        self.path = path
        self.current_pose = None
        self.current_index = 0

        self.timer = self.create_timer(
            0.05,
            self.follow_path
        )

        self.DIST_TOLERANCE = 0.20
        self.ANGLE_TOLERANCE = 0.02

        self.MAX_LINEAR = 0.20
        self.MAX_ANGULAR = 0.50

        self.KP_LINEAR = 0.30
        self.KP_ANGULAR = 1.20

        self.state = 'ROTATE'

    def odom_callback(self, msg):

        self.current_pose = (
            msg.pose.pose.position.x,
            msg.pose.pose.position.y,
            self.get_yaw_from_quaternion(
                msg.pose.pose.orientation
            )
        )

    def get_yaw_from_quaternion(self, orientation):

        q = orientation

        return quat2euler(
            [q.w, q.x, q.y, q.z]
        )[2]

    def normalize_angle(self, angle):

        return math.atan2(
            math.sin(angle),
            math.cos(angle)
        )

    def follow_path(self):

        if self.current_pose is None:
            return

        if self.current_index >= len(self.path):

            self.publisher.publish(Twist())
            return

        goal_x, goal_y = self.path[self.current_index]

        x, y, yaw = self.current_pose

        dx = goal_x - x
        dy = goal_y - y

        distance = math.sqrt(dx**2 + dy**2)

        target_yaw = math.atan2(dy, dx)

        yaw_error = self.normalize_angle(
            target_yaw - yaw
        )

        twist = Twist()

        if self.state == 'ROTATE':

            if abs(yaw_error) > self.ANGLE_TOLERANCE:

                twist.angular.z = max(
                    -self.MAX_ANGULAR,
                    min(
                        self.MAX_ANGULAR,
                        self.KP_ANGULAR * yaw_error
                    )
                )

            else:

                self.state = 'MOVE'

        elif self.state == 'MOVE':

            if distance > self.DIST_TOLERANCE:

                speed = max(
                    0.05,
                    min(
                        self.MAX_LINEAR,
                        self.KP_LINEAR * distance
                    )
                )

                if abs(yaw_error) > 0.10:

                    twist.linear.x = speed * 0.5

                    twist.angular.z = max(
                        -self.MAX_ANGULAR,
                        min(
                            self.MAX_ANGULAR,
                            self.KP_ANGULAR * yaw_error
                        )
                    )

                else:

                    twist.linear.x = speed

                    twist.angular.z = max(
                        -self.MAX_ANGULAR * 0.3,
                        min(
                            self.MAX_ANGULAR * 0.3,
                            self.KP_ANGULAR * yaw_error
                        )
                    )

            else:

                self.current_index += 1
                self.state = 'ROTATE'

        self.publisher.publish(twist)


def main(args=None):

    rclpy.init(args=args)

    caminho = convert_path_to_world_coords_in_expanded_maze()

    path_follower = PathFollower(caminho)

    rclpy.spin(path_follower)

    path_follower.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
