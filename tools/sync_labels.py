# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml>=6"]
# ///
"""Apply the organization's label definitions to its GitHub repositories.

`labels.yml` holds the labels every repository carries; `labels/<repository>.yml`
adds the labels of one repository. Without `--apply` the script only prints
the changes. It calls the GitHub API through `gh`, which takes its token from
`GH_TOKEN`.
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

import yaml

ROOT = Path(__file__).resolve().parent.parent
COLOR = re.compile(r"^[0-9a-f]{6}$")
# GitHub rejects a label description longer than this.
MAX_DESCRIPTION = 100


def load(path: Path) -> dict[str, dict[str, str]]:
    entries = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    labels: dict[str, dict[str, str]] = {}
    for entry in entries:
        name, color = entry["name"], str(entry["color"]).lower()
        description = entry.get("description", "")
        if name in labels:
            sys.exit(f"{path.name}: {name} is defined twice")
        if not COLOR.match(color):
            sys.exit(f"{path.name}: {name} has color {color!r}, not six hex digits")
        if len(description) > MAX_DESCRIPTION:
            sys.exit(
                f"{path.name}: {name} has a description over {MAX_DESCRIPTION} characters"
            )
        labels[name] = {"name": name, "color": color, "description": description}
    return labels


def wanted(repository: str) -> dict[str, dict[str, str]]:
    labels = load(ROOT / "labels.yml")
    own = ROOT / "labels" / f"{repository}.yml"
    if own.exists():
        extra = load(own)
        clash = labels.keys() & extra.keys()
        if clash:
            sys.exit(f"{own.name} redefines shared labels: {', '.join(sorted(clash))}")
        labels |= extra
    return labels


def gh(*args: str, body: dict[str, str] | None = None) -> object:
    command = ["gh", "api", *args]
    if body is not None:
        command += ["--input", "-"]
    result = subprocess.run(
        command,
        check=False,
        input=json.dumps(body) if body is not None else None,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.exit(f"gh api {' '.join(args)}: {result.stderr.strip()}")
    return json.loads(result.stdout) if result.stdout.strip() else None


def listing(path: str) -> list[dict[str, object]]:
    result = subprocess.run(
        ["gh", "api", "--paginate", "--jq", ".[] | tojson", path],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.exit(f"gh api {path}: {result.stderr.strip()}")
    return [json.loads(line) for line in result.stdout.splitlines() if line]


def repositories(org: str) -> list[str]:
    return sorted(
        str(repo["name"])
        for repo in listing(f"orgs/{org}/repos?per_page=100")
        if not repo["archived"] and repo["has_issues"]
    )


def current(org: str, repository: str) -> dict[str, dict[str, str]]:
    return {
        str(label["name"]): {
            "name": str(label["name"]),
            "color": str(label["color"]).lower(),
            "description": str(label["description"] or ""),
        }
        for label in listing(f"repos/{org}/{repository}/labels?per_page=100")
    }


def sync(org: str, repository: str, apply: bool, prune: bool) -> int:
    target, existing = wanted(repository), current(org, repository)
    path = f"repos/{org}/{repository}/labels"
    changes = 0
    for name, label in target.items():
        if name not in existing:
            print(f"{repository}: create {name}")
            if apply:
                gh("-X", "POST", path, body=label)
        elif existing[name] != label:
            print(f"{repository}: update {name}")
            if apply:
                gh("-X", "PATCH", f"{path}/{quote(name, safe='')}", body=label)
        else:
            continue
        changes += 1
    for name in sorted(existing.keys() - target.keys()):
        if prune:
            print(f"{repository}: delete {name}")
            if apply:
                gh("-X", "DELETE", f"{path}/{quote(name, safe='')}")
            changes += 1
        else:
            print(f"{repository}: keep {name} (not defined; --prune deletes it)")
    return changes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--org", default="eoc-llm-tooling")
    parser.add_argument(
        "--repo", action="append", help="limit to this repository; repeatable"
    )
    parser.add_argument("--apply", action="store_true", help="make the changes")
    parser.add_argument(
        "--prune", action="store_true", help="delete labels not defined"
    )
    parser.add_argument(
        "--check", action="store_true", help="validate the label files and exit"
    )
    args = parser.parse_args()

    if args.check:
        load(ROOT / "labels.yml")
        for own in sorted((ROOT / "labels").glob("*.yml")):
            wanted(own.stem)
        print("label files valid")
        return

    names = args.repo or repositories(args.org)
    changes = sum(sync(args.org, name, args.apply, args.prune) for name in names)
    verb = "made" if args.apply else "to make; run with --apply"
    print(f"{changes} change(s) {verb}")


if __name__ == "__main__":
    main()
