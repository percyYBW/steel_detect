# 车辆零部件的表面缺陷视觉检测系统

## 项目简介

本项目旨在开发一个基于机器视觉和深度学习的车辆零部件缺陷检测系统软件。该软件通过拍摄钢材表面图片，经过检测系统算法来识别缺陷，并对缺陷进行分类。

## 项目结构

```
vehicle_defect_detection/
├── app.py                  # 主应用程序
├── requirements.txt        # 依赖包列表
├── static/                 # 静态文件目录
├── templates/              # 模板文件目录
├── models/                 # 存放训练好的模型
├── uploads/                # 存放上传的图像文件
├── utils/                  # 工具函数目录
│   ├── image_processing.py # 图像处理相关函数
│   └── data_converter.py   # JSON与XML转换工具
└── README.md               # 项目说明文档
```

## 安装依赖

```sh
pip install -r requirements.txt
```

## 运行应用

1. 创建并激活虚拟环境（可选）：
   ```sh
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

2. 安装依赖：
   ```sh
   pip install -r requirements.txt
   ```

3. 运行应用：
   ```sh
   python app.py
   ```

## API 接口

### 上传图像

- **URL**: `/api/upload`
- **Method**: `POST`
- **Request Parameters**:
  - `file`: 上传的图像文件
- **Response**:
  ```json
  {
    "status": "success",
    "file_id": "1234567890abcdef"
  }
  ```

### 检测图像

- **URL**: `/api/detect`
- **Method**: `POST`
- **Request Parameters**:
  - `file_id`: 上传文件的唯一标识符
- **Response**:
  ```json
  {
    "status": "success",
    "defects": [
      {
        "type": "scratch",
        "confidence": 0.95
      },
      {
        "type": "inclusion",
        "confidence": 0.85
      }
    ]
  }
  ```

### 查询检测结果

- **URL**: `/api/results`
- **Method**: `GET`
- **Request Parameters**:
  - `file_id`: 上传文件的唯一标识符
- **Response**:
  ```json
  {
    "status": "success",
    "defects": [
      {
        "type": "scratch",
        "confidence": 0.95
      },
      {
        "type": "inclusion",
        "confidence": 0.85
      }
    ]
  }
  ```

### 查询所有检测记录

- **URL**: `/api/records`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "status": "success",
    "records": []
  }
  ```

### JSON 转 XML

- **URL**: `/api/json_to_xml`
- **Method**: `POST`
- **Request Parameters**:
  - JSON 数据
- **Response**:
  ```json
  {
    "status": "success",
    "xml": "<xml>...</xml>"
  }
  ```

### XML 转 JSON

- **URL**: `/api/xml_to_json`
- **Method**: `POST`
- **Request Parameters**:
  - XML 数据
- **Response**:
  ```json
  {
    "status": "success",
    "json": {...}
  }
  ```

## 注意事项

- 您可能需要根据实际情况修改 `app.py` 中的 `UPLOAD_FOLDER` 路径。
- 确保在 `models/` 目录中放置训练好的深度学习模型文件。