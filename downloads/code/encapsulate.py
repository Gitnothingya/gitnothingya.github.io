import os
import struct
import re
from pathlib import Path
import zipfile

def encapsulate(image_path, zip_path, output_filename):
    """
    将压缩包数据分块封装到图片中
    :param image_path: 原始图片路径
    :param zip_path: 压缩包路径
    :param output_filename: 输出文件名（基础名称）
    """
    # 读取图片数据
    with open(image_path, 'rb') as f:
        img_data = f.read()
    img_len = len(img_data)
    
    # 读取压缩包数据
    with open(zip_path, 'rb') as f:
        zip_data = f.read()
    
    # 分块设置
    chunk_size = 10 * 1024 * 1024  # 10MB
    total_chunks = (len(zip_data) + chunk_size - 1) // chunk_size
    
    # 处理输出文件名
    base, ext = os.path.splitext(output_filename)
    
    for i in range(total_chunks):
        start = i * chunk_size
        end = start + chunk_size
        chunk = zip_data[start:end]
        
        # 构建分块文件名
        if total_chunks > 1:
            chunk_filename = f"{base}_{i}{ext}"
        else:
            chunk_filename = output_filename
        
        # 构建分块文件内容：图片 + 分块数据 + 4字节图片长度
        chunk_file_data = img_data + chunk + struct.pack('!I', img_len)
        
        # 写入文件
        with open(chunk_filename, 'wb') as f:
            f.write(chunk_file_data)

def decapsulate(input_filename):
    """
    从封装图片中提取并解压压缩包
    :param input_filename: 输入文件名（基础名称或分块文件）
    """
    input_path = Path(input_filename)
    if not input_path.exists():
        raise FileNotFoundError(f"文件 {input_filename} 不存在")
    
    # 准备文件收集参数
    dir_path = input_path.parent
    base_stem = input_path.stem
    ext = input_path.suffix
    
    # 匹配分块文件名模式
    match = re.match(r'^(.*?)_(\d+)$', base_stem)
    if match:
        base_name = match.group(1)
        pattern = re.compile(rf'^{re.escape(base_name)}_(\d+){re.escape(ext)}$')
    else:
        base_name = base_stem
        pattern = re.compile(rf'^{re.escape(base_name)}_(\d+){re.escape(ext)}$')
    
    # 收集所有分块文件
    chunk_files = []
    for file in dir_path.iterdir():
        if pattern.match(file.name):
            index = int(pattern.match(file.name).group(1))
            chunk_files.append( (index, file) )
    
    # 如果没有找到分块文件则处理单个文件
    if not chunk_files:
        chunk_files.append( (0, input_path) )
    
    # 按索引排序
    chunk_files.sort()
    
    # 校验并提取数据
    zip_data = bytearray()
    img_len = None
    
    for index, chunk_file in chunk_files:
        with open(chunk_file, 'rb') as f:
            data = f.read()
        
        # 校验文件有效性
        if len(data) < 4:
            raise ValueError(f"文件 {chunk_file} 损坏")
        
        # 提取图片长度信息
        current_img_len = struct.unpack('!I', data[-4:])[0]
        
        # 首次获取图片长度
        if img_len is None:
            img_len = current_img_len
        elif current_img_len != img_len:
            raise ValueError("分块文件中图片长度不一致")
        
        # 校验数据有效性
        if len(data) < img_len + 4:
            raise ValueError(f"文件 {chunk_file} 数据不完整")
        
        # 提取压缩数据
        zip_data.extend(data[img_len:-4])
    
    # 写入临时压缩包
    temp_zip = dir_path / "temp_restored.zip"
    with open(temp_zip, 'wb') as f:
        f.write(zip_data)
    
    # 解压文件
    with zipfile.ZipFile(temp_zip, 'r') as zf:
        zf.extractall(dir_path)
    
    # 清理临时文件
    os.remove(temp_zip)
    print(f"成功解压到目录：{dir_path}")

if __name__ == "__main__":
    # 示例用法
    # 封装示例
    # encapsulate("original.jpg", "data.zip", "output.jpg")
    
    # 解封装示例
    # decapsulate("output_0.jpg")
    pass