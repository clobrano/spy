#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import os
import time
import threading
from s import run


@pytest.fixture
def setupFilesystemWatcher():
    thread = threading.Thread(
        target=run, name="spy/run", kwargs={"watch_dir": os.getcwd()}
    )
    thread.start()
    # give it a second to be ready to listen
    time.sleep(0.5)
    yield


@pytest.fixture
def setupCreateNewfile():
    open("newfile", "w")
    yield
    os.remove("newfile")


def test_spy_catch_events_from_the_directory(setupFilesystemWatcher, capfd):
    with open("newfile", "w"):
        pass
    time.sleep(1)
    out, err = capfd.readouterr()
    assert "newfile" in out
    os.remove("newfile")


def test_spy_catch_change_event_from_directory(
        setupFilesystemWatcher, setupCreateNewfile, capfd):
    with open("newfile", "w") as f:
        time.sleep(.5)
        f.write("new content")
    time.sleep(.5)
    out, err = capfd.readouterr()
    assert "changed" in out


def test_spy_run_command_on_create_event(capfd):
    thread = threading.Thread(
        target=run,
        name="spy/run",
        kwargs={
            "watch_dir": os.getcwd(),
            "on_create": "echo user command output"}
    )
    thread.start()
    # give it a second to be ready to listen
    time.sleep(1)
    with open("newfile", "w"):
        pass
    time.sleep(.5)
    out, err = capfd.readouterr()
    assert "user command output" in out
    time.sleep(.5)
    os.remove("newfile")


def test_spy_run_command_on_change_event_from_directory(setupCreateNewfile,
                                                        capfd):
    thread = threading.Thread(
        target=run,
        name="spy/run",
        kwargs={
            "watch_dir": os.getcwd(),
            "on_change": "echo user command output on change"}
    )
    thread.start()
    # give it a second to be ready to listen
    time.sleep(1)
    with open("newfile", "w") as f:
        time.sleep(.5)
        f.write("new content")
    time.sleep(1)
    out, err = capfd.readouterr()
    assert "user command output on change" in out
    os.remove("newfile")
