from __future__ import division

import csv
import io
import logging
import subprocess
import sys

from guild.plugins.tensorflow_util import SummaryPlugin

STATS = [
    "index",
    "fan.speed",
    "pstate",
    "memory.total",
    "memory.used",
    "utilization.gpu",
    "utilization.memory",
    "temperature.gpu",
    "power.draw"
]

class GPUPlugin(SummaryPlugin):

    SUMMARY_NAME = "gpu stats"

    def init(self):
        self._stats_cmd = _stats_cmd()

    def enabled_for_op(self, _op):
        return self._stats_cmd is not None

    def read_summary_values(self):
        return _gpu_stats(self._stats_cmd) if self._stats_cmd else {}

def _gpu_stats(stats_cmd):
    stats = {}
    for raw in _read_raw_gpu_stats(stats_cmd):
        stats.update(_calc_gpu_stats(raw))
    return stats

def _read_raw_gpu_stats(stats_cmd):
    p = subprocess.Popen(stats_cmd, stdout=subprocess.PIPE)
    raw_lines = _read_csv_lines(p.stdout)
    result = p.wait()
    if result == 0:
        return raw_lines
    else:
        logging.error("reading GPU stats (smi output: '%s')", raw_lines)
        return []

def _stats_cmd():
    try:
        out = subprocess.check_output(["which", "nvidia-smi"])
    except OSError:
        return None
    else:
        return [
            out.strip(),
             "--format=csv,noheader",
             "--query-gpu=%s" % ",".join(STATS),
        ]

def _read_csv_lines(raw_in):
    csv_in = raw_in if sys.version_info[0] == 2 else io.TextIOWrapper(raw_in)
    return list(csv.reader(csv_in))

def _calc_gpu_stats(raw):
    # See STATS for list of stat names/indexes
    index = raw[0]
    mem_total = _parse_raw(raw[3], _parse_bytes)
    mem_used = _parse_raw(raw[4], _parse_bytes)
    vals = [
        ("fanspeed", _parse_raw(raw[1], _parse_percent)),
        ("pstate", _parse_raw(raw[2], _parse_pstate)),
        ("mem_total", mem_total),
        ("mem_used", mem_used),
        ("mem_free", mem_total - mem_used),
        ("mem_util", _parse_raw(raw[6], _parse_percent)),
        ("util", _parse_raw(raw[5], _parse_percent)),
        ("temp", _parse_raw(raw[7], _parse_int)),
        ("powerdraw", _parse_raw(raw[8], _parse_watts))
    ]
    return dict([(_gpu_val_key(index, name), val) for name, val in vals])

def _parse_raw(raw, parser):
    stripped = raw.strip()
    if stripped == "[Not Supported]":
        return None
    else:
        return parser(stripped)

def _parse_pstate(val):
    assert val.startswith("P")
    return int(val[1:])

def _parse_int(val):
    return int(val)

def _parse_percent(val):
    assert val.endswith(" %")
    return float(val[0:-2]) / 100

def _parse_bytes(val):
    assert val.endswith(" MiB")
    return int(val[0:-4]) * 1024 * 1024

def _parse_watts(val):
    assert val.endswith(" W")
    return float(val[0:-2])

def _gpu_val_key(index, name):
    return "system/gpu%s/%s" % (index, name)
