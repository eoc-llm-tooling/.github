from pathlib import Path

import pytest
import sync_labels

SHARED = """
- name: severity:major
  color: D93F0B
  description: A documented guarantee fails
- name: decision-needed
  color: 5319e7
"""


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


@pytest.fixture
def root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    write(tmp_path / "labels.yml", SHARED)
    monkeypatch.setattr(sync_labels, "ROOT", tmp_path)
    return tmp_path


def test_load_lowercases_colors_and_defaults_the_description(root: Path) -> None:
    labels = sync_labels.load(root / "labels.yml")

    assert labels["severity:major"]["color"] == "d93f0b"
    assert labels["decision-needed"]["description"] == ""


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("- {name: a, color: ffffff}\n- {name: a, color: eeeeee}\n", "defined twice"),
        ("- {name: a, color: fff}\n", "six hex digits"),
        ("- {name: a, color: 000000}\n", "quote it"),
        (f"- {{name: a, color: ffffff, description: {'x' * 101}}}\n", "over 100"),
    ],
)
def test_load_rejects_invalid_entries(tmp_path: Path, text: str, message: str) -> None:
    with pytest.raises(SystemExit, match=message):
        sync_labels.load(write(tmp_path / "bad.yml", text))


def test_wanted_adds_the_repository_labels(root: Path) -> None:
    write(root / "labels" / "proxy.yml", "- {name: 'area:docs', color: bfd4f2}\n")

    assert set(sync_labels.wanted("proxy")) == {
        "severity:major",
        "decision-needed",
        "area:docs",
    }
    assert set(sync_labels.wanted("other")) == {"severity:major", "decision-needed"}


def test_wanted_refuses_a_redefined_shared_label(root: Path) -> None:
    write(root / "labels" / "proxy.yml", "- {name: decision-needed, color: '000000'}\n")

    with pytest.raises(SystemExit, match="redefines shared labels: decision-needed"):
        sync_labels.wanted("proxy")


@pytest.fixture
def github(root: Path, monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, ...]]:
    existing = {
        "severity:major": {
            "name": "severity:major",
            "color": "ffffff",
            "description": "A documented guarantee fails",
        },
        "good first issue": {
            "name": "good first issue",
            "color": "7057ff",
            "description": "",
        },
    }
    calls: list[tuple[str, ...]] = []
    monkeypatch.setattr(sync_labels, "current", lambda org, repo: existing)
    monkeypatch.setattr(sync_labels, "gh", lambda *args, body=None: calls.append(args))
    return calls


def test_a_dry_run_changes_nothing(github: list[tuple[str, ...]]) -> None:
    changes = sync_labels.sync("org", "repo", apply=False, prune=True)

    assert changes == 3
    assert github == []


def test_apply_creates_updates_and_prunes(github: list[tuple[str, ...]]) -> None:
    changes = sync_labels.sync("org", "repo", apply=True, prune=True)

    assert changes == 3
    assert github == [
        ("-X", "PATCH", "repos/org/repo/labels/severity%3Amajor"),
        ("-X", "POST", "repos/org/repo/labels"),
        ("-X", "DELETE", "repos/org/repo/labels/good%20first%20issue"),
    ]


def test_without_prune_undefined_labels_are_kept(
    github: list[tuple[str, ...]],
) -> None:
    changes = sync_labels.sync("org", "repo", apply=True, prune=False)

    assert changes == 2
    assert ("-X", "DELETE", "repos/org/repo/labels/good%20first%20issue") not in github
