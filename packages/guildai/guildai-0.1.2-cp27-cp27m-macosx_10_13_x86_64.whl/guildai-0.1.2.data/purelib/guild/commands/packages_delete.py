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

import click

from guild import click_util

@click.command("delete, rm")
@click.argument("packages", metavar="PACKAGE...")
@click.option(
    "-y", "--yes",
    help="Do not prompt before deleting.",
    is_flag=True)

@click_util.use_args

def delete_packages(args):
    """Uninstall one or more packages.

    This command is equivalent to 'guild uninstall [options]
    PACKAGE...'.
    """
    from . import packages_impl
    packages_impl.uninstall_packages(args)
