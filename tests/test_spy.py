#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest
import os
import time
import threading
from spy.s import main, DEBUG


@pytest.fixture
def setupFilesystemWatcher():
    thread = threading.Thread(
        target=main,
        name="spy/run",
        kwargs={"watch_dir": os.getcwd(), "timeout": 3}
    )
    thread.start()
    # give it a second to be ready to listen
    time.sleep(0.5)
    yield


@pytest.fixture
def setupCreateNewfile():
    open("newfile.txt", "w")
    yield
    os.remove("newfile.txt")


@pytest.mark.skipif(not DEBUG, reason="This needs debug logs to pass")
def test_spy_catch_events_from_the_directory(setupFilesystemWatcher, capfd):
    with open("newfile.txt", "w"):
        pass
    time.sleep(1)
    out, err = capfd.readouterr()
    assert "newfile.txt" in out
    os.remove("newfile.txt")


@pytest.mark.skipif(not DEBUG, reason="This needs debug logs to pass")
def test_spy_catch_change_event_from_directory(
        setupFilesystemWatcher, setupCreateNewfile, capfd):
    with open("newfile.txt", "w") as f:
        time.sleep(.5)
        f.write("new content")
    time.sleep(.5)
    out, err = capfd.readouterr()
    assert "changed" in out


def test_spy_run_command_on_create_event(capfd):
    thread = threading.Thread(
        target=main,
        name="spy/run",
        kwargs={
            "watch_dir": os.getcwd(),
            "on_create": "echo user command output",
            "timeout": 3}
    )
    thread.start()
    # give it a second to be ready to listen
    time.sleep(1)
    with open("newfile.txt", "w"):
        pass
    time.sleep(.5)
    out, err = capfd.readouterr()
    assert "user command output" in out
    time.sleep(.5)
    os.remove("newfile.txt")


def test_spy_run_command_on_change_event_from_directory(setupCreateNewfile,
                                                        capfd):
    thread = threading.Thread(
        target=main,
        name="spy/run",
        kwargs={
            "watch_dir": os.getcwd(),
            "on_change": "echo user command output on change",
            "timeout": 3}
    )
    thread.start()
    # give it a second to be ready to listen
    time.sleep(1)
    with open("newfile.txt", "w") as f:
        time.sleep(.5)
        f.write("new content")
    time.sleep(1)
    out, err = capfd.readouterr()
    assert "user command output on change" in out


def test_spy_can_use_event_path_on_event(capfd):
    thread = threading.Thread(
        target=main,
        name="spy/run",
        kwargs={
            "watch_dir": os.getcwd(),
            "on_create": "echo event path is {path}",
            "timeout": 3}
    )
    thread.start()
    # give it a second to be ready to listen
    time.sleep(1)
    with open("newfile.txt", "w"):
        pass
    time.sleep(.5)
    out, err = capfd.readouterr()
    assert f"event path is {os.getcwd()}/newfile.txt" in out
    time.sleep(.5)
    os.remove("newfile.txt")


def test_spy_can_listen_events_on_some_extensions_only(capfd):
    thread = threading.Thread(
        target=main,
        name="spy/run",
        kwargs={
            "watch_dir": os.getcwd(),
            "on_create": "echo user command output",
            "timeout": 3,
            "extensions": [".txt"]}
    )
    thread.start()
    # give it a second to be ready to listen
    time.sleep(1)
    with open("newfile.txt", "w"):
        pass
    time.sleep(.5)
    out, err = capfd.readouterr()
    assert "user command output" in out
    time.sleep(.5)
    os.remove("newfile.txt")

def test_spy_ignores_events_if_file_does_not_have_listen_extension(capfd):
    thread = threading.Thread(
        target=main,
        name="spy/run",
        kwargs={
            "watch_dir": os.getcwd(),
            "on_create": "echo user command output",
            "timeout": 3,
            "extensions": [".py"]}
    )
    thread.start()
    # give it a second to be ready to listen
    time.sleep(1)
    with open("newfile.txt", "w"):
        pass
    time.sleep(.5)
    out, err = capfd.readouterr()
    assert "" in out
    time.sleep(.5)
    os.remove("newfile.txt")

