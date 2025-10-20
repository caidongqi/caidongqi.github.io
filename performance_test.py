#!/usr/bin/env python3
"""
网站性能测试脚本
测试图片加载速度和整体性能
"""

import requests
import time
import os
from urllib.parse import urljoin

def test_image_performance():
    """测试图片加载性能"""
    base_url = "http://localhost:8000"
    
    # 测试图片列表
    test_images = [
        "/picture/optimized/cdq-cambridge.webp",
        "/picture/optimized/cdq-formal.webp", 
        "/picture/optimized/cdq-madrid-mobicom23.webp",
        "/picture/optimized/cdq-eurosys.webp"
    ]
    
    print("=== 图片加载性能测试 ===")
    
    total_size = 0
    total_time = 0
    
    for img_path in test_images:
        url = urljoin(base_url, img_path)
        try:
            start_time = time.time()
            response = requests.get(url)
            end_time = time.time()
            
            if response.status_code == 200:
                load_time = (end_time - start_time) * 1000  # 转换为毫秒
                size_kb = len(response.content) / 1024
                total_size += size_kb
                total_time += load_time
                
                print(f"✅ {img_path}")
                print(f"   大小: {size_kb:.1f} KB")
                print(f"   加载时间: {load_time:.1f} ms")
                print(f"   速度: {size_kb/load_time*1000:.1f} KB/s")
                print()
            else:
                print(f"❌ {img_path} - HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ {img_path} - 错误: {e}")
    
    print(f"总大小: {total_size:.1f} KB")
    print(f"总加载时间: {total_time:.1f} ms")
    print(f"平均速度: {total_size/total_time*1000:.1f} KB/s")

def test_page_performance():
    """测试页面加载性能"""
    base_url = "http://localhost:8000"
    
    print("=== 页面加载性能测试 ===")
    
    try:
        start_time = time.time()
        response = requests.get(base_url)
        end_time = time.time()
        
        if response.status_code == 200:
            load_time = (end_time - start_time) * 1000
            size_kb = len(response.content) / 1024
            
            print(f"✅ 主页加载成功")
            print(f"   页面大小: {size_kb:.1f} KB")
            print(f"   加载时间: {load_time:.1f} ms")
            print(f"   速度: {size_kb/load_time*1000:.1f} KB/s")
            
            # 检查关键优化
            content = response.text
            optimizations = {
                "WebP支持": "webp" in content.lower(),
                "懒加载": "loading=" in content.lower(),
                "响应式图片": "picture>" in content,
                "性能监控": "performance" in content.lower()
            }
            
            print("\n=== 优化检查 ===")
            for opt, status in optimizations.items():
                status_icon = "✅" if status else "❌"
                print(f"{status_icon} {opt}")
                
        else:
            print(f"❌ 页面加载失败 - HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ 页面加载错误: {e}")

def compare_file_sizes():
    """比较文件大小优化效果"""
    print("=== 文件大小对比 ===")
    
    original_dir = "picture"
    optimized_dir = "picture/optimized"
    
    if not os.path.exists(optimized_dir):
        print("❌ 优化目录不存在，请先运行优化脚本")
        return
    
    total_original = 0
    total_optimized = 0
    
    for filename in os.listdir(original_dir):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            original_path = os.path.join(original_dir, filename)
            name, ext = os.path.splitext(filename)
            webp_path = os.path.join(optimized_dir, f"{name}.webp")
            
            if os.path.exists(original_path) and os.path.exists(webp_path):
                original_size = os.path.getsize(original_path) / 1024
                webp_size = os.path.getsize(webp_path) / 1024
                
                total_original += original_size
                total_optimized += webp_size
                
                reduction = (1 - webp_size/original_size) * 100
                
                print(f"{filename}: {original_size:.1f} KB → {webp_size:.1f} KB ({reduction:.1f}% 减少)")
    
    total_reduction = (1 - total_optimized/total_original) * 100
    print(f"\n总体优化: {total_original:.1f} KB → {total_optimized:.1f} KB ({total_reduction:.1f}% 减少)")

if __name__ == "__main__":
    print("🚀 开始性能测试...\n")
    
    # 检查服务器是否运行
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        if response.status_code != 200:
            print("❌ 本地服务器未运行，请先启动服务器")
            exit(1)
    except:
        print("❌ 无法连接到本地服务器，请确保服务器在 http://localhost:8000 运行")
        exit(1)
    
    compare_file_sizes()
    print()
    test_page_performance()
    print()
    test_image_performance()
    
    print("\n🎉 性能测试完成！")
