import fire
from PIL import Image, ImageOps


def add_border(input_image, output_image, border, color=255):
    img = Image.open(input_image)
    dpi = img.info['dpi']

    if isinstance(border, int) or isinstance(border, tuple):
        if border == 0:
            size = img.size
            # width > height
            if size[0] > size[1]:
                border = (dpi[0] // 4, dpi[0] // 2)
                bimg = ImageOps.expand(img, border=border, fill=color)
            else:
                border = (dpi[0] // 2, dpi[0] // 4)
                bimg = ImageOps.expand(img, border=border, fill=color)
        else:
            bimg = ImageOps.expand(img, border=border, fill=color)
    else:
        raise RuntimeError('Border is not an integer or tuple!')
    bimg.save(output_image)
    print(input_image + ' now has borders and was converted to .png')


if __name__ == '__main__':
    fire.Fire(add_border)
