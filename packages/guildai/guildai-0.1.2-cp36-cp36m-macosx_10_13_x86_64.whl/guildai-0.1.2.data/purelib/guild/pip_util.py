# Copyright 2017 TensorHub, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division

from pip.commands.install import InstallCommand
from pip.utils import get_installed_distributions

class Distribution(object):

    def __init__(self, d):
        self._d = d

    def __str__(self):
        return str(self._d)

    @property
    def name(self):
        return self._d.project_name

    @property
    def version(self):
        return self._d.version

def install(reqs, index_urls=None, upgrade=False):
    cmd = InstallCommand()
    args = ["--user"]
    if upgrade:
        args.append("--upgrade")
    if index_urls:
        args.append("--index-url", index_urls[0])
        for url in index_urls[1:]:
            args.append("--extra-index-url", url)
    args.extend(reqs)
    cmd.run(*cmd.parse_args(args))

def get_installed():
    installed = get_installed_distributions(user_only=True)
    return [Distribution(d) for d in installed]
