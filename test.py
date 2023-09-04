from PIL import Image, ImageDraw, ImageFont
import cv2
import glob
import numpy as np


images = []


def grayscaring():
    image_pil = Image.fromarray(frame)
    resize = image_pil.resize((170, 90), Image.LANCZOS)
    gray_img = resize.convert("L")
    img_dot_array = np.array(gray_img)
    norm_img_array = img_dot_array / 255
    lines = [0] * gray_img.size[1]
    for i in range(0, gray_img.size[1]):
        print(" ")
        for j in range(0, gray_img.size[0]):
            if norm_img_array[i, j] > 0.9:  # 明るさが0.9より上だったら#を割り当てる
                lines[i] = "@" if j == 0 else lines[i] + "@"
            elif norm_img_array[i, j] > 0.8:
                lines[i] = "n" if j == 0 else lines[i] + "n"
            elif norm_img_array[i, j] > 0.7:  # 明るさが0.7より上だったらkを割り当てる
                lines[i] = "k" if j == 0 else lines[i] + "k"
            elif norm_img_array[i, j] > 0.5:  # 明るさが0.5より上だったら>を割り当てる
                lines[i] = ">" if j == 0 else lines[i] + ">"
            elif norm_img_array[i, j] > 0.3:  # 明るさが0.3より上だったら'を割り当てる
                lines[i] = "'" if j == 0 else lines[i] + "'"
            elif norm_img_array[i, j] > 0.2:
                lines[i] = "l" if j == 0 else lines[i] + "l"
            else:
                lines[i] = " " if j == 0 else lines[i] + " "
    print("\033[H")
    font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf", 17)
    left, top, right, bottom = max(font.getbbox(line) for line in lines)
    w = abs(right - left)
    h = abs(top - bottom)
    img = Image.new("RGB", (w, h * len(lines)), "#000000")
    draw = ImageDraw.Draw(img)

    for i, line in enumerate(lines):
        # print(line)
        draw.text((0, i * h), line, fill="#ffffff")
    images.append(img)
    print("ok")
    images[0].save(
        "pillow_imagedraw.gif",
        save_all=True,
        append_images=images[1:],
        optimize=False,
        duration=100,
        loop=0,
    )


if __name__ == "__main__":
    cap = cv2.VideoCapture("zundamon10f.GIF")  # ここに好きなGIF画像や動画のpathを入力してください
    cap.set(cv2.CAP_PROP_FPS, 0.5)
    while cap.isOpened():
        flag, frame = cap.read()  # 動画を1フレームずつ読み込む
        if not flag:
            break
        grayscaring()
