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
from . import runs_support

@click.command("info")
@click.argument("run", required=False)
@runs_support.run_scope_options
@runs_support.run_filters
@click.option("--env", help="Include run environment", is_flag=True)
@click.option("--flags", help="Include run flags", is_flag=True)
@click.option("--files", help="Include run files", is_flag=True)

@click.pass_context
@click_util.use_args

def run_info(ctx, args):
    """Show run details.

    RUN must be a run ID (or the start of a run ID that uniquely
    identifies a run) or a zero-based index corresponding to the run
    as it appears in the list of filtered runs.

    By default the latest run is selected (index 0).

    EXAMPLES

    Show info for the latest run in the current project:

        guild runs info

    Show info for the latest run system wide:

        guild runs info -S

    Show info for the latest completed run in the current project:

        guild runs info -c

    Show info for run a64b1710:

        guild runs info a64b1710

    """
    from . import runs_impl
    runs_impl.run_info(args, ctx)
