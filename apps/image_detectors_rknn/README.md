# RKNN Object Detectors for Rockchip NPU (RK3566 / RK3588)

Universal, production-ready edge AI object detection suite optimized for Rockchip NPUs via **`rknn-toolkit-lite2`**.

This repository provides a single, unified Python inference engine (`detect.py`) capable of running multiple state-of-the-art detector families (**PP-PicoDet**, **Ultralytics YOLOv8 & YOLO11**, and **Deci AI YOLO-NAS**) directly on the Rockchip Neural Processing Unit (NPU) with zero code modifications.

---

## Features

- **Multi-Architecture Support:** Seamlessly executes models from three distinct architectures:
  - **Baidu PP-PicoDet:** Anchor-free ultra-lightweight detector (`picodet_s_320`, `picodet_s_416`).
  - **Ultralytics YOLO:** SOTA real-time detectors (`yolov8n`, `yolo11n_320`, `yolo11n_640`).
  - **Deci AI YOLO-NAS:** Neural Architecture Search-optimized model (`yolo-nas_s`).
- **Dynamic Tensor Resolution Scaling:** Dynamically queries input tensor dimensions directly from the NPU runtime (e.g., 320x320, 416x416, 640x640) and applies proportional unscaling to raw input frames.
- **Production-Ready Visual Output:** Generates annotated frames with distinct category-colored bounding boxes, class confidence tags, and a telemetry HUD displaying inference latency and real-time FPS.
- **Automated Benchmarking Mode:** Built-in `--benchmark` command to profile pure NPU latency and full end-to-end pipeline execution across test sets.
- **Surveillance Pipeline Drop-In:** Emits standard detection strings to `stdout` (`<class> @ (x1 y1 x2 y2) <conf>`), making it a drop-in replacement for edge camera surveillance scripts and alert dispatchers.

---

## Hardware & OS Compatibility

| Component | Tested Platform | Also Compatible With |
|---|---|---|
| **SoC** | Rockchip **RK3566** (Quad-Core Cortex-A55 @ 1.8 GHz, 0.8 TOPS NPU) | Rockchip **RK3588** / **RK3588S** (6.0 TOPS), **RK3568**, **RK3562**, **RV1106** / **RV1103** |
| **SBCs** | Radxa Zero 3W / 3E (4 GB LPDDR4) | Orange Pi 3B, Orange Pi 5 / 5 Plus, Radxa ROCK 5B / 5A, Quartz64 |
| **Operating System** | Debian 12 (Bookworm) 64-bit / Linux Kernel 5.10.160-rockchip | Ubuntu 22.04 / 24.04 LTS (ARM64), Armbian, DietPi |
| **NPU Driver / Runtime** | `librknnrt.so` v2.3.2 (Driver v0.9.8) | `librknnrt` >= 2.0.0 |
| **Python** | Python 3.10, 3.11, 3.12 | Python >= 3.8 |

---

## Python Environment Setup

### 1. System Libraries
Ensure the Rockchip NPU runtime library (`librknnrt.so`) is installed on your single-board computer:
```bash
# Verify NPU device node and runtime library
ls -l /dev/rknpu*
ldconfig -p | grep rknn
```

If missing, install `librknnrt.so` from the official [Rockchip RKNN Runtime GitHub repository](https://github.com/airockchip/rknn-toolkit2/tree/master/rknpu2/runtime/Linux/librknn_api/aarch64) to `/usr/lib/`.

### 2. Python Dependencies
Clone this repository and install the required dependencies:
```bash
cd ~/image_detectors_rknn
pip3 install -r requirements.txt
```

#### `requirements.txt`:
```text
numpy>=1.20.0,<2.0.0
opencv-python-headless>=4.5.0
rknn-toolkit-lite2>=2.3.0
```

> **Installation Note for `rknn-toolkit-lite2`:**  
> If `pip3 install rknn-toolkit-lite2` is not available directly on your index, download the appropriate `.whl` for your Python version (e.g. Python 3.10, 3.11, or 3.12) from the official [Rockchip RKNN Toolkit2 Releases](https://github.com/airockchip/rknn-toolkit2/tree/master/rknn-toolkit-lite2/packages):
> ```bash
> # Example for Python 3.11/3.12 ARM64:
> pip3 install rknn_toolkit_lite2-2.3.2-cp311-cp311-linux_aarch64.whl
> ```

---

## Models Included

All pre-compiled `.rknn` models are stored in the `models/` directory:

| Filename | Architecture | Input Resolution | Precision | File Size | Output Heads |
|---|---|:---:|:---:|:---:|---|
| [`yolo11n_320_rk3566.rknn`](models/yolo11n_320_rk3566.rknn) | Ultralytics YOLO11n | 320x320 | FP16 | 6.3 MB | 1 head: `(1, 84, 2100)` |
| [`default-yolov8n-rk3566.rknn`](models/default-yolov8n-rk3566.rknn) | Ultralytics YOLOv8n | 320x320 | FP16 | 7.0 MB | 1 head: `(1, 84, 2100)` |
| [`picodet_s_320_rk3566.rknn`](models/picodet_s_320_rk3566.rknn) | Baidu PP-PicoDet-S | 320x320 | FP16 | 5.1 MB | 2 heads: `(1, 2125, 4)`, `(1, 80, 2125)` |
| [`deci-fp16-yolonas_s-rk3566-v2.3.2-2.rknn`](models/deci-fp16-yolonas_s-rk3566-v2.3.2-2.rknn) | Deci AI YOLO-NAS-S | 320x320 | FP16 | 23.8 MB | 2 heads: `(1, 2100, 4)`, `(1, 2100, 80)` |
| [`picodet_s_416_rk3566.rknn`](models/picodet_s_416_rk3566.rknn) | Baidu PP-PicoDet-S | 416x416 | FP16 | 4.5 MB | 2 heads: `(1, 3598, 4)`, `(1, 80, 3598)` |
| [`yolo11n_rk3566.rknn`](models/yolo11n_rk3566.rknn) | Ultralytics YOLO11n | 640x640 | FP16 | 6.7 MB | 1 head: `(1, 84, 8400)` |

---

## Usage

### Positional CLI Syntax
```bash
python3 detect.py <input_img> <output_img> [conf_thresh] [model_path]
```

- `<input_img>`: Path to input image file (JPG, PNG, WebP).
- `<output_img>`: Path where annotated image with visual bounding boxes will be saved.
- `[conf_thresh]`: *(Optional)* Detection confidence threshold (default: `0.25`).
- `[model_path]`: *(Optional)* Path to `.rknn` model file (default: `models/picodet_s_416_rk3566.rknn`).

### Examples

#### 1. Ultra-High Accuracy Human Surveillance with PicoDet-S (416x416)
```bash
python3 detect.py sample_img/3.jpg output.jpg 0.25 models/picodet_s_416_rk3566.rknn
```
**Stdout Output:**
```text
person @ (245 522 375 651) 0.676270
person @ (246 287 374 411) 0.654297
person @ (675 525 804 650) 0.652344
person @ (245 43 373 173) 0.632812
person @ (897 259 1016 421) 0.627441
backpack @ (1122 409 1205 481) 0.427246
...
```

#### 2. Ultra-Fast Edge Inference with YOLO11n (320x320, ~17.4 FPS)
```bash
python3 detect.py sample_img/2.jpg output_elephants.jpg 0.25 models/yolo11n_320_rk3566.rknn
```

#### 3. High-Resolution Detection with YOLO11n (640x640)
```bash
python3 detect.py sample_img/1.jpg output_birds.jpg 0.30 models/yolo11n_rk3566.rknn
```

#### 4. Deci AI YOLO-NAS-S Inference
```bash
python3 detect.py sample_img/4.jpg output_traffic.jpg 0.25 models/deci-fp16-yolonas_s-rk3566-v2.3.2-2.rknn
```

---

## Automated Benchmark Suite

Run the full empirical benchmark matrix across all 6 models and 6 sample images:
```bash
python3 detect.py --benchmark
```

---

## Empirical Benchmarks

*Hardware Platform: Radxa Zero 3W (Rockchip RK3566 NPU @ 0.8 TOPS, 4 GB LPDDR4, `librknnrt` 2.3.2)*

### Phase 1: Pure NPU Inference Latency (20 Warm Iterations)

| Model Architecture | Target Resolution | Model Size | NPU Latency | Pure NPU Throughput | Relative Speed |
|---|:---:|:---:|:---:|:---:|:---:|
| **YOLO11n** | 320x320 | 6.3 MB | **57.4 ms** | **17.4 FPS** | **1.00x (Fastest)** |
| **YOLOv8n** | 320x320 | 7.0 MB | **71.7 ms** | **13.9 FPS** | 1.25x |
| **PP-PicoDet-S** | 320x320 | 5.1 MB | **73.5 ms** | **13.6 FPS** | 1.28x |
| **YOLO-NAS-S** | 320x320 | 23.8 MB | **96.6 ms** | **10.4 FPS** | 1.68x |
| **PP-PicoDet-S** | 416x416 | 4.5 MB | **122.8 ms** | **8.1 FPS** | 2.14x |
| **YOLO11n** | 640x640 | 6.7 MB | **218.1 ms** | **4.6 FPS** | 3.80x |

---

### Phase 2: Full End-to-End Pipeline Performance across Sample Images (conf = 0.25)
*(Includes OpenCV image decode, bilinear resize, NPU inference, tensor parsing, NMS, and visual HUD rendering)*

| Model | `1.jpg` (Birds & Jet) `960x540` | `2.jpg` (Elephants & Truck) `2560x1707` | `3.jpg` (Crowd Scene) `1280x720` | `4.jpg` (Street & Bike) `1280x720` | `5.jpg` (Indoor People) `626x417` | `6.jpg` (Landscape) `1920x1080` |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **YOLO11n (320x320)** | 0 obj (77.8 ms) | 9 obj (96.3 ms) | 0 obj (73.2 ms) | 0 obj (80.6 ms) | 1 obj (82.5 ms) | 0 obj (97.2 ms) |
| **YOLOv8n (320x320)** | 0 obj (89.1 ms) | 9 obj (110.9 ms) | 6 obj (91.2 ms) | 0 obj (89.7 ms) | 1 obj (88.5 ms) | 0 obj (89.0 ms) |
| **PP-PicoDet-S (320x320)** | 22 obj (99.7 ms) | 17 obj (115.8 ms) | **30 obj** (146.9 ms) | **15 obj** (96.6 ms) | **8 obj** (115.6 ms) | 1 obj (108.6 ms) |
| **YOLO-NAS-S (320x320)** | 1 obj (117.7 ms) | **20 obj** (141.4 ms) | 23 obj (144.2 ms) | 6 obj (115.4 ms) | 6 obj (115.7 ms) | **2 obj** (120.7 ms) |
| **PP-PicoDet-S (416x416)** | 34 obj (161.2 ms) | 18 obj (226.0 ms) | 28 obj (190.8 ms) | 6 obj (165.7 ms) | 7 obj (163.8 ms) | 0 obj (152.1 ms) |
| **YOLO11n (640x640)** | **50 obj** (328.1 ms) | 18 obj (306.5 ms) | 18 obj (295.6 ms) | 2 obj (285.5 ms) | 3 obj (291.6 ms) | 0 obj (318.3 ms) |

---

## Architectural Analysis & Model Recommendations

1. **For Maximum Real-Time Throughput:**
   - **YOLO11n (320x320)** achieves **57.4 ms NPU latency (~17.4 FPS)**. Ideal for motion detection trigger systems or high-framerate stream tracking where fast inference latency is paramount.

2. **For Surveillance & Small Object Sensitivity:**
   - **PP-PicoDet-S (416x416)** is the superior choice for security cameras and indoor surveillance. It yields the highest human confidence margins (60%–75% vs 30%–50% on YOLO) and detects small, distant individuals and backpacks reliably while still maintaining **8.1 FPS** on the RK3566 NPU.

3. **For High-Resolution Panoramic Scenes:**
   - **YOLO11n (640x640)** delivers unmatched detection density (e.g. 50 individual birds in `1.jpg` and 94% confidence on elephants in `2.jpg`). At **218 ms (~4.6 FPS)**, it is ideally suited for 1080p/4K stationary camera surveillance with low frame rate (1–3 FPS).

4. **For Balanced Multi-Class Detection:**
   - **Deci AI YOLO-NAS-S** delivers stable multi-class bounding boxes with high fidelity across diverse object categories at **10.4 FPS**.

---

## Sample Images Reference

The `sample_img/` directory includes 6 varied real-world test scenes:
- `1.jpg` (`960x540`): Sky landscape with flying birds and distant jet.
- `2.jpg` (`2560x1707`): High-resolution wildlife safari scene with elephants and safari trucks.
- `3.jpg` (`1280x720`): High-density pedestrian crowd and surveillance camera angle.
- `4.jpg` (`1280x720`): Urban traffic environment with bicycles and traffic lights.
- `5.jpg` (`626x417`): Indoor indoor meeting / office crowd scene.
- `6.jpg` (`1920x1080`): Wide landscape highway scene.

---

## License

This project is licensed under the Apache 2.0 License.
Pretrained model weights belong to their respective original authors (Ultralytics, Baidu PaddlePaddle, Deci AI).
