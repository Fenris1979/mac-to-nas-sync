#!/usr/bin/env python3
"""
sync_to_nas.py
Compares a local Mac folder to a NAS folder and copies any missing files to the NAS.
Designed to be run manually or scheduled via cron / launchd.
"""

import os
import shutil
import logging
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIGURATION — edit these two paths
# ─────────────────────────────────────────────
MAC_FOLDER = Path("/Users/yourname/Documents/MyFolder")   # Source on your Mac
NAS_FOLDER = Path("/Volumes/MyNAS/MyFolder")              # NAS mount point
# ─────────────────────────────────────────────

LOG_FILE = Path.home() / "sync_to_nas.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),          # also print to terminal
    ],
)
log = logging.getLogger(__name__)


def get_relative_files(folder: Path) -> set[Path]:
    """Return a set of all file paths relative to *folder*."""
    return {
        f.relative_to(folder)
        for f in folder.rglob("*")
        if f.is_file()
    }


def sync(mac_folder: Path, nas_folder: Path) -> None:
    log.info("=" * 60)
    log.info("Sync started")
    log.info(f"  Source : {mac_folder}")
    log.info(f"  Target : {nas_folder}")

    # ── Guard checks ──────────────────────────────────────────
    if not mac_folder.exists():
        log.error(f"Source folder not found: {mac_folder}")
        return

    if not nas_folder.exists():
        log.error(
            f"NAS folder not found: {nas_folder}  "
            "(is the NAS mounted?)"
        )
        return

    # ── Compare ───────────────────────────────────────────────
    mac_files = get_relative_files(mac_folder)
    nas_files = get_relative_files(nas_folder)

    missing = mac_files - nas_files          # on Mac but NOT on NAS

    if not missing:
        log.info("Nothing to copy — NAS is already up to date.")
        log.info("Sync finished.\n")
        return

    log.info(f"{len(missing)} file(s) to copy.")

    # ── Copy missing files ────────────────────────────────────
    copied = 0
    errors = 0

    for rel_path in sorted(missing):
        src = mac_folder / rel_path
        dst = nas_folder / rel_path

        try:
            dst.parent.mkdir(parents=True, exist_ok=True)   # recreate sub-dirs
            shutil.copy2(src, dst)                           # copy2 preserves timestamps
            log.info(f"  COPIED  {rel_path}")
            copied += 1
        except Exception as exc:
            log.error(f"  FAILED  {rel_path}  → {exc}")
            errors += 1

    log.info(f"Done — {copied} copied, {errors} error(s).")
    log.info("Sync finished.\n")


if __name__ == "__main__":
    sync(MAC_FOLDER, NAS_FOLDER)
