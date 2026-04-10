"""
Scan wedding photo folders and regenerate index.html with embedded gallery data.
Run from this directory: python build_gallery.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".heic", ".heif"}

# Folders that look like the wedding parts (your four download folders)
PART_PATTERN = re.compile(r"part[-\s]?(\d+)", re.IGNORECASE)


def human_album_title(folder_name: str) -> str:
    m = PART_PATTERN.search(folder_name)
    if m:
        return f"Part {m.group(1)}"
    return folder_name


def collect_albums() -> list[dict]:
    albums: list[dict] = []
    for d in sorted(BASE.iterdir(), key=lambda p: p.name.lower()):
        if not d.is_dir():
            continue
        if d.name.startswith((".", "_")):
            continue
        photos: list[dict] = []
        for f in sorted(d.rglob("*")):
            if not f.is_file():
                continue
            if f.suffix.lower() not in IMAGE_EXTS:
                continue
            rel = f.relative_to(BASE).as_posix()
            photos.append({"file": rel, "name": f.name})
        if not photos:
            continue
        albums.append(
            {
                "id": d.name,
                "title": human_album_title(d.name),
                "photos": photos,
            }
        )
    return albums


def main() -> None:
    albums = collect_albums()
    out = BASE / "index.html"
    template = (BASE / "gallery_template.html").read_text(encoding="utf-8")
    data_json = json.dumps(
        {"albums": albums},
        ensure_ascii=False,
        separators=(",", ":"),
    )
    html = template.replace("/*__GALLERY_DATA__*/", data_json)
    out.write_text(html, encoding="utf-8")
    total = sum(len(a["photos"]) for a in albums)
    print(f"Wrote {out} ({len(albums)} albums, {total} photos)")


if __name__ == "__main__":
    main()
