import pytesseract
from PIL import Image
import cv2
import os

# 设置Tesseract的路径
os.environ['TESSDATA_PREFIX'] = r'D:\code\project\pkuAutoElective\Tesseract-OCR\tessdata'
pytesseract.pytesseract.tesseract_cmd = r'D:\code\project\pkuAutoElective\Tesseract-OCR\tesseract.exe'

# 设置只识别英文和数字
custom_config = r'--psm 8 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def recognize_captcha(image_path):
    # 加载验证码图片
    img = cv2.imread(image_path)
    
    # 图像预处理
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binarized_img = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY)
    
    # 使用Tesseract OCR识别图像中的文字，传递自定义的配置
    captcha_text = pytesseract.image_to_string(binarized_img, config=custom_config)
    return captcha_text.strip()

def main():
    # 测试前11张图片
    for i in range(1, 12):
        image_path = f'captcha/data/{i}.png'
        if os.path.exists(image_path):
            result = recognize_captcha(image_path)
            print(f"图片 {i}.png 识别结果：{result}")
        else:
            print(f"图片 {i}.png 不存在")

if __name__ == "__main__":
    main()
