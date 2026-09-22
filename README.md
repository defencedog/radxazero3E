# Radxa ZERO 3E (Rockchip RK3566) Resource & Knowledge Base

[![Board](https://img.shields.io/badge/Hardware-Radxa%20ZERO%203E-blue.svg)](https://radxa.com/products/zeros/zero3e)
[![SoC](https://img.shields.io/badge/SoC-Rockchip%20RK3566-orange.svg)](https://www.rock-chips.com/)
[![NPU](https://img.shields.io/badge/NPU-RKNN%201.0%20TOPS-green.svg)](https://github.com/rockchip-linux/rknpu2)
[![GPU](https://img.shields.io/badge/GPU-Mali--G52%202EE-purple.svg)](https://gitlab.freedesktop.org/panfrost)
[![Form Factor](https://img.shields.io/badge/Form%20Factor-70x30mm%20Zero-lightgrey.svg)](https://radxa.com/)

A curated repository of hardware documentation, device tree overlays, edge AI stacks (Immich VPU/NPU), CasaOS templates, system optimizations, and practical tutorials for the ultra-compact **Radxa ZERO 3E** Single Board Computer.

---

## 📋 Hardware Specifications

| Subsystem | Specification |
| :--- | :--- |
| **Processor (SoC)** | Rockchip RK3566 (Quad-Core 64-bit ARM Cortex-A55 @ up to 1.8 GHz / 2.0 GHz OC) |
| **Graphics (GPU)** | ARM Mali-G52-2EE (OpenGL ES 1.1/2.0/3.2, Vulkan 1.1, OpenCL 2.0) |
| **Neural Engine (NPU)** | Rockchip RKNN 1.0 TOPS @ INT8 (Supports TensorFlow, PyTorch, Caffe, ONNX) |
| **Video Engine (VPU)** | 4K@60fps H.265/H.264/VP9 decode, 1080p@60fps H.265/H.264 encode |
| **Networking** | Native Gigabit Ethernet (10/100/1000 Mbps RJ45) with optional PoE HAT support |
| **I/O & Expansion** | 40-pin GPIO header, USB 3.0 Type-C HOST, USB 2.0 Type-C OTG / Power |
| **Video Output** | Micro HDMI port supporting displays up to 1080p / 4K@60Hz |
| **Form Factor** | Ultra-compact 70 mm × 30 mm (Raspberry Pi Zero footprint with full Gigabit LAN) |

---

## 🗂️ Repository Architecture

The repository is organized into 5 dedicated, modular directories:

```text
radxazero3E/
├── tutorials/       # System administration, Docker watchdog, and GPIO tutorials
├── kernels/         # Device tree overlays (dtb_dtbo) and overclocked DTBs
├── hardware/        # Schematics, GPIO pinouts, DXF 3D case model, and peripherals
├── apps/            # Self-hosted applications (Immich VPU/NPU, RKNN Object Detectors, Paperless-ngx, Recoll)
├── files_tools/     # CasaOS YAML templates, Android companion clients, Samba configs
├── .gitignore       # Repository exclusion rules
└── README.md        # Master documentation (this file)
```

---

## 🚀 Navigation & Component Index

### 1. [Tutorials & Troubleshooting (`tutorials/`)](./tutorials/)
Comprehensive guides for configuring, optimizing, and extending your Radxa ZERO 3E:
- [**First Start & Installation**](./tutorials/First_Start_Install.md): Complete initial Armbian setup checklist, package mirrors, and system provisioning.
- [**Manual Overclocking Guide**](./tutorials/Manual_Overclocking.md): Safe CPU scaling up to 2.0 GHz and thermal curve management.
- [**Ramlog Sizing & Syslog Error Fix**](./tutorials/Increase_ramlog_avoid_rsyslog_errors.md): Increasing ramlog partition size to eliminate rsyslog crashes and disk fill.
- [**CasaOS Container Crash Fix (Exit 134)**](./tutorials/CasaOS_Docker_Container_Bug.md): Resolving runc shim task exit status 134 crashes in CasaOS.
- [**Docker Health Checker Watchdog**](./tutorials/Systemd_Service_Docker_health_checker.md): Automated systemd timer/service watchdog that revives dead containers.
- [**Software RAID via mdadm in CasaOS**](./tutorials/RAID_via_mdadm_in_CasaOS.md): Assembling software RAID arrays for high-reliability CasaOS storage.
- [**SIST2 Advanced SQLite Syntax**](./tutorials/SIST2_Advance_SQLite_Syntax.md): FTS query construction for the SIST2 lightweight document indexer.
- [**Non-Root GPIO Access**](./tutorials/Non-root_access_GPIO.md): Udev rules and permission groups for non-root 40-pin GPIO control.
- [**High-Power LED GPIO Switch**](./tutorials/High_Power_Led_GPIO_Switch.md): Driving high-current LED loads using MOSFET / transistor circuits.
- [**Hardware PWM Pin Configuration**](./tutorials/PWM_GPIO.md): Initializing hardware PWM channels for fan speed control.

---

### 2. [Kernels & Device Trees (`kernels/`)](./kernels/)
Verified device trees, overlays, and frequency profiles:
- [**Device Tree Overlays (`kernels/dtb_dtbo/`)](./kernels/dtb_dtbo/): Compiled `.dtbo` overlay files, overlay source trees, and overclocked DTB configurations (`overclocked/`) supporting 2.0 GHz CPU and 500 MHz VPU operation.

---

### 3. [Hardware & Peripherals (`hardware/`)](./hardware/)
Official schematics, mechanical drawings, and peripheral hardware:
- [**Manuals & Schematics**](./hardware/manuals/): Official schematics (`radxa_zero_3e_v1200_schematic.pdf`), component placement maps, product brief, 40-pin GPIO map (`GPIO.md`), and 3D printable case models (`case-for-radxa-zero-3e-model_files.zip`).
- [**Peripherals & Cooling**](./hardware/peripherals/): Powered USB-C hub wiring (RSHTech), 5-pin USB adapters, and dual-fan cooling solutions.

---

### 4. [Self-Hosted Application Stacks (`apps/`)](./apps/)
Optimized application stacks designed for the RK3566:
- [**Immich with Rockchip VPU/NPU Acceleration**](./apps/immich_Rockchip_VPU_NPU/): Immich photo and video management with hardware video transcoding (Rockchip MPP/RGA VPU) and NPU machine learning acceleration.
- [**Universal RKNN Object Detectors**](./apps/image_detectors_rknn/): Multi-architecture edge AI object detection suite (PP-PicoDet, YOLOv8, YOLO11, YOLO-NAS) on the RK3566 NPU with automated benchmarking.
- [**Paperless-ngx**](./apps/paperless-ngx/): Document management system with optimized SQLite configuration and OCR tuning.
- [**Recoll Full-Text Desktop Search**](./apps/recoll_debian/): Complete desktop search engine package for Debian/Armbian with prebuilt archives and user guide.

---

### 5. [Templates & Tools (`files_tools/`)](./files_tools/)
Portable configuration templates and companion packages:
- [**CasaOS Application Templates**](./files_tools/CasaOS_yaml/): Curated Docker Compose YAML definitions for Jellyfin, Calibre, KeepassXC, n8n, Stirling-PDF, Memos, MeTube, and SIST2.
- [**Android Companion Clients**](./files_tools/android_clients/): Multi-part 7z archives of companion mobile clients (Syncthing Android, Moe Memos).
- [**Optimized Samba Configurations**](./files_tools/etc_samba/): Low-overhead Samba server configurations (`smb.conf`, `smb.casa.conf`) tuned for high-throughput LAN file transfer.

---

## 📜 License & Acknowledgments

- **Repository Maintainer:** Usama Khan ([cv.ukhan.org](https://cv.ukhan.org))
- **Hardware Manufacturer:** Radxa Limited ([radxa.com](https://radxa.com))
- **SoC Manufacturer:** Rockchip Electronics Co., Ltd.
