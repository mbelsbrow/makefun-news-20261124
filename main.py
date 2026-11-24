"""make.fun entry: news-image-20261124.

The repository ships a finished front page (frontpage.png, drawn from the
day's wire reports). This program places a copy of it where the grader
expects the entry image, and nothing else. It uses only the standard
library, touches no network, and writes identical bytes on every run.
"""
import hashlib
import os
import sys
from pathlib import Path

IMAGE = "frontpage.png"
OUTPUT_NAME = "entry.png"
LIMIT = 1_048_576  # 1 MiB
SIGNATURE = b"\x89PNG\r\n\x1a\n"


def load_image_bytes():
    path = Path(__file__).resolve().with_name(IMAGE)
    try:
        blob = path.read_bytes()
    except OSError:
        print(f"cannot read {IMAGE} beside main.py", file=sys.stderr)
        sys.exit(1)
    if blob[:8] != SIGNATURE:
        print(f"{IMAGE} does not start with the PNG signature",
              file=sys.stderr)
        sys.exit(1)
    if len(blob) > LIMIT:
        print(f"{IMAGE} exceeds the 1 MiB limit", file=sys.stderr)
        sys.exit(1)
    return blob


def write_entry(blob):
    directory = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / OUTPUT_NAME
    destination.write_bytes(blob)
    if destination.read_bytes() != blob:
        print("verification failed: output differs from source",
              file=sys.stderr)
        sys.exit(1)
    return destination


def main():
    blob = load_image_bytes()
    destination = write_entry(blob)
    digest = hashlib.sha256(blob).hexdigest()
    print(f"{destination}: {len(blob)} bytes, sha256 {digest}")


if __name__ == "__main__":
    main()
