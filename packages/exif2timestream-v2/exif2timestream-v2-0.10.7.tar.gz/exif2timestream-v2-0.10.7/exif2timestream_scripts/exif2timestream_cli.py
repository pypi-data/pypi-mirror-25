#!/usr/bin/env python3
import glob
import argparse
import datetime
import re
from libexif2timestream2.time import verbose_timedelta, str_to_datetime
from libexif2timestream2.process import process_timestream
from libexif2timestream2.image import detect_backends


class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith('r|'):
            return text[2:].splitlines()
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


parser = argparse.ArgumentParser(description="exif2timestream cli", formatter_class=SmartFormatter)

parser.add_argument('input', type=str, nargs="+",
                    help='Directory(s) containing unsorted images (from the same image source)')

parser.add_argument('-O', "--output-path", type=str,
                    help="Output directory, will create if nonexistent.",
                    default=".")

parser.add_argument('-n', '--name', type=str, required=True,
                    help='Name for the output timelapse')

parser.add_argument('-d', '--depth', type=int,
                    help="Recursion depth for input directory scanning.")


def parse_res(res_str):
    if res_str in ("orig", "original"):
        return None
    if "x" in res_str:
        return list(map(int, res_str.split("x")))
    if "," in res_str:
        return list(map(int, res_str.split(",")))


parser.add_argument('-r', '--resolutions', type=parse_res,
                    default=[], action='append',
                    help="Resolutions to resize to. (eg -r orig -r 1280x720 -r 1920x1080)")

parser.add_argument('-t', '--output-image-type',
                    choices=['jpeg', 'png', 'tif'], default=['jpeg'], action='append',
                    help="Output image type.")

parser.add_argument('-o', "--overwrite",
                    action='store_true', default=False,
                    help='Overwrite files that already exist.')

parser.add_argument('-rt', "--rotation",
                    choices=[0, 90, 180, 270],
                    help='Rotation in 90° increments. Storing 0 will remove the orientation flag.')
parser.add_argument('-p', "--pyramid",
                    action='store_true', default=False,
                    help='Create pyramidal tiffs.')

parser.add_argument('-ie', "--ignore-exif",
                    action='store_true', default=False,
                    help='Flag to totally ignore exif data and attempt to infer the timepoint exclusively from the filenames.')

archive_mode_help = """r|Archive Modes:
    copy:       leave source images in their original location.
    move:       remove source images after processing.
    archive:    create a new tarball of the source images
        (overwriting any previous ones) and leave the source
        images in their original place.
    archive-rm: create/append to a tarball and remove the source
        images after processing.    
"""

parser.add_argument('-am', '--archive-mode', choices=['archive', 'archive-rm', 'move', 'copy'],
                    default='copy',
                    help=archive_mode_help)

parser.add_argument('-ap', '--archive-path', type=str,
                    help="Archive tarball path to archive the originals in.")


def str_to_timedelta(st):
    suffix_dict = {
        "d": "days",
        "days": "days",
        "h": "hours",
        "hr": "hours",
        "hrs": "hours",
        "hour": "hours",
        "hours": "hours",
        "m": "minutes",
        "min": "minutes",
        "mins": "minutes",
        "minute": "minutes",
        "minutes": "minutes",
        's': "seconds",
        'sec': "seconds",
        'secs': "seconds",
        'second': "seconds",
        'seconds': "seconds",
        "ms": "milliseconds",
        "milliseconds": "milliseconds"
    }
    # regex: capture floating point with sign and word
    vals = re.match(r'^([-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?)(\w+)$', st)
    if not vals:
        raise argparse.ArgumentError()
    gs = vals.groups()
    if len(gs) != 2:
        raise argparse.ArgumentError()
    value, suffix = gs
    return datetime.timedelta(**{suffix_dict[suffix]: float(value)})


def dt_parse(st):
    try:
        return str_to_datetime(st, extra=("%Y_%m_%d_%H_%M_%S",))
    except:
        argparse.ArgumentError()


parser.add_argument('-s', '--start', type=dt_parse,
                    default=datetime.datetime.fromtimestamp(0),
                    help='Start datetime, year first day last (2012-01-01T12:10 is a good example) [default=1970-01-01T00:00:00]')

parser.add_argument('-e', '--end', type=dt_parse,
                    default=datetime.datetime.now(),
                    help='End datetime, year first & day last assumed. [default=now]')

parser.add_argument('-i', '--interval', type=str_to_timedelta,
                    default=datetime.timedelta(minutes=5),
                    help='Interval (suffix eg: 30s, 15m, 1h, 5d). [default=5m]')

parser.add_argument('-ts', '--time-shift', type=str_to_timedelta,
                    default=datetime.timedelta(0),
                    help='Time shift all images by a value (suffix and sign eg: -30s, +15m, 1h, -5d)')

parser.add_argument('-da', '--dont-align',
                    action='store_true', default=False,
                    help="Don't align any images to the interval. This will probably result in odd timestamps.")

parser.add_argument('-aw', '--align-window', type=str_to_timedelta,
                    default=datetime.timedelta(minutes=2),
                    help='The the amount of time aligning that is acceptable to match a timepoint (suffix eg: 30s, 2.5m 15m). [default=2m]')


args = parser.parse_args()


def main():
    detect_backends()
    print("Range {} to {}".format(args.start, args.end))
    if args.time_shift:
        print("Time shifting by {}".format(verbose_timedelta(args.time_shift)))
    sources = []

    for source in args.input:
        sources.extend(glob.glob(source))
    print("Sources: \n\t{}".format("\n\t".join(sources)))
    params = {
        "archive_mode": args.archive_mode,
        "archive_path": args.archive_path,
        "resolutions": args.resolutions,
        "extensions": args.output_image_type,
        "time_shift": args.time_shift,
        "pyramid": args.pyramid,
        "ignore_exif": args.ignore_exif,
        "rotation": args.rotation,
        "overwrite": args.overwrite
    }
    if args.depth:
        params['depth'] = args.depth

    process_timestream(args.name,
                       args.input,
                       args.output_path,
                       args.start,
                       args.end,
                       args.interval,
                       **params)


if __name__ == "__main__":
    main()
