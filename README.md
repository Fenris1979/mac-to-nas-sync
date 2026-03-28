# sync_to_nas 🗂️

A lightweight Python script that compares a folder on your Mac to a folder on your NAS and copies over any missing files — including all subfolders and nested files. Designed to run periodically via `cron` so your NAS stays up to date automatically.

---

## Features

- ✅ Recursive — walks the entire folder tree, no matter how deeply nested
- ✅ One-way sync — copies files missing from the NAS, never deletes or overwrites
- ✅ Recreates subfolder structure on the NAS automatically
- ✅ Preserves original file timestamps
- ✅ Skips gracefully if the NAS isn't mounted and logs the reason
- ✅ Logs every run to `~/sync_to_nas.log`
- ✅ No third-party dependencies — uses Python's standard library only

---

## Requirements

- macOS
- Python 3.9+
- NAS mounted and accessible under `/Volumes/`

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Fenris1979/mac-to-nas-sync.git
cd sync_to_nas
```

### 2. Edit the paths

Open `sync_to_nas.py` and update the two paths at the top of the file:

```python
MAC_FOLDER = Path("/Users/yourname/Documents/MyFolder")   # Your local folder
NAS_FOLDER = Path("/Volumes/MyNAS/MyFolder")              # Your NAS mount point
```

Your NAS will appear under `/Volumes/` when it's mounted. You can find its name in **Finder → Locations** in the sidebar, or by running:

```bash
ls /Volumes/
```

### 3. Run manually to test

```bash
python3 sync_to_nas.py
```

You'll see output in the terminal and a log written to `~/sync_to_nas.log`.

---

## Scheduling with Cron

To run the script automatically, add it to your crontab:

```bash
crontab -e
```

Then add one of the following lines:

```bash
# Every hour
0 * * * * /usr/bin/python3 /path/to/sync_to_nas.py

# Every day at 2:00 AM
0 2 * * * /usr/bin/python3 /path/to/sync_to_nas.py

# Every 30 minutes
*/30 * * * * /usr/bin/python3 /path/to/sync_to_nas.py
```

> **Tip:** Not sure where your Python is? Run `which python3` in Terminal to get the full path.

---

## Log File

Every run is logged to:

```
~/sync_to_nas.log
```

Example output:

```
2025-03-28 02:00:01  INFO     ============================================================
2025-03-28 02:00:01  INFO     Sync started
2025-03-28 02:00:01  INFO       Source : /Users/yourname/Documents/MyFolder
2025-03-28 02:00:01  INFO       Target : /Volumes/MyNAS/MyFolder
2025-03-28 02:00:02  INFO     3 file(s) to copy.
2025-03-28 02:00:02  INFO       COPIED  2024/vacation/img1.jpg
2025-03-28 02:00:02  INFO       COPIED  2024/work/report.pdf
2025-03-28 02:00:02  INFO       COPIED  2025/img3.jpg
2025-03-28 02:00:03  INFO     Done — 3 copied, 0 error(s).
2025-03-28 02:00:03  INFO     Sync finished.
```

---

## How It Works

1. Scans the Mac folder recursively using `Path.rglob("*")` to collect every file
2. Does the same for the NAS folder
3. Computes the difference — files on the Mac that are not on the NAS
4. For each missing file, recreates the subfolder path on the NAS and copies the file using `shutil.copy2` (which preserves timestamps)

---

## License

MIT
