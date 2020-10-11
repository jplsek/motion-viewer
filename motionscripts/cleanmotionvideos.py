#!/usr/bin/env python3

import sys
import time
from functools import partial
from multiprocessing import Lock, Pool, Process, Value
from os import remove
from os.path import getsize
from pathlib import Path
from subprocess import run

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


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


def check_and_remove(file, dry_run, min_duration, with_dots=True):
    # use ffprobe to get the duration of the video
    proc = run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1', file],
               capture_output=True, text=True)

    stdout = proc.stdout.strip()

    if proc.returncode != 0:
        msg = ('Error running ffprobe: ' + stdout + proc.stderr).strip()
        printer.err(msg)
        return

    try:
        duration = float(stdout)
    except ValueError:
        printer.warn(f'{file} could not be parsed. Received "{stdout}" '
                     'instead of a number. Please check it manually.')
        return

    if duration < min_duration:
        msg = f'(duration: {duration}): {file}'
        if dry_run:
            printer.info(f'Would delete {msg}')
        else:
            try:
                remove(file)
                printer.info(f'Deleted {msg}')
            except PermissionError:
                printer.err(
                    f'Permission denied when trying to delete {msg}')
    elif with_dots:
        printer.info('.', newline=False)


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


def watch(dry_run=False, min_duration=2):
    target_dir = get_target_dir(Path('/'))

    def on_created(event):
        src = event.src_path
        if event.is_directory or not src.endswith('.mkv'):
            return

        def run():
            # a created file does not mean the file has been
            # completely made/copied
            # (this is to avoid the "End of file" error from ffprobe)
            cur_size = -1
            while (cur_size != getsize(src)):
                cur_size = getsize(src)
                time.sleep(1)

            check_and_remove(event.src_path, dry_run, min_duration, False)

        Process(target=run).start()

    event_handler = FileSystemEventHandler()
    event_handler.on_created = on_created

    observer = Observer()
    observer.schedule(event_handler, str(target_dir))
    observer.start()
    observer.join()


def clean(dry_run=False, root=Path('/'), min_duration=2):
    target_dir = get_target_dir(root)

    videos = Path(target_dir).glob('*.mkv')

    check_and_remove_default = partial(
        check_and_remove, dry_run=dry_run, min_duration=min_duration)

    with Pool() as p:
        p.map(check_and_remove_default, videos)

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