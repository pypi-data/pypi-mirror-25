from . import exif
from . import image
from . import time
from .directorydb import DirectoryDB
import traceback
# import shutil
import os
import sys
from .archiver import Archiver
from tqdm import tqdm

# USE_RAWKIT = False
# if not os.environ.get("NO_RAWKIT", False):
#     try:
#         from rawkit.raw import Raw
#         import tempfile
#         USE_RAWKIT = True
#     except:
#         pass

ts_top_structure = "{name}~{width}{suffix}"
ts_name_structure = ts_top_structure + "_{dt}.{ext}"


def dt_get(image_file_path, ignore_exif=False):
    """
    attempts to get a datetime object from an image using first exif data, and then the filename.

    :param image_file_path: image file path to get the datetime from
    :param ignore_exif: whether to use exif data for the image or not
    :return: datetime.datetime or None
    """

    if ignore_exif:
        return exif.dt_from_filename(image_file_path)
    return exif.dt_from_exif(image_file_path) or exif.dt_from_filename(image_file_path)


def get_top_name(name, resolution=None, name_suffix=""):
    if resolution is None or resolution in ['original', 'orig', 'source']:
        return ts_top_structure.format(name=name, width="fullres", suffix=name_suffix)
    return ts_top_structure.format(name=name, width=resolution[0], suffix=name_suffix)


def get_name(name, dt, extension, resolution=None, name_suffix=""):
    return ts_name_structure.format(
        name=name,
        dt=time.dt_to_filename(dt),
        width="fullres" if resolution is None else resolution[0],
        ext=extension,
        suffix=name_suffix)


def process_image(dt, src_path, output_directory, name, name_suffix, extensions, resolutions, rotation, pyramid):
    for res in resolutions:
        output_path = os.path.join(output_directory,
                                   get_top_name(name, resolution=res, name_suffix=name_suffix),
                                   time.dt_to_path(dt))
        os.makedirs(output_path, exist_ok=True)

        for ext in extensions:
            image_name = get_name(name, dt, extension=ext, resolution=res, name_suffix=name_suffix)
            image_path = os.path.join(output_path, image_name)

            image.resize(src_path,
                         image_path,
                         rotate=rotation,
                         size=res)

    if pyramid and not os.environ.get("FORCE_PIL", None):
        output_path = os.path.join(output_directory,
                                   get_top_name(name, name_suffix="-pyramid"),
                                   time.dt_to_path(dt))
        os.makedirs(output_path, exist_ok=True)

        image_name = get_name(name, dt, extension="tiff", name_suffix="-pyramid")
        image_path = os.path.join(output_path, image_name)

        image.pyramid(src_path,
                      image_path)


def process_timestream(name, source_directory, output_directory,
                       start, end, interval,
                       depth=None,
                       time_shift=None,
                       extensions=[".jpg"],
                       dont_align=False,
                       resolutions=[None, (1920, 1080)],
                       pyramid=None,
                       rotation=None,
                       ignore_exif=False,
                       archive_mode="archive",
                       archive_path=None,
                       name_suffix="",
                       force_align=False
                       ):
    if not name_suffix.startswith("-") and name_suffix != "":
        name_suffix = "-" + name_suffix

    if not resolutions:
        resolutions = [None]

    archiver = None
    if archive_mode in ("archive", 'archive-rm'):
        if archive_path is None:
            archive_path = os.path.join(output_directory,
                                        "{}-{}".format(name, "archive"))
        if not archive_path.endswith(".tar"):
            archive_path = archive_path + ".tar"
        archiver = Archiver(archive_path, append=archive_mode == "archive-rm")
        archiver.open()

    try:
        warned = False
        with DirectoryDB(source_directory, depth=depth) as db:
            progressbar = tqdm(total=len(db.keys()))
            for src_path in db.keys():
                try:
                    src_path = src_path.decode('utf-8')
                    dt = dt_get(src_path, ignore_exif=ignore_exif)
                    if not dt:
                        print("Couldnt get datetime for {}".format(os.path.basename(src_path)))
                        continue

                    if not start < dt < end:
                        if not warned:
                            print("OOR {}\t{} to {}".format(dt.isoformat(), start.isoformat(), end.isoformat()))
                            warned = True
                        continue
                    if warned:
                        print("INR {}\t{} to {}".format(dt.isoformat(), start.isoformat(), end.isoformat()))
                        warned = False

                    if archiver:
                        archiver += src_path
                    if force_align:
                        dt = time.round_time(dt, interval)
                    else:
                        if not dont_align:
                            dtn = time.round_time(dt, interval)

                            if (dtn - dt).total_seconds() > interval.total_seconds() / 2 and not force_align:
                                continue
                            else:
                                dt = dtn
                    if time_shift:
                        dt = dt + time_shift
                    # if src_path.lower().endswith((".cr2", '.nef')) and USE_RAWKIT:
                    #     with tempfile.NamedTemporaryFile(suffix=".tiff") as f, Raw(src_path) as rawfile:
                    #         rawfile.save(filename=f.name, filetype='tiff')
                    #         process_image(dt,
                    #                       f.name,
                    #                       output_directory,
                    #                       name, name_suffix,
                    #                       extensions, resolutions, rotation,
                    #                       pyramid)
                    # else:
                    process_image(dt,
                                  src_path,
                                  output_directory,
                                  name, name_suffix,
                                  extensions, resolutions, rotation,
                                  pyramid)

                    if archive_mode in ("move", "archive-rm"):
                        os.remove(src_path)
                except KeyboardInterrupt:
                    sys.exit(1)
                except Exception as e:
                    print("Unhandled Exception!")
                    traceback.print_exc()
                finally:
                    progressbar.update(1)
            progressbar.close()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    finally:
        if archiver:
            archiver.close()
