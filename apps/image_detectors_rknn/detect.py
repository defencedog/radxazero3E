#!/usr/bin/env python3
"""
RKNN Unified Object Detection Runner
Universal Multi-Model Detector for Rockchip RK3566 / RK3588 NPU

Supported Model Architectures:
  1. Baidu PP-PicoDet (picodet_s_320, picodet_s_416)
  2. Ultralytics YOLO (default-yolov8n, yolo11n_320, yolo11n 640x640)
  3. Deci AI YOLO-NAS (deci-fp16-yolonas_s 320x320)

Usage:
  python3 detect.py <input_img> <output_img> [conf_thresh] [model_path]
  python3 detect.py --benchmark
"""

import sys
import os
import time
import cv2
import numpy as np
from rknnlite.api import RKNNLite

COCO_CLASSES = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
    'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
    'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
    'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
    'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
    'hair drier', 'toothbrush'
]

# Distinct colors per class for visualization
COLORS = np.random.default_rng(42).uniform(60, 255, size=(len(COCO_CLASSES), 3)).astype(int).tolist()

def get_input_dims(rknn, model_path):
    """Dynamically query input tensor dimensions from RKNN runtime, with filename fallback."""
    infer_w, infer_h = 320, 320
    try:
        attr = rknn.rknn_runtime.get_tensor_attr(0)
        dims = list(attr.dims)[:attr.n_dims]
        spatial = [d for d in dims if d > 3]
        if len(spatial) >= 2:
            infer_h, infer_w = spatial[0], spatial[1]
        elif len(spatial) == 1:
            infer_h = infer_w = spatial[0]
    except Exception:
        fname = os.path.basename(model_path).lower()
        if '640' in fname:
            infer_w = infer_h = 640
        elif '416' in fname:
            infer_w = infer_h = 416
        else:
            infer_w = infer_h = 320
    return infer_w, infer_h

def run_detection(model_path, input_path, output_path=None, conf_thresh=0.25, nms_thresh=0.45, verbose=True):
    """
    Executes end-to-end detection on a single image.
    Handles dynamic architecture identification, preprocessing, NPU inference, and postprocessing.
    """
    orig_img = cv2.imread(input_path)
    if orig_img is None:
        print(f"Error: Could not read image from '{input_path}'", file=sys.stderr)
        return None

    h_orig, w_orig = orig_img.shape[:2]

    # Initialize RKNN Runtime
    rknn = RKNNLite(verbose=False)
    if rknn.load_rknn(model_path) != 0:
        print(f"Error: Failed to load RKNN model '{model_path}'", file=sys.stderr)
        return None

    if rknn.init_runtime(core_mask=RKNNLite.NPU_CORE_AUTO) != 0:
        print("Error: Failed to initialize RKNN runtime", file=sys.stderr)
        return None

    infer_w, infer_h = get_input_dims(rknn, model_path)

    # Preprocessing (Bilinear resize to NPU input resolution, NCHW layout)
    t_pre0 = time.perf_counter()
    img_resized = cv2.resize(orig_img, (infer_w, infer_h), interpolation=cv2.INTER_LINEAR)
    inp = np.transpose(img_resized, (2, 0, 1)).astype(np.float32)
    inp = np.expand_dims(inp, 0)
    t_pre = (time.perf_counter() - t_pre0) * 1000.0

    # NPU Inference
    t_infer0 = time.perf_counter()
    outputs = rknn.inference(inputs=[inp])
    t_infer = (time.perf_counter() - t_infer0) * 1000.0
    rknn.release()

    if not outputs or len(outputs) == 0:
        print("Error: NPU inference returned empty outputs", file=sys.stderr)
        return None

    # Universal Postprocessing based on output head count and shapes
    t_post0 = time.perf_counter()
    scale_x = w_orig / float(infer_w)
    scale_y = h_orig / float(infer_h)

    num_out = len(outputs)
    nms_boxes = []
    cids_filt = []
    confs_filt = []

    if num_out == 1:
        # Architecture: Ultralytics YOLOv8 / YOLO11
        # Output shape: (1, 84, N) -> first 4 rows [cx, cy, w, h], next 80 rows class logits
        out = outputs[0][0]  # (84, N)
        boxes_raw = out[:4, :].T  # (N, 4)
        scores_raw = out[4:, :].T  # (N, 80)

        cids = np.argmax(scores_raw, axis=1)
        confs = np.max(scores_raw, axis=1)
        mask = confs >= conf_thresh

        boxes_filt = boxes_raw[mask]
        cids_filt = cids[mask]
        confs_filt = confs[mask]

        for b in boxes_filt:
            cx, cy, bw, bh = b
            x1 = (cx - bw / 2.0) * scale_x
            y1 = (cy - bh / 2.0) * scale_y
            w_box = bw * scale_x
            h_box = bh * scale_y
            nms_boxes.append([int(round(x1)), int(round(y1)), int(round(w_box)), int(round(h_box))])

    elif num_out == 2:
        out0 = outputs[0][0]  # (N, 4) -> [xmin, ymin, xmax, ymax]
        out1 = outputs[1][0]  # (80, N) or (N, 80)

        if out1.shape[0] == 80:
            # Architecture: PP-PicoDet (scores shape: 80 x N)
            scores_raw = out1.T  # Transpose to (N, 80)
        else:
            # Architecture: Deci AI YOLO-NAS (scores shape: N x 80)
            scores_raw = out1

        cids = np.argmax(scores_raw, axis=1)
        confs = np.max(scores_raw, axis=1)
        mask = confs >= conf_thresh

        boxes_filt = out0[mask]
        cids_filt = cids[mask]
        confs_filt = confs[mask]

        for b in boxes_filt:
            x1 = b[0] * scale_x
            y1 = b[1] * scale_y
            x2 = b[2] * scale_x
            y2 = b[3] * scale_y
            w_box = max(0, x2 - x1)
            h_box = max(0, y2 - y1)
            nms_boxes.append([int(round(x1)), int(round(y1)), int(round(w_box)), int(round(h_box))])
    else:
        print(f"Error: Unsupported model output tensor count: {num_out}", file=sys.stderr)
        return None

    # Non-Maximum Suppression (NMS)
    detections = []
    if len(nms_boxes) > 0:
        indices = cv2.dnn.NMSBoxes(nms_boxes, confs_filt.tolist(), conf_thresh, nms_thresh)
        if len(indices) > 0:
            indices = np.array(indices).flatten()
            for idx in indices:
                cid = int(cids_filt[idx])
                conf = float(confs_filt[idx])
                box = nms_boxes[idx]
                cname = COCO_CLASSES[cid] if cid < len(COCO_CLASSES) else f'class_{cid}'
                detections.append({
                    'class_id': cid,
                    'class_name': cname,
                    'confidence': conf,
                    'box': box
                })

    t_post = (time.perf_counter() - t_post0) * 1000.0
    t_total = t_pre + t_infer + t_post

    # Standard stdout output matching production pipeline format
    if verbose:
        for det in detections:
            x, y, w, h = det['box']
            x1 = max(0, min(w_orig - 1, x))
            y1 = max(0, min(h_orig - 1, y))
            x2 = max(0, min(w_orig - 1, x + w))
            y2 = max(0, min(h_orig - 1, y + h))
            print(f"{det['class_name']} @ ({x1} {y1} {x2} {y2}) {det['confidence']:.6f}")

    # Render Visual Annotations
    if output_path:
        annotated = orig_img.copy()
        for det in detections:
            x, y, w, h = det['box']
            x1 = max(0, min(w_orig - 1, x))
            y1 = max(0, min(h_orig - 1, y))
            x2 = max(0, min(w_orig - 1, x + w))
            y2 = max(0, min(h_orig - 1, y + h))

            cid = det['class_id']
            color = COLORS[cid % len(COLORS)]

            # Bounding rectangle
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)

            # Label banner
            label = f"{det['class_name']} {det['confidence']*100:.1f}%"
            (tw, th), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            by1 = max(0, y1 - th - baseline - 4)
            by2 = y1
            bx2 = min(w_orig - 1, x1 + tw + 6)
            cv2.rectangle(annotated, (x1, by1), (bx2, by2), color, -1)
            cv2.putText(annotated, label, (x1 + 3, y1 - baseline - 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

        # Telemetry HUD Header
        mname = os.path.basename(model_path)
        fps = 1000.0 / t_infer if t_infer > 0 else 0
        hud = f"{mname} | Latency: {t_infer:.1f}ms ({fps:.1f} FPS) | Objects: {len(detections)}"
        cv2.putText(annotated, hud, (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(annotated, hud, (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

        out_dir = os.path.dirname(output_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
        cv2.imwrite(output_path, annotated)

    return {
        'model': os.path.basename(model_path),
        'input_dims': (infer_w, infer_h),
        'num_detections': len(detections),
        'detections': detections,
        't_pre_ms': t_pre,
        't_infer_ms': t_infer,
        't_post_ms': t_post,
        't_total_ms': t_total,
        'fps': 1000.0 / t_infer if t_infer > 0 else 0
    }

def run_all_benchmarks():
    """Run full benchmark matrix across all 6 models and 6 sample images."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(script_dir, "models")
    sample_dir = os.path.join(script_dir, "sample_img")

    models = [
        ("yolo11n_320_rk3566.rknn", "YOLO11n (320x320)"),
        ("default-yolov8n-rk3566.rknn", "YOLOv8n (320x320)"),
        ("picodet_s_320_rk3566.rknn", "PP-PicoDet-S (320x320)"),
        ("deci-fp16-yolonas_s-rk3566-v2.3.2-2.rknn", "YOLO-NAS-S (320x320)"),
        ("picodet_s_416_rk3566.rknn", "PP-PicoDet-S (416x416)"),
        ("yolo11n_rk3566.rknn", "YOLO11n (640x640)")
    ]

    sample_imgs = [
        ("1.jpg", "Birds & Jet"),
        ("2.jpg", "Elephants & Truck"),
        ("3.jpg", "Crowd / Street"),
        ("4.jpg", "Traffic Lights & Bike"),
        ("5.jpg", "Indoor People"),
        ("6.jpg", "Street Landscape")
    ]

    print("\n" + "=" * 80)
    print("RKNN NPU OBJECT DETECTION BENCHMARK MATRIX (RK3566 @ 0.8 TOPS)")
    print("=" * 80 + "\n")

    print("### Phase 1: Pure NPU Inference Latency (20 Warm Cycles)\n")
    print("| Model Architecture | Input Res | File Size | Inference Latency | NPU FPS |")
    print("|---|:---:|:---:|:---:|:---:|")

    for mfile, mlabel in models:
        mpath = os.path.join(models_dir, mfile)
        if not os.path.exists(mpath):
            continue
        msize = os.path.getsize(mpath) / (1024 * 1024)

        rknn = RKNNLite(verbose=False)
        rknn.load_rknn(mpath)
        rknn.init_runtime(core_mask=RKNNLite.NPU_CORE_AUTO)

        infer_w, infer_h = get_input_dims(rknn, mpath)
        dummy_inp = np.zeros((1, 3, infer_h, infer_w), dtype=np.float32)

        # Warmup
        rknn.inference(inputs=[dummy_inp])

        t0 = time.perf_counter()
        iters = 20
        for _ in range(iters):
            rknn.inference(inputs=[dummy_inp])
        lat = (time.perf_counter() - t0) / iters * 1000.0
        fps = 1000.0 / lat
        rknn.release()

        print(f"| **{mlabel}** | {infer_w}x{infer_h} | {msize:.1f} MB | **{lat:.1f} ms** | **{fps:.1f} FPS** |")

    print("\n### Phase 2: Full End-to-End Pipeline Performance across Sample Images (conf=0.25)\n")
    headers = ["Model"] + [f"{fname} ({desc})" for fname, desc in sample_imgs]
    print("| " + " | ".join(headers) + " |")
    print("|---|" + "|".join([":---:" for _ in sample_imgs]) + "|")

    for mfile, mlabel in models:
        mpath = os.path.join(models_dir, mfile)
        if not os.path.exists(mpath):
            continue
        row = [f"**{mlabel}**"]
        for sfile, sdesc in sample_imgs:
            spath = os.path.join(sample_dir, sfile)
            out_img = f"/tmp/bench_{sfile}_{mfile}.jpg"
            res = run_detection(mpath, spath, out_img, conf_thresh=0.25, verbose=False)
            if res:
                row.append(f"{res['num_detections']} obj ({res['t_total_ms']:.1f}ms)")
            else:
                row.append("ERR")
        print("| " + " | ".join(row) + " |")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--benchmark':
        run_all_benchmarks()
        sys.exit(0)

    if len(sys.argv) < 3:
        print("Usage: python3 detect.py <input_img> <output_img> [conf_thresh] [model_path]")
        print("       python3 detect.py --benchmark")
        sys.exit(1)

    inp = sys.argv[1]
    out = sys.argv[2]
    conf = float(sys.argv[3]) if len(sys.argv) > 3 else 0.25

    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_model = os.path.join(script_dir, "models", "picodet_s_416_rk3566.rknn")
    mod = sys.argv[4] if len(sys.argv) > 4 else default_model

    run_detection(mod, inp, out, conf, verbose=True)

if __name__ == '__main__':
    main()
