import fire
from PIL import Image, ImageOps
import cv2
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def jpg_2_png(input_image, output_image):
    jpg_image = cv2.imread(input_image)
    cv2.imwrite(output_image, jpg_image)
    print(input_image + ' converted to png.')


def add_border(input_image, output_image, border, color=255):
    img = Image.open(input_image)
    try:
        dpi = img.info['dpi']
    except KeyError:
        dpi = (72, 72)

    if isinstance(border, int) or isinstance(border, tuple):
        if border == 0:
            size = img.size
            # width > height
            print(size[0])
            print(size[1])

            if size[0] > size[1]:
                border = (dpi[0], ((size[0] + dpi[1] * 2) - size[1])//2)
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


def upload(file_name):
    gauth = GoogleAuth()

    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()

    gauth.SaveCredentialsFile("mycreds.txt")
    drive = GoogleDrive(gauth)

    sub = '.jpg'
    png = file_name.replace(sub, '.png')
    jpg_2_png(file_name, png)
    border = png.replace('.png', '_border.png')
    add_border(png, border, 0)

    file1 = drive.CreateFile(
        {'parents': [{'id': '1UDkzbjnfLT4q9VS3i2EWnNdHkVYzOiUm'}]})
    file1.SetContentFile(border)
    file1.Upload()
    print(border + ' uploaded!')


if __name__ == '__main__':
    fire.Fire()
