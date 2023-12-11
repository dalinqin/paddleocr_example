from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
import csv

img_path = str("c:\\aaa.jpg")

ocr = PaddleOCR(use_angle_cls=True, lang="ch")
result = ocr.ocr(img_path, cls=False, det=True, rec=True)

rows_with_y = {}

# 遍历OCR结果，将文本根据其Y坐标分组到不同的行
for item in result[0]:
    # 获取坐标和文本
    coords, (text, confidence) = item
    # 我们用Y坐标的平均值来确定文本可能属于的行
    y_coord = sum([point[1] for point in coords]) / 4
    # 用一定的阈值来判定是否为同一行，这里假设如果Y坐标差距小于等于10则认为是同一行
    threshold = 15
    found_row = False
    for row_y in rows_with_y.keys():
        if abs(row_y - y_coord) <= threshold:
            rows_with_y[row_y].append((text, coords[0][0]))  # 将文本和X坐标加入相应行
            found_row = True
            break
    if not found_row:
        rows_with_y[y_coord] = [(text, coords[0][0])]

# 现在我们有了按行分组的文本，我们需要按X坐标对每行的文本进行排序
sorted_rows = []
for y in sorted(rows_with_y.keys()):
    # 按X坐标对行内元素进行排序
    sorted_texts = sorted(rows_with_y[y], key=lambda x: x[1])
    # 提取文本内容
    sorted_row_texts = [text for text, _ in sorted_texts]
    # 将排序后的文本行加入到结果列表
    sorted_rows.append(sorted_row_texts)


csv_file_path = 'c:\\aaa.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    for row in sorted_rows:
        csvwriter.writerow(row)    




#直接存成pdf



from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
# conda install reportlab

width, height = 1270, 1980  

pdfmetrics.registerFont(TTFont('ChineseFont', 'c:\\STSong.ttf'))  


c = canvas.Canvas("c:\\output.pdf", pagesize=(width, height))

c.setFont("ChineseFont", 10)

for line in result[0]:
    x, y, text = line[0][0][0], line[0][0][1], line[1][0]
    c.drawString(x, height - y, text)  

c.save()

