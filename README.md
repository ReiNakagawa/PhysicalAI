# PhysicalAI

このプロジェクトはROS2,Gazeboを用いてTurtleBot3を自動制御するプロジェクトです。

## 特徴

- TurtleBot3に搭載された360°LiDAR(レーザースキャン)センサで障害物を検知し、ルールに基づいて障害物を自動で回避できる

## ディレクトリ構成
PhysicalAI/
├── pai_ws.zip #ワークスペース
├── robot_controller_node.py #LiDARデータ、障害物回避(pai_ws/src/my_robot_control/my_robot_control)
├── setup.py #robot_controller_node.py実行用(pai_ws/src/my_robot_control)
└── README.md
