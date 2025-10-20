#!/bin/bash

# 图片优化脚本
# 创建优化后的图片目录
mkdir -p picture/optimized

echo "开始优化图片..."

# 优化函数
optimize_image() {
    local input="$1"
    local filename=$(basename "$input")
    local name="${filename%.*}"
    local ext="${filename##*.}"
    
    echo "优化: $filename"
    
    # 1. 压缩原格式图片 (质量85%)
    convert "$input" -quality 85 -strip "picture/optimized/${name}_compressed.${ext}"
    
    # 2. 生成WebP格式 (质量80%)
    convert "$input" -quality 80 -strip "picture/optimized/${name}.webp"
    
    # 3. 生成缩略图 (200px宽度)
    convert "$input" -resize 200x -quality 80 -strip "picture/optimized/${name}_thumb.webp"
    
    # 4. 生成中等尺寸 (800px宽度)
    convert "$input" -resize 800x -quality 80 -strip "picture/optimized/${name}_medium.webp"
}

# 优化所有图片
for img in picture/*.{jpg,JPG,png,PNG}; do
    if [ -f "$img" ]; then
        optimize_image "$img"
    fi
done

echo "图片优化完成！"
echo "优化后的文件大小对比："

# 显示文件大小对比
echo "原文件 vs 优化后文件:"
for img in picture/*.{jpg,JPG,png,PNG}; do
    if [ -f "$img" ]; then
        filename=$(basename "$img")
        name="${filename%.*}"
        ext="${filename##*.}"
        
        original_size=$(ls -lh "$img" | awk '{print $5}')
        compressed_size=$(ls -lh "picture/optimized/${name}_compressed.${ext}" 2>/dev/null | awk '{print $5}' || echo "N/A")
        webp_size=$(ls -lh "picture/optimized/${name}.webp" 2>/dev/null | awk '{print $5}' || echo "N/A")
        
        echo "$filename: $original_size -> 压缩: $compressed_size, WebP: $webp_size"
    fi
done
