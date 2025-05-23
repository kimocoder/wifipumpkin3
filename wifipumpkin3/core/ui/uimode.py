from __future__ import absolute_import
import urwid
from wifipumpkin3.core.utility.collection import SettingsINI
import wifipumpkin3.core.utility.constants as C
import threading

# This file is part of the wifipumpkin3 Open Source Project.
# wifipumpkin3 is licensed under the Apache 2.0.

# Copyright 2020 P0cL4bs Team - Marcos Bomfim (mh4x0f)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class WidgetBase(urwid.Frame):
    """
    common class for widgets
    """

    _conf = SettingsINI(C.CONFIG_INI)

    def __init__(self, *args, **kwargs):
        pass

    def setup_view(self):
        raise NotImplementedError

    def main(self):
        raise NotImplementedError

    def handleWindow(self, key):
        raise NotImplementedError

    def render_view(self):
        return self
