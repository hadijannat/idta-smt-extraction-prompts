"""CI: every prompt file must match its pinned SHA-256 hash byte-for-byte.

The SHA pins are load-bearing. A single byte changed in any prompt file
invalidates the corresponding F1 number reported in ``docs/EVALUATION.md``
and in the ETFA 2026 paper. This test enforces the pins on every push.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"
SUMS_PATH = PROMPTS_DIR / "SHA256SUMS"
EXPECTED_VERSIONS = {f"prompt_v{i}.txt" for i in range(5)}


def _parse_sha256sums() -> dict[str, str]:
    """Parse SHA256SUMS into ``{filename: expected_hash}``."""
    expected: dict[str, str] = {}
    for raw_line in SUMS_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        sha, name = line.split(maxsplit=1)
        expected[name.strip()] = sha
    return expected


def test_sha256sums_pins_exactly_five_versions() -> None:
    pinned = set(_parse_sha256sums())
    assert pinned == EXPECTED_VERSIONS, (
        f"SHA256SUMS must pin exactly {sorted(EXPECTED_VERSIONS)}; got {sorted(pinned)}"
    )


def test_every_prompt_matches_its_pinned_hash() -> None:
    expected = _parse_sha256sums()
    for name, want in expected.items():
        path = PROMPTS_DIR / name
        assert path.exists(), f"prompts/{name} is missing"
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == want, (
            f"{name}: pinned {want!r}, actual {actual!r}. "
            "If you intended to revise the prompt, regenerate SHA256SUMS, "
            "bump the version in CHANGELOG.md and CITATION.cff, and update "
            "the F1 numbers in docs/EVALUATION.md."
        )


def test_no_unpinned_prompt_files_in_prompts_dir() -> None:
    on_disk = {p.name for p in PROMPTS_DIR.glob("prompt_*.txt")}
    pinned = set(_parse_sha256sums())
    extras = on_disk - pinned
    assert not extras, f"prompts/ contains files not pinned in SHA256SUMS: {sorted(extras)}"
