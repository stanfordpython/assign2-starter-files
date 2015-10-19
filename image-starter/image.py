"""
Image manipulation library for CS 92SI: The Python Programming Language
@author sredmond
@date 10-19-15
"""
from PIL import Image
from pathlib import Path


def load_image(filename):
    with Image.open(filename, 'r') as image:
        image = image.convert('RGBA')
    return _swap_major(_unflatten(list(image.getdata()), image.width, image.height))


def save_image(data2D, filename):
    data2D = _swap_major(data2D)
    image = _to_image(data2D)
    image.save(filename, format='PNG')


def _swap_major(data2D):
    width, height = len(data2D[0]), len(data2D)
    columns = []
    for i in range(width):
        columns.append([data2D[j][i] for j in range(height)])
    return columns


def _flatten(data2D):
    data1D = []
    for row in data2D:
        data1D.extend(row)
    return data1D


def _unflatten(data1D, width, height):
    assert len(data1D) == width * height
    length = len(data1D)
    return [data1D[i:i+width] for i in range(0, length, width)]


def _to_image(data2D):
    size = len(data2D[0]), len(data2D)
    image = Image.new('RGBA', size)
    data1D = _flatten(data2D)
    image.putdata(data1D)
    return image


def show_image(data2D):
    data2D = _swap_major(data2D)
    image = _to_image(data2D)
    image.show()

def show_all_images(slc, *rest, buffer_width=1):
    width, height = len(slc), len(slc[0])
    slices = []
    slices += slc
    for chunk in rest:
        slices += [[(0, 0, 0, 0) for _ in range(height)] for _ in range(buffer_width)]
        slices += chunk
    show_image(slices)


class FileSystemException(Exception): pass


def files_in_directory(dirname):
    p = Path(dirname)
    if not p.is_dir():
        raise FileSystemException("`{dir}` is not a valid directory".format(dir=dirname))
    return [str(child) for child in p.iterdir() if child.is_file()]


__all__ = ['load_image', 'show_image', 'show_all_images', 'save_image', 'files_in_directory']
