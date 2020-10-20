#!/usr/bin/env python3

import sys
from functools import partial
from multiprocessing import Lock, Pool, Process, Value
from os import remove
from os.path import getsize, getmtime
from pathlib import Path
from subprocess import run
from time import sleep

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

gigabyte = 1_000_000_000


class Printer:
    """Keep track of newlines such that extra newlines are not created.

    For example:  Instead of:
      ...           ...
      Foo           Foo
      Bar
      .             Bar
                    .
    """
    # Value is required to share memory between processes
    has_newline = Value('b', True)

    # don't want dots apearing on the same line as proper text
    lock = Lock()

    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END = '\033[0m'

    def info(self, string, newline=True):
        with self.lock:
            if newline:
                if not self.has_newline.value:
                    string = '\n' + string
                string += '\n'
                self.has_newline.value = True
            else:
                self.has_newline.value = False

            sys.stdout.write(string)
            sys.stdout.flush()

    def err(self, string):
        self.info(self.ERROR + str(string) + self.END)

    def warn(self, string):
        self.info(self.WARNING + str(string) + self.END)


printer = Printer()


def remove_video(video, dry_run, msg=None):
    if not msg:
        msg = str(video)

    if dry_run:
        printer.info(f'Would delete {msg}')
        return True

    try:
        remove(video)
    except PermissionError:
        printer.err(
            f'Permission denied when trying to delete {msg}')
        return False

    printer.info(f'Deleted {msg}')
    return True


def check_and_remove(video, dry_run, min_duration, with_dots=True):
    # use ffprobe to get the duration of the video
    proc = run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1', video],
               capture_output=True, text=True)

    stdout = proc.stdout.strip()

    if proc.returncode != 0:
        msg = ('Error running ffprobe: ' + stdout + proc.stderr).strip()
        printer.err(msg)
        return False

    try:
        duration = float(stdout)
    except ValueError:
        printer.warn(f'{video} could not be parsed. Received "{stdout}" '
                     'instead of a number. Please check it manually.')
        return False

    if duration < min_duration:
        msg = f'(duration: {duration}): {video}'
        return remove_video(video, dry_run, msg)

    if with_dots:
        printer.info('.', newline=False)

    return False


def get_target_dir(root):
    # read target_dir from config
    try:
        with open(root / 'etc/motion/motion.conf') as f:
            for line in f:
                if line.startswith('target_dir'):
                    # get value, remove first slash, and newline char
                    return root / line.split(' ')[1][1:].strip()
    except FileNotFoundError as e:
        printer.err(e)
        sys.exit(1)


def get_dir_size(videos):
    return sum(f.stat().st_size for f in videos) / gigabyte


def get_video_size(video):
    return video.stat().st_size / gigabyte


def remove_old_videos(target_dir, dry_run, max_size):
    videos = list(get_videos(target_dir))
    dir_size = get_dir_size(videos)

    if dir_size < max_size:
        return

    printer.info(f'Directory is {dir_size:0.2f}GB and is greater than '
                 f'the max size of {max_size}GB, removing old files...')
    videos.sort(key=getmtime)

    for video in videos:
        size = get_video_size(video)
        msg = f'({dir_size:0.2f}GB/{max_size}GB): {video}'

        if not remove_video(video, dry_run, msg):
            break

        dir_size -= size

        if dir_size < max_size:
            break


def watch(dry_run=False, min_duration=2, max_size=50):
    target_dir = get_target_dir(Path('/'))

    def on_created(event):
        src = event.src_path
        if event.is_directory or not src.endswith('.mkv'):
            return

        def run():
            # a created file does not mean the file has been
            # completely made/copied
            # (this is to avoid the "End of file" error from ffprobe)
            sleep(1)
            cur_size = -1
            while cur_size != getsize(src):
                cur_size = getsize(src)
                sleep(1)

            # remove small files
            if check_and_remove(event.src_path, dry_run, min_duration, False):
                return

            # remove old files
            remove_old_videos(target_dir, dry_run, max_size)

        Process(target=run).start()

    event_handler = FileSystemEventHandler()
    event_handler.on_created = on_created

    observer = Observer()
    observer.schedule(event_handler, str(target_dir))
    observer.start()
    observer.join()


def get_videos(target_dir):
    return Path(target_dir).glob('*.mkv')


def remove_small_videos(target_dir, dry_run, min_duration):
    videos = get_videos(target_dir)

    # Remove small videos
    check_and_remove_default = partial(
        check_and_remove, dry_run=dry_run, min_duration=min_duration)

    with Pool() as p:
        p.map(check_and_remove_default, videos)


def clean(dry_run=False, root=Path('/'), min_duration=2, max_size=50):
    target_dir = get_target_dir(root)

    remove_small_videos(target_dir, dry_run, min_duration)

    remove_old_videos(target_dir, dry_run, max_size)

    printer.info('')


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Remove short videos.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-d', '--dry-run', action='store_true',
                        help='Show what files would be deleted')
    parser.add_argument('-w', '--watch', action='store_true',
                        help='Watch the directory for new files')
    parser.add_argument('-r', '--root', default=Path('/'), type=Path,
                        help='Set the root directory')
    parser.add_argument('-m', '--min-duration', default=2, type=int,
                        help='The minimum duration in seconds of the video '
                        'required to keep')
    parser.add_argument('-x', '--max-size', default=50, type=int,
                        help='The maximum size in gigabytes of total videos '
                        'to keep')

    args = parser.parse_args()
    args = vars(args)
    should_watch = args.pop('watch')

    if should_watch:
        # watchdog does not work with sshfs
        args.pop('root')
        watch(**args)
    else:
        clean(**args)


if __name__ == "__main__":
    main()
