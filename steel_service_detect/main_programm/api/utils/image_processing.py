import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import numpy as np
import os
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_model(model_path, device):
    """加载预训练模型"""
    if not os.path.exists(model_path):
        logger.error(f"模型文件未找到: {model_path}")
        raise FileNotFoundError(f"模型文件未找到: {model_path}")
    try:
        model = torch.load(model_path, map_location=device)
        model.eval()
        logger.info(f"模型加载成功: {model_path}")
        return model
    except Exception as e:
        logger.error(f"加载模型时出错: {e}")
        raise e

def preprocess_image(image_path, image_size=(896,896)): # 调整为模型输入尺寸
    """预处理图像，使其适合模型输入"""
    if not os.path.exists(image_path):
        logger.error(f"图像文件未找到: {image_path}")
        raise FileNotFoundError(f"图像文件未找到: {image_path}")
    try:
        image = Image.open(image_path).convert('RGB')
        preprocess = transforms.Compose([
            transforms.Resize(image_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        image = preprocess(image)
        image = image.unsqueeze(0)  # 增加批次维度
        logger.info(f"图像预处理成功: {image_path}")
        return image
    except Exception as e:
        logger.error(f"预处理图像时出错: {e}")
        raise e

def detect_defects(image_path, model, device, defect_types=None, threshold=0.5):
    """使用深度学习模型检测图像中的缺陷"""
    if defect_types is None:
        defect_types = ['crazing', 'inclusion', 'patches', 'pitted_surface', 'rolled-in_scale', 'scratches']  # 缺陷类型，可能需要修改此列表
    image = preprocess_image(image_path).to(device)
    with torch.no_grad():
        predictions = model(image)
    predictions = torch.sigmoid(predictions).cpu().numpy()
    defects = []

    # 假设模型输出为多个类别的概率
    for i, defect_type in enumerate(defect_types):
        if predictions[0][i] > threshold:
            defects.append({'type': defect_type, 'confidence': float(predictions[0][i])})

    logger.info(f"缺陷检测完成: {defects}")
    return defects

if __name__ == "__main__":
    model_path = "C:\\Users\\Percy\\Desktop\\test-main\\yolov5\\models\\yolov5s.yaml"  # 模型路径，可能需要修改此路径
    image_path = "C:\\Users\\Percy\\Desktop\\test-main\\NEU-DET\\valid\\images"  # 图像路径，可能需要修改此路径

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = load_model(model_path, device)
    defects = detect_defects(image_path, model, device)
    print(defects)