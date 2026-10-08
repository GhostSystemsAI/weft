"""Structural checks on the open-work table in STATUS.md.

Each row of the table that links a GitHub issue or pull request must name
that number in the link text, so a reader of the rendered table sees the
number the row points at. The check reads only the checkout (AGENTS.md
rule 9).

Follow-up: the buildability review (docs/reviews/2026-10-08-buildability.md)
describes a live-state check that fails when a linked issue's state no longer
matches the row. That check needs the GitHub API and runs as a separate CI
step, never as part of this offline test.
"""

import re
from pathlib import Path

STATUS = Path(__file__).resolve().parent.parent / "STATUS.md"
LINK = re.compile(r"\[([^\]]+)\]\((https://github\.com/[^)\s]+/(?:issues|pull)/(\d+))\)")


def open_work_rows():
    lines = STATUS.read_text(encoding="utf-8").splitlines()
    start = lines.index("## Open work")
    rows = []
    for line in lines[start + 1 :]:
        if line.startswith("## "):
            break
        if line.startswith("|") and not line.startswith("|---"):
            rows.append(line)
    return rows[1:]  # drop the header row


def test_open_work_table_has_rows():
    assert open_work_rows()


def test_issue_links_name_their_number():
    mismatches = []
    for row in open_work_rows():
        for text, url, number in LINK.findall(row):
            if not re.search(rf"#{number}\b", text):
                mismatches.append(f"link text {text!r} does not name #{number} for {url}")
    assert not mismatches, "\n".join(mismatches)
