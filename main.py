"""Copy the museum label from entry.txt to the make.fun output dir.

Stdlib only. Reads entry.txt next to this file, validates it, and
writes its exact bytes to $MAKEFUN_OUTPUT_DIR/entry.txt.
"""

import hashlib
import os
import sys
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.txt"
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not output_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1

    try:
        data = source.read_bytes()
    except OSError as exc:
        print(f"error: cannot read entry.txt: {exc}", file=sys.stderr)
        return 1

    text = data.decode("utf-8", errors="strict") if data else ""
    line = text.strip()
    if not line:
        print("error: entry.txt is empty", file=sys.stderr)
        return 1
    if len(line) > 200:
        print(f"error: entry is {len(line)} characters, over the 200 limit", file=sys.stderr)
        return 1
    if "\n" in line:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if len(data) > 1000:
        print("error: entry.txt is unexpectedly large", file=sys.stderr)
        return 1

    out_dir = Path(output_dir)
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "entry.txt"
        out_path.write_bytes(data)
    except OSError as exc:
        print(f"error: cannot write output: {exc}", file=sys.stderr)
        return 1

    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {out_path} ({len(data)} bytes)")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
