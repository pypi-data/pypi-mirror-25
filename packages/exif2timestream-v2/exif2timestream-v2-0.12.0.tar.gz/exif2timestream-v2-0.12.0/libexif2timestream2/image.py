import traceback
import warnings
import sys
import os
from . import exif

AVAILABLE_LIBRARIES = []
USE_VIPS = False
os.environ['VIPS_WARNING'] = "0"

if not os.environ.get("FORCE_PIL", None):
    try:
        import gi
        gi.require_version("Vips", '8.0')
        from gi.repository import Vips

        Vips.cache_set_max(10)

        USE_VIPS = True
    except:
        traceback.print_exc()
        warnings.warn("Unable to import Vips", ImportWarning)

if os.environ.get("USE_RAWKIT", False):
    try:
        from rawkit.raw import Raw
        import tempfile

        USE_RAWKIT = True
    except:
        pass

try:
    from PIL import Image
except:
    traceback.print_exc()
    warnings.warn("Unable to import pil", ImportWarning)


def detect_backends():
    backends = []
    try:
        import gi
        gi.require_version("Vips", '8.0')
        from gi.repository import Vips
        backends.append("vips {}".format(Vips.version_string()))
    except:
        traceback.print_exc()
        warnings.warn("Unable to import Vips", ImportWarning)
    try:
        from PIL import Image
        import PIL
        backends.append("Pillow {}".format(PIL.__version__))
    except:
        traceback.print_exc()
        warnings.warn("Unable to import pil", ImportWarning)
    print("{} available backends".format(len(backends)))
    for b in backends:
        print("\t{}".format(b))


def _remove_magickload_temp():
    # for some bizarre reason, vips magickload will leave temporary files here.
    for f in os.scandir("."):
        if f.name.startswith("magick-"):
            os.remove(f)


def fix_vips_cache():
    Vips.cache_drop_all()


def _resize_vips(input_path, output_path, size=(1920, 1080), rotate=None,
                 preserve_aspect=True, progress_callback=None):
    """
    Resizes an image with vips.
    preserves output by default, default size target is 1920x1080.

    :param input_path: input image path
    :type input_path: str
    :param output_path: output image path, anything residing here will be removed.
    :type output_path: str
    :param size: target size of image (default=(1920, 1080)
    :type size: tuple or list
    :param preserve_aspect: whether to preserve the aspect ratio of the image or not (default=True)
    :type preserve_aspect: bool
    :param progress_callback: callback for progress, will be `callback(progress_percent, eta_seconds)`
    """
    access = Vips.Access.SEQUENTIAL
    if rotate is None:
        access = Vips.Access.SEQUENTIAL

    if input_path.lower().endswith((".cr2", '.nef')):
        # reading cr2/nef doesnt work well with new_from_file, use magickload instead
        vips_image = Vips.Image().magickload(input_path, access=access)
    else:
        vips_image = Vips.Image().new_from_file(input_path, access=access)

    if progress_callback is not None:
        vips_image.set_progress(True)

        def callback(vimage, progress_pointer):
            progress_callback(vimage.time.percent, vimage.time.eta)

        vips_image.connect('eval', callback)

    if rotate is not None:
        vips_image.remove(Vips.META_ORIENTATION)
        vips_image = vips_image.rot(rotate // 90)

    if not size is None and not size in ['original', 'orig', 'source']:
        hscale = float(size[0]) / float(vips_image.width)
        vscale = float(size[1]) / float(vips_image.height)
        if hscale != vscale and not preserve_aspect:
            warnings.warn("Aspect ratio mismatch and not preserving aspect, h{} v{}".format(hscale, vscale),
                          RuntimeWarning)
        if not preserve_aspect:
            vips_image = vips_image.resize(hscale, vscale=vscale)
        else:
            vips_image = vips_image.resize(hscale)

    vips_image.write_to_file(output_path)
    # _remove_magickload_temp()


def _resize_pil(input_path, output_path, size=(1920, 1080), rotate=None, preserve_aspect=True):
    """
    resizes an image using PIL, also rotates the image and sets the orientation to 0

    :param input_path:
    :param output_path:
    :param size:
    :param rotate:
    :param preserve_aspect:
    :return:
    """
    with exif.ExifContext(input_path, destination=output_path) as ex:
        image = Image.open(input_path)

        if not size is None and not size in ['original', 'orig', 'source']:
            if preserve_aspect:
                size = (size[0], (size[0] / image.size[0]) * image.size[1])
            image = image.resize(list(map(int, size)), resample=Image.LANCZOS)

        if rotate is not None:
            if rotate != 0:
                image = image.rotate(int((rotate // 90) * 90), expand=1)
            ex.set_orientation_0()
        image.save(output_path)


def _resize_rawkit(input_path, output_path, size=(1920, 1080), rotate=None,
                   preserve_aspect=True, progress_callback=None):
    with tempfile.NamedTemporaryFile(suffix=".tiff") as f, Raw(input_path) as rawfile:
        rawfile.save(filename=f.name, filetype='tiff')
        if USE_VIPS:
            _resize_vips(f.name, output_path, size=size,
                         preserve_aspect=preserve_aspect,
                         rotate=rotate,
                         progress_callback=progress_callback)
        else:
            _resize_pil(f.name, output_path, size=size,
                        rotate=rotate,
                        preserve_aspect=preserve_aspect)


def resize(input_path, output_path, size=(1920, 1080), rotate=None,
           preserve_aspect=True, progress_callback=None):
    """
    Exposed resize function.
    will call the right function to resize an image

    :param input_path: input image path
    :type input_path: str
    :param output_path: output image path, anything residing here will be removed.
    :type output_path: str
    :param size: target size of image (default=(1920, 1080)
    :type size: tuple or list
    :param rotate: rotation to apply to the image, choice of None, 0 90, 180, 270
    :type rotate: int (0, 90, 180, 270)
    :param preserve_aspect: whether to preserve the aspect ratio of the image or not (default=True)
    :type preserve_aspect: bool
    :param progress_callback: callback for progress, will be `callback(progress_percent, eta_seconds)`
    only available if vips
    """

    if USE_VIPS:
        _resize_vips(input_path, output_path, size=size,
                     preserve_aspect=preserve_aspect,
                     rotate=rotate,
                     progress_callback=progress_callback)
    else:
        _resize_pil(input_path, output_path, size=size,
                    rotate=rotate,
                    preserve_aspect=preserve_aspect)


def pyramid(input_path, output_path, tile_params=None, progress_callback=None):
    """
    turns an image into a pyramidal tiff
    sensible convert params are already set:
    {
        compression: "lzw",
        tile_width: 256,
        tile_height: 256,
    }

    :param input_path:
    :param output_path:
    :param size:
    :param tile_params: dict of parameters for the pyramidal transform. 
    :param progress_callback: callback for progress, will be `callback(progress_percent, eta_seconds)`
    """
    params = dict(
        tile_width=256,
        tile_height=256,
        compression='lzw'
    )
    if type(tile_params) is dict:
        params.update(tile_params)

    params['tile'] = True
    params['pyramid'] = True

    vips_image = Vips.Image().new_from_file(input_path)
    if progress_callback is not None:
        vips_image.set_progress(True)

        def callback(vimage, progress_pointer):
            progress_callback(vimage.time.percent, vimage.time.eta)

        vips_image.connect('eval', callback)

    vips_image.write_to_file(output_path, **params)
