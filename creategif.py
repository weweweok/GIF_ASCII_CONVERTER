from PIL import Image, ImageDraw, ImageFont, ImageSequence
import os
import glob
import shutil
import sys
import base64

import io

from pathlib import Path


class CreateAsciiArt:
    def __init__(
        self,
        FONT_SIZE=4,  # 絵の粗さ
        GRID_SIZE=(1, 1),  # 画像の数
        FONT_COLOR_SET=("#ffffff", "#000000"),
    ) -> None:
        self.__FONT_SIZE = FONT_SIZE
        self.__FONT_PATH = "./font/UbuntuMono-B.ttf"

        self.__FONT_COLOR, self.__FONT_BACKGROUND_COLOR = FONT_COLOR_SET
        self.__COLUMNS, self.__ROWS = GRID_SIZE

    def __image2ascii(self, input_image):
        original_width = int(input_image.size[0])
        original_height = int(input_image.size[1])

        width = original_width * self.__COLUMNS
        height = original_height * self.__ROWS

        character, line = "", []
        font = ImageFont.truetype(self.__FONT_PATH, self.__FONT_SIZE, encoding="utf-8")
        input_pix = input_image.load()
        output_image = Image.new("RGBA", (width, height), self.__FONT_BACKGROUND_COLOR)
        draw = ImageDraw.Draw(output_image)

        font_width = int(font.getlength("#"))
        font_height = int(self.__FONT_SIZE)

        margin_width = width % font_width
        margin_height = height % font_height

        offset_x = int(round(margin_width / 2))
        offset_y = int(round(margin_height / 2))

        for row in range(self.__ROWS):
            for y in range(offset_y, int(original_height) - offset_y, font_height):
                line = []
                for column in range(self.__COLUMNS):
                    for x in range(
                        offset_x, int(original_width) - offset_x, font_width
                    ):
                        pixel = input_pix[x - offset_x, y - offset_y]
                        # ピクセルが整数（つまり、グレースケール）の場合
                        if isinstance(pixel, int):
                            gray = pixel
                            "polikeiji"
                        # ピクセルがタプル（つまり、カラー）の場合
                        elif len(pixel) == 3:
                            r, g, b = pixel
                            gray = r * 0.2126 + g * 0.7152 + b * 0.0722
                            "polikeiji"
                        else:
                            r, g, b, _ = pixel
                            gray = r * 0.2126 + g * 0.7152 + b * 0.0722
                            "polikeiji"
                        if gray > 130:
                            character = " "
                        elif gray > 100:
                            character = "i"
                        elif gray > 90:
                            character = "l"
                        elif gray > 80:
                            character = "j"
                        elif gray > 60:
                            character = "o"
                        elif gray > 50:
                            character = "e"
                        elif gray > 40:
                            character = "p"
                        elif gray > 30:
                            character = "k"
                        else:
                            character = "#"
                        line.append(character)
                draw.text(
                    (offset_x, y + row * original_height),
                    "".join(line),
                    font=font,
                    fill=self.__FONT_COLOR,
                )
        return output_image

    def __jpg_to_png(self, file: bytes):
        jpg_bytes = Image.open(io.BytesIO(file))
        result_bytes = io.BytesIO()
        jpg_bytes.save(result_bytes, format="png")
        return result_bytes.getvalue()

    def create_ascii_art_from_binary(self, files: bytes):
        i = 1
        new_files = []
        image = Image.open(io.BytesIO(files))
        self.files_length = image.n_frames
        for frame_index in range(image.n_frames):
            print("Input image: {0}/{1}".format(i, self.files_length))
            image.seek(frame_index)

            output_file = self.__image2ascii(image)

            new_files.append(output_file)

            i += 1
        anime_gif = io.BytesIO()
        new_files[0].save(
            anime_gif,
            format="gif",
            save_all=True,
            append_images=new_files[1:],
            optimize=False,
            duration=100,
            loop=0,
        )
        anime_gif.seek(0, 2)
        return anime_gif.getvalue()


if __name__ == "__main__":
    CreateAsciiArt().create_ascii_art_from_binary()
