# Copyright 2017 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""Dialect definitions for djangolg."""

from __future__ import print_function
from __future__ import unicode_literals

import importlib

from djangolg import settings
from djangolg.dialects.base import BaseDialect

__all__ = ['available_dialects', 'get_dialect']

classes = []

for item in settings.DIALECTS:
    try:
        module_path, class_name = item.rsplit('.', 1)
        cls = getattr(importlib.import_module(module_path), class_name)
        if issubclass(cls, BaseDialect):
            classes.append(cls)
    except ImportError:  # pragma: no cover
        pass

__all__.extend(classes)


def available_dialects(output="map"):
    """Get available dialect classes."""
    if output == "map":
        return {d.name: d for d in classes}
    if output == "choices":
        return [(d.name, d.description) for d in classes]
    if output == "list":
        return [d.name for d in classes]
    else:
        raise ValueError("invalid output type: {0}".format(output))


def get_dialect(name=None):
    """Instantiate a dialect class by name."""
    return available_dialects(output="map")[name]()
