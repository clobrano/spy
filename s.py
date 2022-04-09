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


class Runner:
    map: Dict[str, str] = {}

    def __init__(self,
                 on_create: str = None,
                 on_change: str = None,
                 on_remove: str = None):
        self.map["created"] = on_create
        self.map["modified"] = on_change
        self.map["removed"] = on_remove

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
        print(f"{event.src_path}")

        print(f"{self.runner.run(event.event_type)}")
        if event.event_type == "created":
            print(f"{event.src_path} created")
        if event.event_type == "modified":
            print(f"{event.src_path} changed")
        if event.event_type == "removed":
            print(f"{event.src_path} removed")


def run(watch_dir: str = os.getcwd(),
        on_create: str = None,
        on_change: str = None,
        on_remove: str = None) -> None:
    runner = Runner(on_create=on_create,
                    on_change=on_change,
                    on_remove=on_remove)
    handler = FileSystemHandler(runner)
    observer = Observer()
    observer.schedule(handler, watch_dir)
    observer.start()
    for _ in range(3):
        time.sleep(1)
    observer.stop()
    observer.join()


if __name__ == "__main__":
    run()
