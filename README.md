# 🚀 Autonomous Navigation with Nav2 using Cartographer SLAM
This project implements autonomous navigation in a simulated or real-world environment using ROS 2 Nav2 and Cartographer SLAM. The system allows a robot to map an unknown environment, localize itself within the map, and navigate autonomously to predefined goals.

---

## 🛠️ Installation

### 1️⃣ **Clone the Repository**  
```bash
cd ~/ros_ws/src
git clone https://github.com/yashbhaskar/Autonomous-Navigation-with-Nav2.git
cd ~/ros_ws
```
### 2️⃣ **Build the Package** 
```bash
colcon build
source install/setup.bash
```

## 🎮 Usage

### Launch Autobringup File:
```bash
ros2 launch robot_bringup autobringup.launch.py use_sim_time:=True exploration:=True
```

## 📹 Images 

# 1. Robot Model in Rviz2
   ![model](https://github.com/user-attachments/assets/e3c2ec1a-0901-401f-aaed-df58b7f816e1)

# 2. Robot and Goal Point
   ![map](https://github.com/user-attachments/assets/31df00bf-fb12-405a-be05-bcf7117147d8)

# 3. Autonoumous Navigation
   ![navi](https://github.com/user-attachments/assets/be0e5f33-ddd9-4266-aaac-53bf13b81a18)

## 📹 Demo Video

https://github.com/user-attachments/assets/34b6ef60-da32-49e1-829a-50cfb6e9f6d8


## 📝 Project Blog

Link: ``https://yash-bhaskar-portfolio.netlify.app/robot``

## 🤝 Contributing

Feel free to fork this repository, create a pull request, or open an issue if you have suggestions or find bugs.
