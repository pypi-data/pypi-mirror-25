#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import requests
from PyQt5 import QtCore

try:
    from . import frozen
except ImportError:
    frozen = False

UPDATE_URL = 'https://soft.snbl.eu/_sources/medved.rst.txt'
VERSION_PATTERN = '.. MEDVED Versions'


def pyqt2bool(entry):
    return not (entry == 'false' or not entry)


def get_hg_hash():
    if not get_hg_hash.hash:
        if hasattr(sys, 'frozen') or frozen:
            get_hg_hash.hash = frozen.hg_hash
        else:
            path = os.path.dirname(os.path.dirname(__file__))
            try:
                pipe = subprocess.Popen(['hg', 'id', '-i', '-R', path], stdout=subprocess.PIPE)
                get_hg_hash.hash = pipe.stdout.read().decode()
            except OSError:
                get_hg_hash.hash = 'unknown'
        get_hg_hash.hash = get_hg_hash.hash.strip()
    return get_hg_hash.hash


get_hg_hash.hash = ''


def get_version():
    if not get_version.version:
        if hasattr(sys, 'frozen') or frozen:
            get_version.version = frozen.version
        else:
            get_version.version = '0.0.0'
    return get_version.version


get_version.version = ''


class UpdateChecker(QtCore.QObject):
    sigNewVersion = QtCore.pyqtSignal(str, bool)
    sigFinished = QtCore.pyqtSignal()

    def check(self):
        try:
            r = requests.get(UPDATE_URL)
        except requests.RequestException as err:
            self.sigNewVersion.emit(str(err), True)
        else:
            self.parse(r.text)
        self.sigFinished.emit()

    def parse(self, text):
        version = get_version()
        strings = []
        put = False
        boldline = False
        first = True
        parsing = False
        for line in text.split('\n'):
            if not line:
                continue
            if line == VERSION_PATTERN:
                parsing = True
                continue
            if parsing:
                if line.startswith('..'):
                    continue
                items = line.split()
                try:
                    [int(i) for i in items[1].split('.')]
                except (IndexError, ValueError):
                    pass
                else:
                    put = items[1] > version
                    boldline = True
                if put:
                    line = line.strip()
                    line = line[line.index(" ") + 1:]
                    if boldline:
                        boldline = False
                        if not first:
                            strings.append('</ul>')
                        strings.append(f'<span style="font-weight: bold; color: red">{line}</span>'
                                       f'<ul style="list-style-type:disc">')
                    else:
                        strings.append(f'<li>{line}</li>')
                    first = False
        if strings:
            strings.append('</ul>')
        self.sigNewVersion.emit('\n'.join(strings), False)
