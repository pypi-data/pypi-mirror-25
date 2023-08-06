import piexif
from . import time
import os


def dt_get(image_file_path, ignore_exif=False):
    """
    attempts to get a datetime object from an image using first exif data, and then the filename.

    :param image_file_path: image file path to get the datetime from
    :param ignore_exif: whether to use exif data for the image or not
    :return: datetime.datetime or None
    """

    if ignore_exif:
        return dt_from_filename(image_file_path)

    v = dt_from_exif(image_file_path) or dt_from_filename(image_file_path)

    if v is None:
        print("Couldnt get datetime from: {}".format(image_file_path))
    return v


def transplant_exif(from_file, to_file):
    """
    Transplants exif from one image to another

    :param from_file: file to grab exif data from
    :param to_file: file to transfer exif to.
    """
    # exif = piexif.load(from_file)
    piexif.transplant(from_file, to_file)
    #
    # exif_source = pexif.JpegFile.fromFile(from_file)
    # exif_dest = pexif.JpegFile.fromFile(to_file)
    # print(exif_source.exif.primary.ExtendedEXIF.DateTimeOriginal)
    # exif_dest.exif.primary.ExtendedEXIF.DateTimeOriginal = exif_source.exif.primary.ExtendedEXIF.DateTimeOriginal
    # exif_dest.exif.primary.Orientation = exif_source.exif.primary.Orientation
    # print(exif_source.exif.primary.Orientation)
    # exif_dest.writeFile(to_file)


def dt_from_filename(filename, split_char='-'):
    """
    gets a datetime object from a filename.

    Splits at the last `split_char` character (excluding the extension)
     to extract as much relevant timestamp information

    if the string doesnt contain `split_char` attempts to get a datetime from the full name (minus the extension)

    If a datetime cannot be extracted, None is returned

    :param filename: filename to get a datetime from
    :param split_char: character to split at (default '-')
    :return: datetime object as indicated by the filenames last chunk
    :rtype: datetime.datetime or None
    """

    try:
        fn, ext = os.path.splitext(os.path.basename(filename))
        dt_str_chunk = fn.rsplit("-", 1)[-1]
        dt_str_chunk = dt_str_chunk[-19:]
        return time.str_to_datetime(dt_str_chunk, time.ts_possible_timestamp_formats)
    except:
        return None


def dt_from_exif(from_file):
    """
    attempts to get a datetime from the exif on an image.

    :param from_file: filename to get the exif datetime from
    :return: None or a datetime object from the exif.
    """
    try:
        exif = piexif.load(from_file)
        dtoriginal = exif['Exif'].get(piexif.ExifIFD.DateTimeOriginal).decode("utf-8")
        return time.str_to_datetime(dtoriginal.replace(":", ""))
    except:
        return None


class ExifContext(object):
    def __init__(self, image_file, destination=None):
        self.image_file = image_file
        self.destination = image_file if destination is None else destination
        self.exif = None

    def transplant(self):
        piexif.transplant(self.image_file, self.destination)

    def set_orientation_0(self):
        if piexif.ImageIFD.Orientation in self.exif["0th"]:
            self.exif["0th"].pop(piexif.ImageIFD.Orientation)

    def __enter__(self):
        self.exif = piexif.load(self.image_file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        piexif.remove(self.destination)
        piexif.insert(piexif.dump(self.exif), self.destination)
