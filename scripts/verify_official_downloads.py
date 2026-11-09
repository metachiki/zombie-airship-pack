"""Verify the fixed-file migration, index hashes, and official downloads (Python 3.11+)."""

import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tomllib
from urllib.request import Request, urlopen
import zipfile


ROOT = Path(__file__).resolve().parents[1]
PRIORITY = (
    "shots-fired", "plushie-buddies", "mct-refined-storage-mixin",
    "immersive-fixes", "gputape", "entityculling",
    "builders-delight-forge", "bee-fix",
)


def check(condition, message):
    if not condition:
        raise ValueError(message)


def get_bytes(url):
    request = Request(url, headers={"User-Agent": "zombie-airship-pack/download-verification"})
    with urlopen(request, timeout=60) as response:
        return response.read()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="b572b5b", help="Original Forge pack commit")
    parser.add_argument("--download-dir", type=Path, help="Fetch and verify the migrated JARs here")
    args = parser.parse_args()
    pack = tomllib.loads((ROOT / "pack.toml").read_text(encoding="utf-8"))
    check(pack["versions"] == {"minecraft": "1.20.1", "forge": "47.4.29"}, "Pack versions changed")
    index_bytes = (ROOT / pack["index"]["file"]).read_bytes()
    check(hashlib.new(pack["index"]["hash-format"], index_bytes).hexdigest() == pack["index"]["hash"], "Index hash mismatch")
    index = tomllib.loads(index_bytes.decode())
    baseline_index = tomllib.loads(subprocess.check_output(
        ["git", "show", f"{args.base}:index.toml"], cwd=ROOT,
    ).decode())
    check({e["file"] for e in index["files"]} == {e["file"] for e in baseline_index["files"]}, "Installed file set changed")
    for entry in index["files"]:
        check(hashlib.new(index["hash-format"], (ROOT / entry["file"]).read_bytes()).hexdigest() == entry["hash"], f"Stale index: {entry['file']}")
    print(f"PASS: pack/index chain, {len(index['files'])} indexed files")

    baseline_paths = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", args.base, "mods/"], cwd=ROOT, text=True,
    ).splitlines()
    baseline_paths = {p for p in baseline_paths if p.endswith(".pw.toml")}
    current_paths = {p.relative_to(ROOT).as_posix() for p in (ROOT / "mods").glob("*.pw.toml")}
    check(current_paths == baseline_paths, "MOD definitions were added or removed")
    candidates = {f"mods/{slug}.pw.toml" for slug in PRIORITY}
    migrated = manual = 0
    for path in sorted(current_paths):
        original_bytes = subprocess.check_output(["git", "show", f"{args.base}:{path}"], cwd=ROOT)
        original = tomllib.loads(original_bytes.decode())
        current = tomllib.loads((ROOT / path).read_text(encoding="utf-8"))
        if path not in candidates:
            check(current == original, f"Unrelated MOD changed: {path}")
            continue
        for key in ("name", "filename", "side"):
            check(current[key] == original[key], f"{path}: {key} changed")
        for key in ("hash-format", "hash"):
            check(current["download"][key] == original["download"][key], f"{path}: original file hash changed")
        if "modrinth" not in current.get("update", {}):
            check(current == original, f"Manual entry changed: {path}")
            print(f"MANUAL: {original['name']} (CurseForge file {original['update']['curseforge']['file-id']})")
            manual += 1
            continue
        migrated += 1
        if not args.download_dir:
            continue
        update = current["update"]["modrinth"]
        version = json.loads(get_bytes(f"https://api.modrinth.com/v2/version/{update['version']}"))
        check(version["project_id"] == update["mod-id"], f"Wrong Modrinth project: {path}")
        check(version["status"] == "listed" and "forge" in version["loaders"] and "1.20.1" in version["game_versions"], f"Incompatible release metadata: {path}")
        download = current["download"]
        check(download.get("mode", "url") == "url", f"Unexpected download mode: {path}")
        matches = [f for f in version["files"] if f["hashes"]["sha1"] == download["hash"] and f["url"] == download["url"]]
        check(len(matches) == 1 and download["url"].startswith("https://cdn.modrinth.com/"), f"URL/hash not published by Modrinth: {path}")
        data = get_bytes(download["url"])
        check(hashlib.sha1(data).hexdigest() == download["hash"], f"Original SHA-1 mismatch: {path}")
        check(hashlib.sha512(data).hexdigest() == matches[0]["hashes"]["sha512"], f"Modrinth SHA-512 mismatch: {path}")
        check(len(data) == matches[0]["size"], f"Size mismatch: {path}")
        with zipfile.ZipFile(io.BytesIO(data)) as jar:
            forge = tomllib.loads(jar.read("META-INF/mods.toml").decode("utf-8-sig"))
        check(forge["modLoader"] == "javafml", f"Not a Forge JAR: {path}")
        args.download_dir.mkdir(parents=True, exist_ok=True)
        (args.download_dir / current["filename"]).write_bytes(data)
        dependencies = [d for group in forge.get("dependencies", {}).values() for d in group if d["modId"] in ("forge", "minecraft")]
        ranges = ", ".join(f"{d['modId']} {d['versionRange']}" for d in dependencies)
        print(f"PASS: {original['name']}: SHA-1 + SHA-512 + size + Forge JAR; {ranges}")
    print(f"PASS: {len(current_paths)} original MOD definitions preserved; {migrated} migrated, {manual} manual")


if __name__ == "__main__":
    main()
