#!/usr/bin/env python3
"""news-image-20261118 v3 entrypoint: copy the built front page to output.

The front page (entry.png) is built by compose.py at build time from
photorealistic photos in assets/. This entrypoint only copies it, so it
runs with the standard library alone and writes identical bytes on
every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote", dst, os.path.getsize(dst), "bytes")


if __name__ == "__main__":
    main()
