from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import os

# PNG 图片所在文件夹
img_folder = r"C:\Users\Kong\Desktop\output_pages"
output_pdf = r"C:\Users\Kong\Desktop\final_output_with_margin.pdf"

# 获取图片列表并按顺序排序
img_files = sorted([f for f in os.listdir(img_folder) if f.endswith('.png')])

c = canvas.Canvas(output_pdf, pagesize=A4)
page_width, page_height = A4  # points

margin_ratio = 0.05  # 留白比例 5%
usable_width = page_width * (1 - margin_ratio * 2)
usable_height = page_height * (1 - margin_ratio * 2)

for img_file in img_files:
    img_path = os.path.join(img_folder, img_file)
    img = ImageReader(img_path)
    iw, ih = img.getSize()

    # 按比例缩放到 A4 可用区域
    scale = min(usable_width / iw, usable_height / ih)
    iw_scaled = iw * scale
    ih_scaled = ih * scale

    # 居中放置
    x = (page_width - iw_scaled) / 2
    y = (page_height - ih_scaled) / 2

    c.drawImage(img, x, y, width=iw_scaled, height=ih_scaled)
    c.showPage()  # 新的一页

c.save()
print("PDF 已生成（带留白）:", output_pdf)
