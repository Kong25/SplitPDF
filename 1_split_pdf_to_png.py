import fitz
from PIL import Image
import os

input_pdf = r"C:\Users\Kong\Desktop\test_file.pdf"
output_folder = r"C:\Users\Kong\Desktop\output_pages"
os.makedirs(output_folder, exist_ok=True)

zoom = 3.0
mat = fitz.Matrix(zoom, zoom)
rotate_bottom = True

# 每页的中心分界点 (x_split, y_split)，你可以填入9页的点
# 这里举例前两页，依次添加到第9页
split_points = [
    (297, 585),  # 第1页
    (297, 520),  # 第2页
    (297, 490),  # 第3页
    (297, 500),  # 第4页
    (297, 580),  # 第5页
    (297, 520),  # 第6页
    (297, 530),  # 第7页
    (297, 520),  # 第8页
    (297, 540),  # 第9页
]

doc = fitz.open(input_pdf)

for page_index, page in enumerate(doc):
    if page_index >= len(split_points):
        print(f"第 {page_index+1} 页没有分界点，跳过")
        continue

    x_split, y_split = split_points[page_index]
    page_width = page.rect.width
    page_height = page.rect.height

    # 根据分界点生成三个区域
    crop_areas = {
        "1_top_left": (0, 0, x_split, y_split),
        "2_top_right": (x_split, 0, page_width, y_split),
        "3_bottom": (0, y_split, page_width, page_height)
    }

    for region_name, rect_vals in crop_areas.items():
        rect = fitz.Rect(rect_vals)
        pix = page.get_pixmap(matrix=mat, clip=rect)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        if region_name == "3_bottom" and rotate_bottom:
            img = img.rotate(90, expand=True)

        output_path = os.path.join(output_folder, f"page{page_index+1}_{region_name}.png")
        img.save(output_path, dpi=(300,300))

print("PDF裁剪完成，输出在:", output_folder)
