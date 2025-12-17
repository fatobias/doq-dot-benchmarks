#!/usr/bin/env python3
import subprocess
import re
import time
import json
from pathlib import Path

RUNS = 30

X_VALUES = range(1, 6) # 127.0.0.x
Y_VALUES = [100, 400, 800]

DURATION = "30s"
DOQ_PORT = 8853
DOT_PORT = 8855

BASE_DIR = Path("~/bench").expanduser()

def flatten_dnspyre_json(j):
    flat = {
        "total_requests": j["totalRequests"],
        "success_responses": j["totalSuccessResponses"],
        "io_errors": j["totalIOErrors"],
        "qps": j["queriesPerSecond"],
        "duration_s": j["benchmarkDurationSeconds"],
    }

    lat = j.get("latencyStats", {})
    for k, v in lat.items():
        flat[k.lower()] = v

    return flat


def average_dicts(dicts):
    avg = {}
    keys = set().union(*(d.keys() for d in dicts))
    keys.discard("run")

    for key in keys:
        values = [d[key] for d in dicts if isinstance(d.get(key), (int, float))]
        avg[key] = sum(values) / len(values)

    return avg

def run_benchmark(label, cmd, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    runs = []

    print(f"\n--- {label} -> {out_dir} ---")

    run_id = 1
    attempts = 0

    while run_id <= RUNS:
        attempts += 1
        print(f"{label} run {run_id}/{RUNS} (attempt {attempts})")

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

        if proc.returncode != 0:
            print(f"dnspyre failed (exit {proc.returncode}), retrying…")
            time.sleep(2)
            continue

        try:
            j = json.loads(proc.stdout.strip())
        except json.JSONDecodeError:
            print("invalid JSON output, retrying")
            time.sleep(2)
            continue

        flat = flatten_dnspyre_json(j)
        flat["run"] = run_id

        (out_dir / f"run_{run_id:02d}.json").write_text(
            json.dumps(j, indent=2)
        )

        runs.append(flat)
        run_id += 1
        time.sleep(5)

    (out_dir / "runs.json").write_text(json.dumps(runs, indent=2))
    avg = average_dicts(runs)
    (out_dir / "averages.json").write_text(json.dumps(avg, indent=2))

for x in X_VALUES:
    for y in Y_VALUES:
        doq_dir = BASE_DIR / f"bench_doq_{x}_{y}"
        doq_cmd = [
            "dnspyre",
            "-s", f"quic://127.0.0.{x}:{DOQ_PORT}",
            f"--concurrency={str(y)}",
            "--no-progress",
            "--no-distribution",
            "--json",
            "--duration", DURATION,
            "--separate-worker-connections",
            "--insecure",
            "google.com",
        ]

        run_benchmark(f"DoQ x={x} y={y}", doq_cmd, doq_dir)

        dot_dir = BASE_DIR / f"bench_dot_{x}_{y}"
        dot_cmd = [
            "dnspyre",
            "--dot",
            "-s", f"127.0.0.{x}:{DOT_PORT}",
            f"--concurrency={str(y)}",
            "--no-progress",
            "--no-distribution",
            "--json",
            "--duration", DURATION,
            "--separate-worker-connections",
            "--insecure",
            "google.com",
        ]

        run_benchmark(f"DoT x={x} y={y}", dot_cmd, dot_dir)

