# Gen Finger Controller ROS1 SDK

> 用于 Gen Finger 单相机设备的 ROS1 驱动 SDK，支持相机图像、触觉传感、编码器反馈及开合距离控制。

[English](README.md)

[GitHub代码](https://github.com/genrobot-ai/gen_finger_con_ros1_sdk_release)

License: [MIT License](LICENSE.txt)

## 1 功能特性

- ROS1 Noetic 驱动（`robot_driver` 包），用于 Gen Finger 设备
- 单相机图像流（`camera_count=1`），支持实时预览
- 触觉数据发布（左 / 右）
- finger 开合距离编码器反馈
- 通过 ROS topic 控制 finger 开合
- 单指 / 双指 launch 文件
- 标定、设备 ID、编码器零点、触觉调试等工具脚本
- Demo 脚本：将模型 `PoseStamped` 指令转换为夹爪 topic

## 2 环境要求


| 项目     | 要求                       |
| ------ | ------------------------ |
| 系统     | Ubuntu 20.04（推荐）         |
| ROS    | ROS1 Noetic              |
| Python | 3.8+                     |
| USB    | USB 3.0 接口               |
| 硬件     | Gen Finger controller 设备 |




## 3 快速开始

> 首次使用请先完成 [USB 配置](docs/usb-setup_CN.md)。

```shell
git clone https://github.com/genrobot-ai/gen_finger_con_ros1_sdk_release.git
cd gen_finger_con_ros1_sdk_release
catkin_make
source devel/setup.bash
roslaunch robot_driver single_gripper_start.launch
```

验证反馈并发送控制指令：

```shell
# 终端 2 — 读取编码器反馈
rostopic echo /encoder

# 终端 3 — 设置目标开合 5 cm（范围 [0.0, 0.2] m）
rostopic pub /target_distance std_msgs/Float32 "data: 0.05"
```

启动后会弹出一个相机预览窗口。

## 4 ROS Topic 接口

通过标准 ROS 消息类型订阅传感器数据、发布控制指令。

### 4.1 单指


| Topic                     | 类型                        | 方向  | 说明                       |
| ------------------------- | ------------------------- | --- | ------------------------ |
| `/camera/color/image_raw` | `sensor_msgs/Image`       | 发布  | finger 相机图像              |
| `/encoder`                | `std_msgs/Float32`        | 发布  | finger 开合距离反馈（m）         |
| `/tactile/left`           | `std_msgs/Int8MultiArray` | 发布  | 左侧触觉传感器                  |
| `/tactile/right`          | `std_msgs/Int8MultiArray` | 发布  | 右侧触觉传感器                  |
| `/target_distance`        | `std_msgs/Float32`        | 订阅  | 目标开合距离，范围 `[0.0, 0.2]` m |


控制示例：

```shell
rostopic pub /target_distance std_msgs/Float32 "data: 0.05"
```



### 4.2 双指

所有 topic 以 `/left_gripper` 或 `/right_gripper` 为命名空间前缀。例如：


| Topic                            | 类型                 | 方向  | 说明            |
| -------------------------------- | ------------------ | --- | ------------- |
| `/left_gripper/encoder`          | `std_msgs/Float32` | 发布  | 左 finger 开合反馈 |
| `/left_gripper/target_distance`  | `std_msgs/Float32` | 订阅  | 左 finger 目标距离 |
| `/right_gripper/encoder`         | `std_msgs/Float32` | 发布  | 右 finger 开合反馈 |
| `/right_gripper/target_distance` | `std_msgs/Float32` | 订阅  | 右 finger 目标距离 |


相机与触觉 topic 遵循相同命名空间规则（如 `/left_gripper/camera/...`、`/left_gripper/tactile/...` 等）。

### 4.3 Launch 参数


| 参数                   | 默认值                        | 说明                   |
| -------------------- | -------------------------- | -------------------- |
| `serial`             | `/dev/ttyFingerLeft`       | 串口（单指 launch）        |
| `video_device`       | `/dev/finger_camera_left`  | 相机设备（单指 launch）      |
| `left_serial`        | `/dev/ttyFingerLeft`       | 左 finger 串口          |
| `right_serial`       | `/dev/ttyFingerRight`      | 右 finger 串口          |
| `left_video_device`  | `/dev/finger_camera_left`  | 左 finger 相机          |
| `right_video_device` | `/dev/finger_camera_right` | 右 finger 相机          |
| `camera_resolutions` | `1600x1296`                | 相机分辨率                |
| `show_preview`       | `true`                     | 是否显示 OpenCV 预览窗口     |
| `fps`                | `60`                       | 相机帧率（60 以获得约 30 fps） |




## 5 安装



### 5.1 安装系统与 Python 依赖

```shell
sudo apt update
sudo apt install ros-noetic-desktop-full python3-pip v4l-utils
pip3 install -r requirements.txt
```

`v4l-utils` 提供 USB 配置所需的 `v4l2-ctl` 命令。

### 5.2 拉取仓库并编译

```shell
git clone https://github.com/genrobot-ai/gen_finger_con_ros1_sdk_release.git
cd gen_finger_con_ros1_sdk_release
catkin_make
source devel/setup.bash
```

如需自动加载工作空间，在 `~/.bashrc` 中添加：

```shell
source /path/to/gen_finger_con_ros1_sdk_release/devel/setup.bash
```

编译产物：


| 产物          | 路径                          |
| ----------- | --------------------------- |
| Catkin 工作空间 | `devel/`、`build/`           |
| Launch 文件   | `src/robot_driver/launch/`  |
| 驱动脚本        | `src/robot_driver/scripts/` |




## 6 USB 配置

首次使用前需为每个 USB 口配置 udev 规则，模板见 [config/99-usb-serial.rules](./config/99-usb-serial.rules)。

每只 finger 只需 1 个串口 + 1 个相机（与三相机的 Gen Controller 夹爪不同）。

简要步骤：

1. 用 `udevadm` 和 `v4l2-ctl` 查询串口与相机的 `KERNELS` 值
2. 编辑 `config/99-usb-serial.rules`
3. 复制到 `/etc/udev/rules.d/` 并 reload

详细图文步骤见：

- [USB 配置指南 (ZH)](docs/usb-setup_CN.md)
- [USB Configuration Guide (EN)](docs/usb-setup.md)

双指配置后的默认串口软链接：`/dev/ttyFingerLeft`、`/dev/ttyFingerRight`。

默认相机软链接：`/dev/finger_camera_left`、`/dev/finger_camera_right`。

验证：

```shell
ls -l /dev/ttyFingerLeft /dev/finger_camera_left
ls -l /dev/ttyFingerRight /dev/finger_camera_right
```



## 7 使用方法



### 7.1 单指 Demo

```shell
source devel/setup.bash
roslaunch robot_driver single_gripper_start.launch
```

可选 launch 参数：

```shell
roslaunch robot_driver single_gripper_start.launch show_preview:=false
roslaunch robot_driver single_gripper_start.launch serial:=/dev/ttyFingerLeft video_device:=/dev/finger_camera_left
```

启动后弹出一个图像窗口，输出 topic：

```
/camera/color/image_raw     # 相机图像
/encoder                    # finger 开合距离反馈
/tactile/left               # 左侧触觉
/tactile/right              # 右侧触觉
/target_distance            # finger 开合距离指令
```

launch 文件默认 `<param name="fps" value="60" />`。若旧设备帧率异常，可在 launch 中将 `fps` 改为 `30`。

### 7.2 双指 Demo

```shell
source devel/setup.bash
roslaunch robot_driver dual_gripper_start.launch
```

启动后弹出两个图像预览窗口（每指一个）。

运行 demo 脚本，将模型指令桥接到夹爪 topic：

```shell
cd src/robot_driver/scripts/
python3 left_das_controller_infer.py
python3 right_das_controller_infer.py
```

- `left_das_controller_infer.py`：订阅 `/target_gripper/left_gripper`，发布 `/left_gripper/target_distance`；订阅 `/left_gripper/encoder`，发布 `/gripper/left/current_distance`
- `right_das_controller_infer.py`：订阅 `/target_gripper/right_gripper`，发布 `/right_gripper/target_distance`；订阅 `/right_gripper/encoder`，发布 `/gripper/right/current_distance`



### 7.3 设备工具命令

以下命令需先启动 `roscore`。运行期间**不要**同时启动 `roslaunch` 或其他控制节点。

**单设备：**

```shell
roscore
cd src/robot_driver/scripts/
bash camera_cmd.sh camerarc   # 相机标定（单相机）
bash camera_cmd.sh MCUID      # 设备 ID
bash camera_cmd.sh DMZEROSET  # 编码器零点设置
python3 tactile_dual_print.py # 打印触觉数据
```

**双设备（左 / 右）：**

```shell
roscore
cd src/robot_driver/scripts/

bash camera_cmd.sh left camerarc
bash camera_cmd.sh left MCUID
bash camera_cmd.sh left DMZEROSET
python3 tactile_dual_print.py _gripper_ns:=left_gripper

bash camera_cmd.sh right camerarc
bash camera_cmd.sh right MCUID
bash camera_cmd.sh right DMZEROSET
python3 tactile_dual_print.py _gripper_ns:=right_gripper
```

finger 新设备只有 1 个相机，常用标定命令为 `camerarc`。标定 YAML 文件保存至 `calib_result/`（如 `cam0_sensor.yaml`、`left_cam0_sensor.yaml`）。

通过环境变量指定串口：

```shell
SERIAL_PORT=/dev/ttyFingerLeft bash camera_cmd.sh MCUID
```



## 8 常见问题


| 问题               | 解决方法                                                      |
| ---------------- | --------------------------------------------------------- |
| 找不到串口            | 执行 `sudo apt remove brltty`，重新插拔设备                        |
| 相机或串口路径不对        | 检查 udev 规则，见 [docs/usb-setup_CN.md](docs/usb-setup_CN.md) |
| 相机帧率偏低           | 保持 launch 中 `<param name="fps" value="60" />`             |
| 无 ROS 数据         | 确认 `roscore` 已启动且 udev 规则已生效                              |
| `catkin_make` 失败 | 先 source ROS Noetic：`source /opt/ros/noetic/setup.bash`   |
| 无相机预览            | 检查 udev 相机软链接；用 `v4l2-ctl --list-devices` 验证              |
| 设备工具命令失败         | 运行工具前先停止 `roslaunch` 及其他控制节点                              |




## 9 文档索引


| 说明             | 链接                                                                                 |
| -------------- | ---------------------------------------------------------------------------------- |
| USB 配置 (ZH)    | [docs/usb-setup_CN.md](docs/usb-setup_CN.md)                                       |
| USB setup (EN) | [docs/usb-setup.md](docs/usb-setup.md)                                             |
| udev 规则模板      | [config/99-usb-serial.rules](config/99-usb-serial.rules)                           |
| 单指 launch      | [single_gripper_start.launch](src/robot_driver/launch/single_gripper_start.launch) |
| 双指 launch      | [dual_gripper_start.launch](src/robot_driver/launch/dual_gripper_start.launch)     |
| 标定辅助脚本         | [camera_cmd.sh](src/robot_driver/scripts/camera_cmd.sh)                            |
| 驱动脚本           | [src/robot_driver/scripts/](src/robot_driver/scripts/)                             |


