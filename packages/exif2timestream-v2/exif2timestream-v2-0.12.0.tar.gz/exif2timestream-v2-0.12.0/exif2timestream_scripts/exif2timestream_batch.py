#!/usr/bin/env python3
import yaml
import argparse
import traceback
import datetime, re
from libexif2timestream2.time import verbose_timedelta, str_to_datetime, time_date_to_datetime
from libexif2timestream2.process import process_timestream

parser = argparse.ArgumentParser(description="exif2timestream batch")


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
        raise ValueError("Time delta couldnt be parsed")
    gs = vals.groups()
    if len(gs) != 2:
        raise ValueError()
    value, suffix = gs
    return datetime.timedelta(**{suffix_dict[suffix]: float(value)})


def dt_parse(st):
    try:
        return str_to_datetime(st, extra=("%Y_%m_%d_%H_%M_%S",))
    except:
        argparse.ArgumentError()


parser.add_argument('input', type=str,
                    help='yaml file for processing')

args = parser.parse_args()


def main():
    jobs = yaml.load(open(args.input))

    for name, job in jobs.items():
        try:
            print("Running {}".format(name))
            # print("Time shifting by {}".format(verbose_timedelta(args.time_shift)))
            params = {
                "archive_mode": job.get("archive_mode", "copy"),
                "archive_path": job.get("archive_path", None),
                "resolutions": job.get("output_resolutions", [None, [1920, 1080]]),
                "extensions": job.get("output_filetypes", ['jpeg']),
                "time_shift": str_to_timedelta(job.get("time_shift", "0m")),
                "pyramid": job.get("pyramid", False),
                "rotation": job.get("rotation", None),
                "ignore_exif": job.get("ignore_exif", False),
                "name_suffix": job.get("suffix", ""),
                "force_align": job.get("force_align", False)
            }
            if "depth" in job.keys():
                params['depth'] = job.get("depth", None)

            src, dest = job.get("source_directory", None), job.get("output_directory", None)
            if not src or not dest:
                print("No src or no dest")
            if isinstance(src, str):
                src = [src]
            start = job.get("start", None)
            if not start:
                print("No start, skipping...")
                continue

            start = str_to_datetime(start)
            end = str_to_datetime(job.get("end", "now"))
            interval = str_to_timedelta(job.get("interval", "5m"))

            process_timestream(name,
                               src,
                               dest,
                               start,
                               end,
                               interval,
                               **params)
        except Exception as e:
            traceback.print_exc()


if __name__ == "__main__":
    main()
