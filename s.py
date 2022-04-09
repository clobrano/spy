#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vi: set ft=python :
"""Spy catches files changes and react with custom commands"""
from typing import Dict
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import argparse

DEBUG = False


def dbg(msg: str) -> None:
    if DEBUG:
        print(msg)


class Runner:
    map: Dict[str, str] = {}

    def __init__(
        self, on_create: str = None, on_change: str = None, on_remove: str = None
    ):
        self.map["created"] = on_create
        self.map["modified"] = on_change
        self.map["deleted"] = on_remove

    def run(self, event_type: str) -> int:
        cmd = self.map.get(event_type, None)
        if not cmd:
            return 0
        cp = subprocess.run(cmd, shell=True)
        return cp.returncode


class FileSystemHandler(FileSystemEventHandler):
    """Listen to filesystem changes and react with
    user provided commands"""

    def __init__(self, runner: Runner):
        self.runner = runner

    def on_any_event(self, event):
        if event.is_directory:
            return
        dbg(f"{event.src_path}")
        dbg(f"{event.event_type}")

        self.runner.run(event.event_type)
        if event.event_type == "created":
            dbg(f"{event.src_path} created")
        if event.event_type == "modified":
            dbg(f"{event.src_path} changed")
        if event.event_type == "deleted":
            dbg(f"{event.src_path} deleted")


def run(
    watch_dir: str = os.getcwd(),
    on_create: str = None,
    on_change: str = None,
    on_remove: str = None,
    recursive: bool = True,
    timeout: int = -1,
) -> None:
    runner = Runner(
        on_create=on_create,
        on_change=on_change,
        on_remove=on_remove
    )
    handler = FileSystemHandler(runner)
    observer = Observer()
    observer.schedule(handler, watch_dir, recursive)
    observer.start()
    if timeout == -1:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
    else:
        for _ in range(timeout):
            time.sleep(1)
        observer.stop()
    observer.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument(
        "--watch-dir", "-w", default=os.getcwd(), help="The directory to watch"
    )
    parser.add_argument(
        "--recursive", "-r", default=True,
        help="whether to watch the subdirectories"
    )
    parser.add_argument(
        "--on-create",
        help="command to execute when a file is created inside the directory",
    )
    parser.add_argument(
        "--on-change",
        help="command to execute on directory changes"
    )
    parser.add_argument(
        "--on-remove",
        help="command to execute when a file is deleted from the directory",
    )
    parser.add_argument(
        "--timeout",
        default=-1,
        help="timeout in seconds for Spy to watch the directory (-1 is infinite)",
    )
    args = parser.parse_args()

    run(args.watch_dir,
        args.on_create,
        args.on_change,
        args.on_remove,
        args.recursive,
        args.timeout)
