"""Analyze simulated authentication logs without relying on the current directory."""

from __future__ import annotations

import argparse
import ipaddress
import re
from collections import Counter
from pathlib import Path
from typing import Iterable

IP_PATTERN = re.compile(r"(?:^|\s)IP=([^\s]+)(?=\s|$)")
FAILED_EVENT_PATTERN = re.compile(r"(?:^|\s)LOGIN_FAILED(?=\s|$)")
DEFAULT_THRESHOLD = 3


def count_failed_logins(lines: Iterable[str]) -> Counter[str]:
    """Return failed-login counts grouped by IP address."""
    counts: Counter[str] = Counter()
    for line in lines:
        if not FAILED_EVENT_PATTERN.search(line):
            continue
        match = IP_PATTERN.search(line)
        if match:
            try:
                address = ipaddress.IPv4Address(match.group(1))
            except ipaddress.AddressValueError:
                continue
            counts[str(address)] += 1
    return counts


def write_outputs(counts: Counter[str], output_dir: Path, threshold: int) -> set[str]:
    """Write deterministic blocked-IP and Markdown report files."""
    blocked = {ip for ip, count in counts.items() if count > threshold}
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "blocked_ips.txt").write_text(
        "".join(f"{ip}\n" for ip in sorted(blocked)), encoding="utf-8"
    )
    report_lines = [
        "# Incident Summary",
        f"Total blocked IPs: {len(blocked)}",
        "",
        "## Blocked IP details",
        *(f"- {ip}: {counts[ip]} failed attempts" for ip in sorted(blocked)),
        "",
    ]
    (output_dir / "report.md").write_text("\n".join(report_lines), encoding="utf-8")
    return blocked


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log_file", type=Path, help="input authentication log")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="directory for blocked_ips.txt and report.md (defaults beside the log)",
    )
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    output_dir = args.output_dir or args.log_file.parent
    with args.log_file.open(encoding="utf-8") as log_file:
        counts = count_failed_logins(log_file)
    blocked = write_outputs(counts, output_dir, args.threshold)
    print("Failed login attempts by IP:")
    for ip, count in sorted(counts.items()):
        print(f"- {ip}: {count}")
    print(f"Blocked IPs: {len(blocked)}")


if __name__ == "__main__":
    main()
