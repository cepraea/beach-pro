"""Validation of local links in the controlled Markdown collection."""

from __future__ import annotations

from pathlib import Path
import re
from urllib.parse import unquote, urlparse

from . import config
from . import reporter as reporter_module


MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
LINE_REFERENCE_RE = re.compile(
    r"^(.*\.(?:md|yaml|yml|json))(?::[0-9]+)?(?:#.*)?$",
    re.IGNORECASE,
)


def normalize_link_target(
    markdown_path: Path,
    raw_target: str,
) -> Path | None:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = unquote(target)
    parsed = urlparse(target)
    if parsed.scheme or target.startswith("#"):
        return None

    match = LINE_REFERENCE_RE.match(target)
    if match:
        target = match.group(1)
    else:
        target = target.split("#", 1)[0]

    candidate = Path(target)
    resolved = (
        candidate.resolve()
        if candidate.is_absolute()
        else (markdown_path.parent / candidate).resolve()
    )
    return resolved


def validate_links(reporter: reporter_module.Reporter) -> None:
    for markdown_path in sorted(
        (config.WORKSPACE_ROOT / "docs").rglob("*.md")
    ):
        text = markdown_path.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK_RE.findall(text):
            target = normalize_link_target(markdown_path, raw_target)
            if target is None:
                continue
            try:
                target.relative_to(config.WORKSPACE_ROOT)
            except ValueError:
                relative_source = markdown_path.relative_to(
                    config.WORKSPACE_ROOT
                )
                reporter.error(
                    f"{relative_source}: local link escapes workspace: "
                    f"{raw_target}"
                )
                continue
            if not target.exists():
                relative_source = markdown_path.relative_to(
                    config.WORKSPACE_ROOT
                )
                reporter.error(
                    f"{relative_source}: broken local link: {raw_target}"
                )
