# -*- coding: utf-8 -*-

# Copyright 2016 Yowza Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""

:author: Zohar Rimon
"""


import os
from os.path import isdir, isfile, join
import shutil

import pytest

from . import proto
from ..buildcontext import BuildContext
from ..graph import populate_targets_graph, topological_sort
from ..utils import yprint


slow = pytest.mark.skipif(not pytest.config.getoption('--with-slow'),
                          reason='need --with-slow option to run')


def clear_output():
    try:
        shutil.rmtree('build')
    except FileNotFoundError:
        pass


@slow
@pytest.mark.usefixtures('in_custominstest_project')
def test_proto_builder(basic_conf):
    print('XXXX')
