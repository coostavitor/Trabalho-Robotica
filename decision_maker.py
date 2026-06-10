#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np

class DecisionMaker(Node):
    def __init__(self):
        super().__init__('decision_maker')
        self.subscription = self.create_subscription(
            Image,
            '/camera/edges',
            self.decision_callback,
            10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.bridge = CvBridge()
        self.get_logger().info(" DecisionMaker SIMPLES iniciado")

    def decision_callback(self, msg):
        try:
            edges = self.bridge.imgmsg_to_cv2(msg, 'mono8')
            
            # Calcula quantos pixels brancos tem na imagem
            white_pixels = np.sum(edges > 0)
            total_pixels = edges.shape[0] * edges.shape[1]
            density = white_pixels / total_pixels
            
            print(f" Densidade total de bordas: {density:.4f}")
            
            twist = Twist()
            
            # Se tiver MUITAS bordas (mais que 1%), desvia
            if density > 0.003:
                print(" MUITAS BORDAS! Desviando...")
                twist.angular.z = 0.8
                twist.linear.x = 0.1
            else:
                print("Seguindo reto")
                twist.linear.x = 0.3
                twist.angular.z = 0.0
            
            self.cmd_pub.publish(twist)
            
        except Exception as e:
            print(f"Erro: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = DecisionMaker()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
