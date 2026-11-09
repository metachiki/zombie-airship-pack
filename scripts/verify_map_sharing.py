"""Verify the map-sharing addition and its official dependency files (Python 3.11+)."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
import tomllib
from urllib.request import Request, urlopen
import zipfile

ROOT = Path(__file__).resolve().parents[1]
UPDATED = {"xaeros-world-map", "xaeros-minimap", "kotlin-for-forge"}
ADDED = "xaeros-maps-multiplayer-plus"
SUPPORT = {"yacl", "open-parties-and-claims"}


def check(condition, message):
    if not condition:
        raise ValueError(message)


def fetch(url):
    with urlopen(Request(url, headers={"User-Agent": "zombie-airship-pack/map-sharing-verification"}), timeout=60) as response:
        return response.read()


def numbers(version):
    match = re.match(r"\d+(?:\.\d+)*", version)
    check(match is not None, f"Unsupported numeric version: {version}")
    parts = tuple(map(int, match.group().split(".")))
    return parts + (0,) * max(0, 4 - len(parts))


def satisfies(version, requirement):
    requirement = requirement.replace(" ", "")
    actual = numbers(version)
    if not requirement.startswith(("[", "(")):
        return actual == numbers(requirement)
    interior = requirement[1:-1]
    if "," not in interior:
        return actual == numbers(interior)
    lower, upper = interior.split(",")
    lower_ok = not lower or (actual >= numbers(lower) if requirement[0] == "[" else actual > numbers(lower))
    upper_ok = not upper or (actual <= numbers(upper) if requirement[-1] == "]" else actual < numbers(upper))
    return lower_ok and upper_ok


def read_mods(data, records):
    with zipfile.ZipFile(io.BytesIO(data)) as jar:
        if "META-INF/mods.toml" in jar.namelist():
            metadata = tomllib.loads(jar.read("META-INF/mods.toml").decode("utf-8-sig"))
            for mod in metadata["mods"]:
                records[mod["modId"]] = (mod["version"], metadata)
        if "META-INF/jarjar/metadata.json" in jar.namelist():
            for nested in json.loads(jar.read("META-INF/jarjar/metadata.json"))["jars"]:
                read_mods(jar.read(nested["path"]), records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="5a73480", help="Pack before adding map sharing")
    parser.add_argument("--download-dir", type=Path, help="Fetch six relevant official files and check dependency ranges")
    args = parser.parse_args()
    archive = subprocess.check_output(["git", "archive", "--format=tar", args.base, "mods"], cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        before = {m.name: tomllib.loads(tar.extractfile(m).read().decode()) for m in tar if m.isfile() and m.name.endswith(".pw.toml")}
    after = {p.relative_to(ROOT).as_posix(): tomllib.loads(p.read_text(encoding="utf-8")) for p in (ROOT / "mods").glob("*.pw.toml")}
    added_path = f"mods/{ADDED}.pw.toml"
    check(set(after) == set(before) | {added_path}, "Unexpected MOD addition/removal")
    for path, original in before.items():
        if Path(path).name.removesuffix(".pw.toml") in UPDATED:
            check(after[path]["name"] == original["name"] and after[path]["side"] == original["side"], f"Name/side changed: {path}")
        else:
            check(after[path] == original, f"Unrelated MOD changed: {path}")
    check(after["mods/open-parties-and-claims.pw.toml"]["filename"] == "open-parties-and-claims-forge-1.20.1-0.25.8.jar", "Land-claim MOD changed")
    pack = tomllib.loads((ROOT / "pack.toml").read_text(encoding="utf-8"))
    check(pack["versions"] == {"minecraft": "1.20.1", "forge": "47.4.29"}, "Minecraft/Forge changed")
    index_bytes = (ROOT / "index.toml").read_bytes()
    check(hashlib.sha256(index_bytes).hexdigest() == pack["index"]["hash"], "Stale pack hash")
    index = tomllib.loads(index_bytes.decode())
    old_index = tomllib.loads(subprocess.check_output(["git", "show", f"{args.base}:index.toml"], cwd=ROOT).decode())
    check({f["file"] for f in index["files"]} == {f["file"] for f in old_index["files"]} | {added_path}, "Unexpected installed file set")
    for entry in index["files"]:
        check(hashlib.sha256((ROOT / entry["file"]).read_bytes()).hexdigest() == entry["hash"], f"Stale index entry: {entry['file']}")
    print(f"PASS: {len(before)} existing MODs preserved; only three required updates and one addition; all pack/index hashes valid")
    if not args.download_dir:
        return
    records = {}
    for slug in sorted(UPDATED | {ADDED} | SUPPORT):
        metadata = after[f"mods/{slug}.pw.toml"]
        download = metadata["download"]
        if "modrinth" in metadata.get("update", {}):
            update = metadata["update"]["modrinth"]
            version = json.loads(fetch("https://api.modrinth.com/v2/version/" + update["version"]))
            check(version["project_id"] == update["mod-id"], f"Wrong project: {slug}")
            candidates = [f for f in version["files"] if f["url"] == download["url"]]
        else:
            check(download["hash-format"] == "sha1", f"Expected original SHA-1: {slug}")
            version = json.loads(fetch(f"https://api.modrinth.com/v2/version_file/{download['hash']}?algorithm=sha1"))
            candidates = [f for f in version["files"] if f["hashes"]["sha1"] == download["hash"]]
        check("forge" in version["loaders"] and "1.20.1" in version["game_versions"], f"Wrong loader/game version: {slug}")
        file = next(f for f in candidates if f["filename"] == metadata["filename"])
        check(file["url"].startswith("https://cdn.modrinth.com/"), f"Unexpected host: {slug}")
        data = fetch(file["url"])
        check(hashlib.new(download["hash-format"], data).hexdigest() == download["hash"], f"Pack hash mismatch: {slug}")
        for algorithm in ("sha1", "sha512"):
            check(hashlib.new(algorithm, data).hexdigest() == file["hashes"][algorithm], f"API hash mismatch: {slug}")
        check(len(data) == file["size"], f"Size mismatch: {slug}")
        args.download_dir.mkdir(parents=True, exist_ok=True)
        (args.download_dir / metadata["filename"]).write_bytes(data)
        read_mods(data, records)
        print(f"PASS: official file, SHA-1 + SHA-512 + size: {slug}")
    versions = {mod: info[0] for mod, info in records.items()} | {"forge": "47.4.29", "minecraft": "1.20.1"}
    for mod, (version, metadata) in records.items():
        loader = metadata["modLoader"]
        if loader in ("javafml", "kotlinforforge"):
            check(satisfies("47" if loader == "javafml" else versions["kotlinforforge"], metadata["loaderVersion"]), f"Unsatisfied language loader: {mod}")
        for dependency in metadata.get("dependencies", {}).get(mod, []):
            target = dependency["modId"]
            if target in versions:
                check(satisfies(versions[target], dependency["versionRange"]), f"Dependency mismatch: {mod} -> {target} {dependency['versionRange']}")
            else:
                check(not dependency.get("mandatory", False), f"Missing dependency: {mod} -> {target}")
    check("xaerolib" in versions, "Bundled XaeroLib missing")
    print("PASS: Forge/Minecraft, Kotlin loader, both maps, YACL, existing Open Parties and Claims and bundled XaeroLib dependency ranges")
    print("Validated versions:", json.dumps(versions, sort_keys=True))


if __name__ == "__main__":
    main()
