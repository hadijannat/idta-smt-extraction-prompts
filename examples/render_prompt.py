"""Render one of the v0..v4 prompts with concrete template metadata substituted.

Each prompt contains seven placeholders. Five are *static template metadata*
that you fix once you pick which IDTA Submodel Template you are extracting
from (e.g. IDTA 02006 Digital Nameplate v3.0.1):

- ``{template_id}``        e.g. ``"IDTA 02006"``
- ``{template_version}``   e.g. ``"3.0.1"``
- ``{template_name}``      e.g. ``"Digital Nameplate for Industrial Equipment"``
- ``{idta_number}``        e.g. ``"02006"``
- ``{root_idshort}``       e.g. ``"Nameplate"``

The remaining two are *runtime context* that an extraction pipeline fills in
per LLM call:

- ``{blocks_json}``        JSON list of page-anchored evidence blocks
- ``{node_graph_json}``    JSON dump of the bounded template node graph
                            (see https://github.com/hadijannat/idta-smt-walker)

The prompts contain embedded JSON examples with literal ``{...}`` braces, so
substitution uses ``str.replace`` rather than ``str.format`` to avoid clashing
with Python format-string parsing.

Usage::

    python examples/render_prompt.py v2

Defaults to ``v2`` (the best-F1 version) if no argument is given.
"""

from __future__ import annotations

import argparse
from pathlib import Path

PROMPT_DIR = Path(__file__).resolve().parent.parent / "prompts"

#: Static metadata for IDTA 02006 Digital Nameplate v3.0.1 — the worked
#: example the headline empirical numbers were measured on.
DEFAULT_STATIC_METADATA: dict[str, str] = {
    "template_id": "IDTA 02006",
    "template_version": "3.0.1",
    "template_name": "Digital Nameplate for Industrial Equipment",
    "idta_number": "02006",
    "root_idshort": "Nameplate",
}

#: Placeholder names the extraction pipeline fills in at runtime.
RUNTIME_PLACEHOLDERS: tuple[str, ...] = ("blocks_json", "node_graph_json")


def render_prompt(version: str, substitutions: dict[str, str] | None = None) -> str:
    """Return the named prompt with placeholders substituted.

    Substitution is literal ``str.replace`` because the prompts contain
    embedded JSON braces. Unsubstituted placeholders (including any
    runtime placeholders the caller did not pass in) remain intact.

    Args:
        version: Prompt version label, one of ``v0``, ``v1``, ``v2``, ``v3``, ``v4``.
        substitutions: Mapping of placeholder names (no braces) to replacement
            values. Keys not listed fall back to
            :data:`DEFAULT_STATIC_METADATA`; entirely unknown placeholders are
            left intact.

    Returns:
        The rendered prompt body. If you want the runtime placeholders
        substituted too, include ``blocks_json`` and ``node_graph_json`` in
        ``substitutions``.
    """
    path = PROMPT_DIR / f"prompt_{version}.txt"
    text = path.read_text(encoding="utf-8")
    effective: dict[str, str] = dict(DEFAULT_STATIC_METADATA)
    if substitutions:
        effective.update(substitutions)
    for name, value in effective.items():
        text = text.replace("{" + name + "}", value)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "version",
        nargs="?",
        default="v2",
        choices=["v0", "v1", "v2", "v3", "v4"],
        help="Prompt version to render (default: v2).",
    )
    args = parser.parse_args()

    rendered = render_prompt(args.version)
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
