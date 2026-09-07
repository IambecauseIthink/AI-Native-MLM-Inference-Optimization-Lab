#!/usr/bin/env python3
"""Capture a sealed benchmark command on a designated remote Linux host."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import signal
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--timeout', type=int, required=True)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    cmd = args.command[1:] if args.command[:1] == ['--'] else args.command
    if platform.system() != 'Linux':
        parser.error('Run benchmark commands only on the designated remote Linux host.')
    if not cmd or args.timeout <= 0:
        parser.error('a command and positive timeout are required')
    args.out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    receipt = {'command': cmd, 'status': 'started', 'started_unix_s': time.time(),
               'timeout_s': args.timeout, 'host': platform.node(), 'quality_verified': False}
    proc = None
    try:
        with (args.out / 'stdout.log').open('wb') as stdout, (args.out / 'stderr.log').open('wb') as stderr:
            proc = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, start_new_session=True)
            receipt.update(pid=proc.pid, pgid=proc.pid)
            (args.out / 'receipt.json').write_text(json.dumps(receipt, indent=2))
            try:
                receipt['exit_code'] = proc.wait(timeout=args.timeout)
                receipt['status'] = 'command-completed' if proc.returncode == 0 else 'command-failed'
            except subprocess.TimeoutExpired:
                receipt['status'] = 'timed-out'
            except KeyboardInterrupt:
                receipt['status'] = 'interrupted'
    except OSError as exc:
        receipt.update(status='launch-failed', error=str(exc), exit_code=127)
    finally:
        if proc is not None:
            # Bound the entire command process group, including residual children.
            try:
                os.killpg(proc.pid, signal.SIGTERM)
                if proc.poll() is None:
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        pass
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            proc.wait()
            receipt.setdefault('exit_code', proc.returncode)
        receipt['elapsed_s'] = time.monotonic() - start
        receipt['sha256'] = {}
        for name in ['stdout.log', 'stderr.log']:
            h = hashlib.sha256()
            with (args.out / name).open('rb') as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    h.update(block)
            receipt['sha256'][name] = h.hexdigest()
        (args.out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))
    raise SystemExit(0 if receipt['status'] == 'command-completed' else 1)


if __name__ == '__main__':
    main()
