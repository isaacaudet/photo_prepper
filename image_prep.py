import fire
from PIL import Image, ImageOps
import cv2


def jpg_2_png(input_image, output_image):
    jpg_image = cv2.imread(input_image)
    cv2.imwrite(output_image, jpg_image)
    print(input_image + ' converted to png.')


def add_border(input_image, output_image, border, color=255):
    img = Image.open(input_image)
    try:
        dpi = img.info['dpi']
    except KeyError:
        dpi = (2400, 2400)
    if isinstance(border, int) or isinstance(border, tuple):
        if border == 0:
            size = img.size
            # width > height
            if size[0] > size[1]:
                border = (dpi[0] // 4, dpi[0] // 2)
                bimg = ImageOps.expand(img, border=border, fill='white')
            else:
                border = (dpi[0] // 2, dpi[0] // 4)
                bimg = ImageOps.expand(img, border=border, fill='white')
        else:
            bimg = ImageOps.expand(img, border=border, fill='white')
    else:
        raise RuntimeError('Border is not an integer or tuple!')
    bimg.save(output_image, dpi=dpi)
    print(input_image + ' has borders.')


if __name__ == '__main__':
    fire.Fire()

