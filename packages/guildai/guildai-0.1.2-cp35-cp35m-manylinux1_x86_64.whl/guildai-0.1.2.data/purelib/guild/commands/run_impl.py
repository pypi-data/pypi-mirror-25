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

import guild.cli
import guild.cmd_support
import guild.op
import guild.project

DEFAULT_PROJECT_LOCATION = "."

def main(args):
    model_name, op_name = _parse_opspec(args.opspec)
    model = _resolve_model(model_name, args)
    project_op = _resolve_op(op_name, model)
    _apply_flags_to_op(args, project_op)
    _apply_disable_plugins(args, project_op)
    op = guild.op.from_project_op(project_op)
    if args.print_cmd:
        _print_op_command(op)
    elif args.print_env:
        _print_op_env(op)
    else:
        if args.yes or _confirm_op(op):
            result = op.run()
            _handle_run_result(result)

def _parse_opspec(spec):
    parts = spec.split(":", 1)
    if len(parts) == 1:
        return None, parts[0]
    else:
        return parts

def _resolve_model(name, args):
    project = _project_for_args(args)
    if name is None:
        return _project_default_model(project)
    else:
        return _project_model(name, project)

def _project_for_args(args):
    location = args.project_location or DEFAULT_PROJECT_LOCATION
    try:
        return guild.project.from_file_or_dir(location)
    except guild.project.NoModels:
        _missing_source_error(args.project_location)

def _missing_source_error(location):
    guild.cli.error(
        "%s does not contain any models\n"
        "Try a different location or 'guild run --help' "
        "for more information."
        % guild.cmd_support.project_location_desc(location))

def _project_required_error():
    guild.cli.error(
        "cannot find a model for this operation\n"
        "Try specifying a project, a package or 'guild run --help' "
        "for more information.")

def _project_default_model(project):
    default = project.default_model()
    if default:
        return default
    else:
        _no_models_for_project_error(project)

def _no_models_for_project_error(project):
    guild.cli.error("%s does not define any models" % project.src)

def _project_model(name, project):
    try:
        return project[name]
    except KeyError:
        _no_such_model_error(name, project)

def _no_such_model_error(name, project):
    guild.cli.error(
        "model '%s' is not defined in %s\n"
        "Try 'guild models%s' for a list of available models."
        % (name,
           guild.cmd_support.project_location_desc(project.src),
           _project_opt(project.src)))

def _project_opt(project_src):
    location = guild.cmd_support.project_location_option(project_src)
    return " -p %s" % location if location else ""

def _resolve_op(name, model):
    op = model.get_op(name)
    if op is None:
        _no_such_operation_error(name, model)
    return op

def _no_such_operation_error(name, model):
    guild.cli.error(
        "operation '%s' is not defined for model '%s'\n"
        "Try 'guild operations %s%s' for a list of available operations."
        % (name, model.name, model.name, _project_opt(model.project.src)))

def _apply_flags_to_op(args, op):
    for arg in args.args:
        name, val = _parse_flag(arg)
        op.flags[name] = val

def _parse_flag(s):
    parts = s.split("=", 1)
    if len(parts) == 1:
        return parts[0], None
    else:
        return parts

def _apply_disable_plugins(args, op):
    if args.disable_plugins:
        op.disabled_plugins.extend([
            name.strip() for name in args.disable_plugins.split(",")
        ])

def _print_op_command(op):
    formatted = " ".join([_maybe_quote_arg(arg) for arg in op.cmd_args])
    guild.cli.out(formatted)

def _maybe_quote_arg(arg):
    return '"%s"' % arg if " " in arg else arg

def _print_op_env(op):
    for name, val in sorted(op.cmd_env.items()):
        guild.cli.out("export %s=%s" % (name, val))

def _confirm_op(op):
    flags = _op_flags(op)
    if flags:
        prompt = (
            "You are about to run %s with the following flags:\n"
            "%s\n"
            "Continue?"
            % (op.name, _format_op_flags(flags)))
    else:
        prompt = (
            "You are about to run %s\n"
            "Continue?" % op.name)
    return guild.cli.confirm(prompt, default=True)

def _op_flags(op):
    flags = []
    args = op.cmd_args
    i = 1
    while i < len(args):
        cur_arg = args[i]
        i = i + 1
        next_arg = args[i] if i < len(args) else None
        if cur_arg[0:2] == "--":
            if next_arg and next_arg[0:2] != "--":
                flags.append((cur_arg[2:], next_arg))
                i = i + 1
            else:
                flags.append((cur_arg[2:], None))
    return flags

def _format_op_flags(flags):
    return "\n".join(["  %s" % _format_flag(name, val)
                      for name, val in flags])

def _format_flag(name, val):
    if val is None:
        return "%s: (boolean switch)" % name
    else:
        return "%s: %s" % (name, val)

def _handle_run_result(exit_status):
    if exit_status != 0:
        guild.cli.error(exit_status=exit_status)
