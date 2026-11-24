"""Entry for the make.fun news-image-20261124 bounty.

The front page itself is a finished 1024x1024 PNG (frontpage.png) that
sums up Tuesday 24 November 2026 in one page. This program's job is
simply to deliver that image, intact, as entry.png in the output
directory the harness provides.
"""

import hashlib
import os
import sys

_PNG_MAGIC = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))
_SIZE_LIMIT = 1048576


class FrontPageExporter:
    """Loads frontpage.png, validates it, and exports a verified copy."""

    def __init__(self):
        here = os.path.dirname(os.path.realpath(__file__))
        self._source = os.path.join(here, "frontpage.png")
        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
        self._target = os.path.join(out_dir, "entry.png")
        self._payload = b""

    def _load(self):
        try:
            with open(self._source, "rb") as stream:
                self._payload = stream.read()
        except OSError as exc:
            self._fail(f"cannot read {self._source}: {exc}")
        if self._payload[:8] != _PNG_MAGIC:
            self._fail(f"{self._source} does not start with the PNG signature")
        if len(self._payload) > _SIZE_LIMIT:
            self._fail(
                f"{self._source} is {len(self._payload)} bytes, "
                f"over the {_SIZE_LIMIT} byte limit"
            )

    def _fail(self, message):
        print(f"error: {message}", file=sys.stderr)
        raise SystemExit(1)

    def export(self):
        self._load()
        try:
            os.makedirs(os.path.dirname(self._target) or ".", exist_ok=True)
            with open(self._target, "wb") as stream:
                stream.write(self._payload)
            with open(self._target, "rb") as stream:
                roundtrip = stream.read()
        except OSError as exc:
            self._fail(f"cannot write {self._target}: {exc}")
        if roundtrip != self._payload:
            self._fail(f"verification failed: {self._target} differs from source")
        checksum = hashlib.sha256(self._payload).hexdigest()
        print(f"{self._target}: {len(self._payload)} bytes, sha256 {checksum}")


if __name__ == "__main__":
    FrontPageExporter().export()
