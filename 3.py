from pathlib import Path
import zipfile, textwrap

root = Path("/mnt/data/digital_twin_onnx")
(root / "models").mkdir(parents=True, exist_ok=True)

detector_py = r'''from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

import cv2
import numpy as np
import onnxruntime as ort
from PIL import Image


@dataclass
class Detection:
    x1: int
    y1: int
    x2: int
    y2: int
    confidence: float
    class_id: int
    class_name: str


class ONNXDetector:
    """
    YOLO ONNX inference helper.

    Supported common output layouts:
      1) YOLOv8/YOLO11 raw output: [1, 4 + classes, N] or [1, N, 4 + classes]
      2) YOLOv5 raw output: [1, N, 5 + classes] (objectness + class scores)
      3) NMS output: [N, 6] or [1, N, 6] as x1,y1,x2,y2,score,class_id

    Note: exported ONNX models differ. Check session output shape and adjust
    parse_output() if your export uses a different layout or normalized boxes.
    """

    def __init__(
        self,
        model_path: Optional[str] = None,
        model_bytes: Optional[bytes] = None,
        class_names: Optional[Sequence[str]] = None,
        input_size: int = 640,
        conf_threshold: float = 0.35,
        iou_threshold: float = 0.45,
    ):
        if model_bytes is None and not model_path:
            raise ValueError("请提供 ONNX 模型路径或模型文件内容。")

        providers = ["CPUExecutionProvider"]
        available = ort.get_available_providers()
        if "CUDAExecutionProvider" in available:
            providers.insert(0, "CUDAExecutionProvider")

        source = model_bytes if model_bytes is not None else str(model_path)
        self.session = ort.InferenceSession(source, providers=providers)
        self.input_meta = self.session.get_inputs()[0]
        self.input_name = self.input_meta.name
        self.output_names = [o.name for o in self.session.get_outputs()]

        shape = self.input_meta.shape
        # Typical NCHW input: [1, 3, 640, 640]
        self.input_h = int(shape[2]) if len(shape) == 4 and isinstance(shape[2], int) else input_size
        self.input_w = int(shape[3]) if len(shape) == 4 and isinstance(shape[3], int) else input_size
        self.class_names = list(class_names) if class_names else []
        self.conf_threshold = float(conf_threshold)
        self.iou_threshold = float(iou_threshold)

    @staticmethod
    def _letterbox(image: np.ndarray, new_shape: tuple[int, int]):
        h, w = image.shape[:2]
        new_h, new_w = new_shape
        scale = min(new_w / w, new_h / h)
        resized_w, resized_h = int(round(w * scale)), int(round(h * scale))
        resized = cv2.resize(image, (resized_w, resized_h), interpolation=cv2.INTER_LINEAR)

        pad_w = new_w - resized_w
        pad_h = new_h - resized_h
        left = pad_w // 2
        right = pad_w - left
        top = pad_h // 2
        bottom = pad_h - top
        canvas = cv2.copyMakeBorder(
            resized, top, bottom, left, right,
            cv2.BORDER_CONSTANT, value=(114, 114, 114)
        )
        return canvas, scale, left, top

    def _preprocess(self, image_rgb: np.ndarray):
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        padded, scale, pad_x, pad_y = self._letterbox(
            image_bgr, (self.input_h, self.input_w)
        )
        tensor = padded[:, :, ::-1].transpose(2, 0, 1)
        tensor = np.ascontiguousarray(tensor, dtype=np.float32) / 255.0
        tensor = tensor[None, ...]
        return tensor, scale, pad_x, pad_y

    def _name(self, class_id: int) -> str:
        if 0 <= class_id < len(self.class_names):
            return self.class_names[class_id]
        return f"class_{class_id}"

    def _nms(self, boxes_xywh, scores, class_ids):
        if len(boxes_xywh) == 0:
            return []
        indices = cv2.dnn.NMSBoxes(
            boxes_xywh,
            scores,
            self.conf_threshold,
            self.iou_threshold
        )
        if len(indices) == 0:
            return []
        return np.array(indices).reshape(-1).tolist()

    def _parse_output(self, output: np.ndarray):
        pred = np.asarray(output)
        pred = np.squeeze(pred)

        if pred.ndim == 1:
            pred = pred.reshape(1, -1)
        if pred.ndim != 2:
            raise RuntimeError(f"暂不支持模型输出维度：{pred.shape}")

        # End-to-end/NMS output: x1,y1,x2,y2,confidence,class_id
        if pred.shape[-1] == 6:
            rows = []
            for row in pred:
                x1, y1, x2, y2, score, cls = row[:6]
                if float(score) < self.conf_threshold:
                    continue
                rows.append((float(x1), float(y1), float(x2), float(y2),
                             float(score), int(cls)))
            return rows, "xyxy"

        # YOLO raw outputs. Convert [features, candidates] to [candidates, features].
        if pred.shape[0] < pred.shape[1] and pred.shape[0] in (4 + 1, 4 + 2, 4 + 3, 4 + 4, 4 + 5, 4 + 6, 4 + 7, 4 + 8, 4 + 9, 4 + 10, 4 + 11, 4 + 12, 4 + 13, 4 + 14, 4 + 15, 4 + 16, 4 + 17, 4 + 18, 4 + 19, 4 + 20, 4 + 21, 4 + 22, 4 + 23, 4 + 24, 4 + 25, 4 + 26, 4 + 27, 4 + 28, 4 + 29, 4 + 30, 4 + 31, 4 + 32, 4 + 33, 4 + 34, 4 + 35, 4 + 36, 4 + 37, 4 + 38, 4 + 39, 4 + 40, 4 + 41, 4 + 42, 4 + 43, 4 + 44, 4 + 45, 4 + 46, 4 + 47, 4 + 48, 4 + 49, 4 + 50, 4 + 51, 4 + 52, 4 + 53, 4 + 54, 4 + 55, 4 + 56, 4 + 57, 4 + 58, 4 + 59, 4 + 60, 4 + 61, 4 + 62, 4 + 63, 4 + 64, 4 + 65, 4 + 66, 4 + 67, 4 + 68, 4 + 69, 4 + 70, 4 + 71, 4 + 72, 4 + 73, 4 + 74, 4 + 75, 4 + 76, 4 + 77, 4 + 78, 4 + 79, 4 + 80):
            pred = pred.T

        rows = []
        feature_count = pred.shape[1]
        is_yolov5 = feature_count > 6 and feature_count - 5 > 0

        for row in pred:
            if feature_count < 5:
                continue
            cx, cy, bw, bh = map(float, row[:4])

            if is_yolov5:
                objectness = float(row[4])
                class_scores = row[5:]
                class_id = int(np.argmax(class_scores))
                score = objectness * float(class_scores[class_id])
            else:
                class_scores = row[4:]
                class_id = int(np.argmax(class_scores))
                score = float(class_scores[class_id])

            if score < self.conf_threshold:
                continue

            x1 = cx - bw / 2
            y1 = cy - bh / 2
            x2 = cx + bw / 2
            y2 = cy + bh / 2
            rows.append((x1, y1, x2, y2, score, class_id))
        return rows, "xyxy"

    def predict(self, image: Image.Image):
        image_rgb = np.asarray(image.convert("RGB"))
        orig_h, orig_w = image_rgb.shape[:2]
        tensor, scale, pad_x, pad_y = self._preprocess(image_rgb)

        outputs = self.session.run(self.output_names, {self.input_name: tensor})
        rows, _ = self._parse_output(outputs[0])

        detections = []
        boxes_for_nms, scores, class_ids = [], [], []
        raw_rows = []

        for x1, y1, x2, y2, score, class_id in rows:
            # Map model coordinates back to original image coordinates.
            x1 = (x1 - pad_x) / scale
            x2 = (x2 - pad_x) / scale
            y1 = (y1 - pad_y) / scale
            y2 = (y2 - pad_y) / scale

            x1 = float(np.clip(x1, 0, orig_w - 1))
            x2 = float(np.clip(x2, 0, orig_w - 1))
            y1 = float(np.clip(y1, 0, orig_h - 1))
            y2 = float(np.clip(y2, 0, orig_h - 1))
            if x2 <= x1 or y2 <= y1:
                continue

            raw_rows.append((x1, y1, x2, y2, score, class_id))
            boxes_for_nms.append([int(x1), int(y1), int(x2 - x1), int(y2 - y1)])
            scores.append(float(score))
            class_ids.append(int(class_id))

        # Class-aware NMS to avoid suppressing overlapping objects of different classes.
        keep = []
        for cls in sorted(set(class_ids)):
            local = [i for i, c in enumerate(class_ids) if c == cls]
            local_indices = self._nms(
                [boxes_for_nms[i] for i in local],
                [scores[i] for i in local],
                [class_ids[i] for i in local]
            )
            keep.extend(local[i] for i in local_indices)

        for i in keep:
            x1, y1, x2, y2, score, class_id = raw_rows[i]
            detections.append(Detection(
                int(round(x1)), int(round(y1)), int(round(x2)), int(round(y2)),
                float(score), int(class_id), self._name(int(class_id))
            ))

        detections.sort(key=lambda d: d.confidence, reverse=True)
        return detections

    @staticmethod
    def draw(image: Image.Image, detections: list[Detection]):
        from PIL import ImageDraw, ImageFont

        result = image.convert("RGB").copy()
        draw = ImageDraw.Draw(result)
        try:
            font = ImageFont.truetype("msyh.ttc", 18)
        except OSError:
            font = ImageFont.load_default()

        palette = [
            (0, 220, 220), (255, 178, 46), (64, 230, 160),
            (70, 150, 255), (220, 90, 240), (255, 100, 100)
        ]
        for det in detections:
            color = palette[det.class_id % len(palette)]
            draw.rectangle((det.x1, det.y1, det.x2, det.y2), outline=color, width=3)
            label = f"{det.class_name} {det.confidence:.2f}"
            box = draw.textbbox((det.x1, max(0, det.y1 - 24)), label, font=font)
            draw.rectangle(box, fill=color)
            draw.text((det.x1, max(0, det.y1 - 24)), label, fill=(0, 15, 20), font=font)
        return result
'''

app_py = r'''from __future__ import annotations

from collections import Counter
from pathlib import Path
import time

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

from detector import ONNXDetector

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
DEFAULT_MODEL = MODEL_DIR / "model.onnx"

st.set_page_config(
    page_title="智能工厂数字孪生平台",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&display=swap');
.stApp { background:#06131d; color:#d9faff; }
header, footer, #MainMenu {visibility:hidden;}
.block-container {padding:1rem 1.5rem 2rem 1.5rem; max-width:1800px;}
[data-testid="stSidebar"] {background:#081c28;border-right:1px solid #155b69;}
[data-testid="stMetric"] {background:linear-gradient(135deg,#0c2b38,#091b28);
border:1px solid #176273;padding:12px;border-radius:5px;}
[data-testid="stMetricLabel"] {color:#77cbd2;}
[data-testid="stMetricValue"] {color:#dfffff;}
h1,h2,h3 {color:#dfffff!important;}
div.stButton>button {background:#087d89;color:white;border:1px solid #20dce1;border-radius:3px;}
div.stButton>button:hover {background:#0a9da6;color:white;border-color:#8affff;}
div[data-testid="stFileUploader"] {background:#0a202b;border:1px dashed #168897;padding:10px;border-radius:5px;}
.small-note {color:#78b9c1;font-size:12px;}
.status-pill {display:inline-block;padding:4px 10px;border:1px solid #20cfae;color:#4ae6bf;
background:#06372f;border-radius:2px;font-size:12px;}
</style>
""", unsafe_allow_html=True)

if "detections" not in st.session_state:
    st.session_state.detections = []
if "annotated" not in st.session_state:
    st.session_state.annotated = None
if "source_name" not in st.session_state:
    st.session_state.source_name = "等待上传检测图片"
if "infer_ms" not in st.session_state:
    st.session_state.infer_ms = 0.0

@st.cache_resource(show_spinner=False)
def load_detector(model_bytes: bytes, class_names_text: str, conf: float, iou: float):
    names = [x.strip() for x in class_names_text.split(",") if x.strip()]
    return ONNXDetector(
        model_bytes=model_bytes,
        class_names=names,
        conf_threshold=conf,
        iou_threshold=iou,
    )

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## ⚙ 系统控制中心")
    st.markdown('<span class="status-pill">● 平台运行中</span>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### ONNX 模型配置")
    uploaded_model = st.file_uploader("上传目标检测模型（.onnx）", type=["onnx"])
    if uploaded_model is not None:
        model_bytes = uploaded_model.getvalue()
        model_label = uploaded_model.name
    elif DEFAULT_MODEL.exists():
        model_bytes = DEFAULT_MODEL.read_bytes()
        model_label = "models/model.onnx"
    else:
        model_bytes = None
        model_label = "未加载模型"

    st.caption(f"当前模型：{model_label}")
    class_names_text = st.text_area(
        "类别名称（按模型类别ID顺序，用英文逗号分隔）",
        value="person,bicycle,car,motorcycle,airplane,bus,train,truck,boat,traffic light",
        height=90,
        help="如果是自定义训练模型，请按训练时的类别顺序填写。类别名称数量应与模型类别数一致。"
    )
    conf = st.slider("置信度阈值", 0.05, 0.95, 0.35, 0.05)
    iou = st.slider("NMS IoU 阈值", 0.10, 0.90, 0.45, 0.05)
    st.markdown("---")
    st.markdown("### 检测输入")
    uploaded_image = st.file_uploader("上传待检测图片", type=["jpg", "jpeg", "png", "bmp"])
    run_button = st.button("▶ 开始目标检测", use_container_width=True, disabled=(model_bytes is None or uploaded_image is None))
    st.markdown("---")
    st.markdown("### 说明")
    st.markdown(
        '<div class="small-note">当前支持常见 YOLO ONNX 输出格式。'
        '不同训练框架的导出格式可能不同，正式接入时需要核对模型输入尺寸、输出张量和类别顺序。</div>',
        unsafe_allow_html=True
    )

# ---------- Inference ----------
if run_button and uploaded_image is not None and model_bytes is not None:
    try:
        source_image = Image.open(uploaded_image).convert("RGB")
        with st.spinner("ONNX Runtime 正在执行目标检测..."):
            detector = load_detector(model_bytes, class_names_text, conf, iou)
            start = time.perf_counter()
            detections = detector.predict(source_image)
            elapsed = (time.perf_counter() - start) * 1000
            annotated = detector.draw(source_image, detections)

        st.session_state.detections = detections
        st.session_state.annotated = annotated
        st.session_state.source_name = uploaded_image.name
        st.session_state.infer_ms = elapsed
    except Exception as exc:
        st.error(f"模型推理失败：{exc}")
        st.info("请检查 ONNX 模型导出格式、输入尺寸、类别配置，以及模型是否为目标检测模型。")

detections = st.session_state.detections
counts = Counter(d.class_name for d in detections)
object_count = len(detections)
class_count = len(counts)
avg_conf = sum(d.confidence for d in detections) / object_count if object_count else 0.0

# ---------- Header ----------
head_l, head_r = st.columns([3, 1])
with head_l:
    st.markdown("# 🏭 智能工厂数字孪生平台")
    st.caption("INTELLIGENT FACTORY DIGITAL TWIN · MACHINE VISION MONITORING")
with head_r:
    st.markdown(
        f'<div style="text-align:right;padding-top:18px;color:#72c5cd;">'
        f'系统时间　{time.strftime("%Y-%m-%d %H:%M:%S")}<br>'
        f'<span style="color:#43e4b4;">● ONNX 推理服务就绪</span></div>',
        unsafe_allow_html=True
    )

# ---------- KPI ----------
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("本次检测目标", object_count, help="当前图片检测到的目标总数")
k2.metric("目标类别数", class_count)
k3.metric("平均置信度", f"{avg_conf * 100:.1f}%")
k4.metric("推理耗时", f"{st.session_state.infer
