import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist # ロボットの速度命令
from sensor_msgs.msg import LaserScan # LiDARデータ用
import numpy as np

class RobotControllerNode(Node):
    def __init__(self):
        super().__init__('robot_controller_node')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.laser_callback,
            10
        )
        self.get_logger().info('Robot Controller Node has been started.')

    def laser_callback(self, msg):

        min_distance = np.inf
        front_ranges = np.array(msg.ranges[0:30] + msg.ranges[-30:]) # 前方60度の範囲

        min_distance = np.min(front_ranges[np.isfinite(front_ranges)]) # 無限大を除外

        twist = Twist()
        
        MAX_LINEAR_SPEED = 0.5
        MAX_ANGULAR_SPEED = 1.0
        
        if min_distance < 0.5: # 0.5m以内に障害物がある場合
            self.get_logger().info(f'Obstacle detected! Min distance: {min_distance:.2f} m. Turning...')
            twist.linear.x = 0.0 # 停止
            twist.angular.z = MAX_ANGULAR_SPEED # 右旋回 
        elif min_distance < 1.0: # 少し近づいたら減速
            twist.linear.x = MAX_LINEAR_SPEED # 前進
            twist.angular.z = 0.0
        else: # 障害物がない場合、直進
            twist.linear.x = MAX_LINEAR_SPEED # 前進
            twist.angular.z = 0.0

        self.publisher_.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = RobotControllerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
