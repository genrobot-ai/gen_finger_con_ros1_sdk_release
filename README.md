# Gen Finger Controller ROS1 SDK

> ROS1 driver for Gen Finger controller — single-camera streaming, tactile sensing, encoder feedback, and distance control.

[中文](README_CN.md)

[GitHub repository](https://github.com/genrobot-ai/gen_finger_con_ros1_sdk_release)

License: [MIT License](LICENSE.txt)

## 1 Features

- ROS1 Noetic driver (`robot_driver` package) for Gen Finger devices
- Single-camera image streaming with optional live preview (`camera_count=1`)
- Tactile sensor data publishing (left / right)
- Encoder feedback for finger opening distance
- Finger distance control via ROS topics
- Single-finger and dual-finger launch files
- Utility scripts for calibration, device ID, encoder zeroing, and tactile debugging
- Demo scripts bridging model `PoseStamped` commands to gripper topics

## 2 Requirements

| Item     | Requirement                   |
| -------- | ----------------------------- |
| OS       | Ubuntu 20.04 (recommended)    |
| ROS      | ROS1 Noetic                   |
| Python   | 3.8+                          |
| USB      | USB 3.0 port                  |
| Hardware | Gen Finger controller device  |

## 3 Quick Start

> First-time users must complete [USB configuration](docs/usb-setup.md) before launching the driver.

```shell
git clone https://github.com/genrobot-ai/gen_finger_con_ros1_sdk_release.git
cd gen_finger_con_ros1_sdk_release
catkin_make
source devel/setup.bash
roslaunch robot_driver single_gripper_start.launch
```

Verify feedback and send a control command:

```shell
# Terminal 2 — read encoder feedback
rostopic echo /encoder

# Terminal 3 — set target opening to 5 cm (range: [0.0, 0.2] m)
rostopic pub /target_distance std_msgs/Float32 "data: 0.05"
```

After startup, one camera preview window appears.

## 4 ROS Topics

Subscribe to sensor topics and publish control commands through standard ROS message types.

### 4.1 Single Finger

| Topic                     | Type                      | Direction | Description                                   |
| ------------------------- | ------------------------- | --------- | --------------------------------------------- |
| `/camera/color/image_raw` | `sensor_msgs/Image`       | publish   | Finger camera image                           |
| `/encoder`                | `std_msgs/Float32`        | publish   | Finger opening distance feedback (m)          |
| `/tactile/left`           | `std_msgs/Int8MultiArray`   | publish   | Left tactile sensor                           |
| `/tactile/right`          | `std_msgs/Int8MultiArray`   | publish   | Right tactile sensor                          |
| `/target_distance`        | `std_msgs/Float32`        | subscribe | Target opening distance, range `[0.0, 0.2]` |

Example control command:

```shell
rostopic pub /target_distance std_msgs/Float32 "data: 0.05"
```

### 4.2 Dual Finger

All topics are prefixed with `/left_gripper` or `/right_gripper`. For example:

| Topic                            | Type               | Direction | Description                    |
| -------------------------------- | ------------------ | --------- | ------------------------------ |
| `/left_gripper/encoder`          | `std_msgs/Float32` | publish   | Left finger opening feedback   |
| `/left_gripper/target_distance`  | `std_msgs/Float32` | subscribe | Left finger target distance    |
| `/right_gripper/encoder`         | `std_msgs/Float32` | publish   | Right finger opening feedback  |
| `/right_gripper/target_distance` | `std_msgs/Float32` | subscribe | Right finger target distance   |

Camera and tactile topics follow the same namespace pattern (`/left_gripper/camera/...`, `/left_gripper/tactile/...`, etc.).

### 4.3 Launch Parameters

| Parameter            | Default                    | Description                          |
| -------------------- | -------------------------- | ------------------------------------ |
| `serial`             | `/dev/ttyFingerLeft`       | Serial port (single-finger launch)   |
| `video_device`       | `/dev/finger_camera_left`  | Camera device (single-finger launch)   |
| `left_serial`        | `/dev/ttyFingerLeft`       | Left serial port (dual-finger launch)  |
| `right_serial`       | `/dev/ttyFingerRight`      | Right serial port (dual-finger launch) |
| `left_video_device`  | `/dev/finger_camera_left`  | Left camera device                   |
| `right_video_device` | `/dev/finger_camera_right` | Right camera device                  |
| `camera_resolutions` | `1600x1296`                | Camera resolution                    |
| `show_preview`       | `true`                     | Enable OpenCV preview window         |
| `fps`                | `60`                       | Camera FPS (60 required for 30 fps) |

## 5 Installation

### 5.1 Install system and Python dependencies

```shell
sudo apt update
sudo apt install ros-noetic-desktop-full python3-pip v4l-utils
pip3 install -r requirements.txt
```

`v4l-utils` provides `v4l2-ctl`, required for USB configuration.

### 5.2 Clone and build

```shell
git clone https://github.com/genrobot-ai/gen_finger_con_ros1_sdk_release.git
cd gen_finger_con_ros1_sdk_release
catkin_make
source devel/setup.bash
```

To load the workspace automatically, add to `~/.bashrc`:

```shell
source /path/to/gen_finger_con_ros1_sdk_release/devel/setup.bash
```

Build outputs:

| Artifact        | Path                                      |
| --------------- | ----------------------------------------- |
| Catkin workspace | `devel/`, `build/`                       |
| Launch files    | `src/robot_driver/launch/`              |
| Driver scripts  | `src/robot_driver/scripts/`             |

## 6 USB Configuration

Configure udev rules once per USB port before first use. The template is at [config/99-usb-serial.rules](./config/99-usb-serial.rules).

Each finger requires only one serial port and one camera rule (unlike the Gen Controller gripper with three cameras).

Summary:

1. Query serial and camera `KERNELS` values with `udevadm` and `v4l2-ctl`
2. Edit `config/99-usb-serial.rules`
3. Copy to `/etc/udev/rules.d/` and reload rules

For step-by-step instructions with screenshots, see:

- [USB 配置指南 (ZH)](docs/usb-setup_CN.md)
- [USB Configuration Guide (EN)](docs/usb-setup.md)

Default serial symlinks after dual-finger setup: `/dev/ttyFingerLeft`, `/dev/ttyFingerRight`.

Default camera symlinks: `/dev/finger_camera_left`, `/dev/finger_camera_right`.

Verify:

```shell
ls -l /dev/ttyFingerLeft /dev/finger_camera_left
ls -l /dev/ttyFingerRight /dev/finger_camera_right
```

## 7 Usage

### 7.1 Single Finger Demo

```shell
source devel/setup.bash
roslaunch robot_driver single_gripper_start.launch
```

Optional launch arguments:

```shell
roslaunch robot_driver single_gripper_start.launch show_preview:=false
roslaunch robot_driver single_gripper_start.launch serial:=/dev/ttyFingerLeft video_device:=/dev/finger_camera_left
```

After startup, one image window appears. Output topics:

```
/camera/color/image_raw     # Camera image
/encoder                    # Finger opening distance feedback
/tactile/left               # Left tactile sensor
/tactile/right              # Right tactile sensor
/target_distance            # Finger opening distance command
```

Launch files default to `<param name="fps" value="60" />`. If frame rate is abnormal on older hardware, try changing `fps` to `30` in the launch file.

### 7.2 Dual Finger Demo

```shell
source devel/setup.bash
roslaunch robot_driver dual_gripper_start.launch
```

After startup, two image preview windows appear (one per finger).

Run demo scripts to bridge model commands to gripper topics:

```shell
cd src/robot_driver/scripts/
python3 left_das_controller_infer.py
python3 right_das_controller_infer.py
```

- `left_das_controller_infer.py`: subscribes to `/target_gripper/left_gripper`, publishes `/left_gripper/target_distance`; subscribes to `/left_gripper/encoder`, publishes `/gripper/left/current_distance`
- `right_das_controller_infer.py`: subscribes to `/target_gripper/right_gripper`, publishes `/right_gripper/target_distance`; subscribes to `/right_gripper/encoder`, publishes `/gripper/right/current_distance`

### 7.3 Device Utilities

These commands require a running `roscore`. Do **not** run them while `roslaunch` or other control nodes are active.

**Single device:**

```shell
roscore
cd src/robot_driver/scripts/
bash camera_cmd.sh camerarc   # Camera calibration (single camera)
bash camera_cmd.sh MCUID      # Device ID
python3 tactile_dual_print.py # Print tactile data
```

**Dual device (left / right):**

```shell
roscore
cd src/robot_driver/scripts/

bash camera_cmd.sh left camerarc
bash camera_cmd.sh left MCUID
python3 tactile_dual_print.py _gripper_ns:=left_gripper

bash camera_cmd.sh right camerarc
bash camera_cmd.sh right MCUID
python3 tactile_dual_print.py _gripper_ns:=right_gripper
```

Finger devices use one camera, so `camerarc` is the normal calibration command. Calibration YAML files are saved to `calib_result/` (e.g. `cam0_sensor.yaml`, `left_cam0_sensor.yaml`).

Override serial port with an environment variable:

```shell
SERIAL_PORT=/dev/ttyFingerLeft bash camera_cmd.sh MCUID
```

## 8 Troubleshooting

| Problem                         | Solution                                                          |
| ------------------------------- | ----------------------------------------------------------------- |
| Serial port not found           | Run `sudo apt remove brltty`, then replug the device              |
| Camera or serial has wrong path | Re-check udev rules; see [docs/usb-setup.md](docs/usb-setup.md)   |
| Low camera frame rate           | Keep `<param name="fps" value="60" />` in the launch file         |
| No ROS data                     | Ensure `roscore` is running and udev rules are loaded             |
| `catkin_make` fails             | Source ROS Noetic: `source /opt/ros/noetic/setup.bash`            |
| No camera preview               | Check udev camera symlinks; verify with `v4l2-ctl --list-devices` |
| Device utility command fails    | Stop `roslaunch` and other control nodes before running utilities |

## 9 Documentation

| Description         | Link                                                                                     |
| ------------------- | ---------------------------------------------------------------------------------------- |
| USB 配置 (ZH)         | [docs/usb-setup_CN.md](docs/usb-setup_CN.md)                                             |
| USB setup (EN)      | [docs/usb-setup.md](docs/usb-setup.md)                                                   |
| udev rules template | [config/99-usb-serial.rules](config/99-usb-serial.rules)                                 |
| Single finger launch | [single_gripper_start.launch](src/robot_driver/launch/single_gripper_start.launch)       |
| Dual finger launch  | [dual_gripper_start.launch](src/robot_driver/launch/dual_gripper_start.launch)           |
| Calibration helper  | [camera_cmd.sh](src/robot_driver/scripts/camera_cmd.sh)                                  |
| Driver scripts      | [src/robot_driver/scripts/](src/robot_driver/scripts/)                                   |
