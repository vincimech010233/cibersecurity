import tempfile
import unittest
from pathlib import Path

from analisis_logs import count_failed_logins, write_outputs


class LogAnalysisTests(unittest.TestCase):
    def test_counts_only_failed_events_with_valid_ips(self) -> None:
        lines = [
            "LOGIN_FAILED - IP=192.168.1.10",
            "LOGIN_SUCCESS - IP=192.168.1.10",
            "LOGIN_FAILED - IP=192.168.1.10",
            "LOGIN_FAILED - IP=not-an-ip",
        ]

        self.assertEqual(count_failed_logins(lines), {"192.168.1.10": 2})

    def test_outputs_are_sorted_and_threshold_is_exclusive(self) -> None:
        counts = {"192.168.1.20": 4, "192.168.1.10": 3}
        with tempfile.TemporaryDirectory() as temporary_dir:
            blocked = write_outputs(counts, Path(temporary_dir), threshold=3)

            self.assertEqual(blocked, {"192.168.1.20"})
            self.assertEqual(
                (Path(temporary_dir) / "blocked_ips.txt").read_text(),
                "192.168.1.20\n",
            )
            report = (Path(temporary_dir) / "report.md").read_text()
            self.assertIn("Total blocked IPs: 1", report)
            self.assertIn("192.168.1.20: 4 failed attempts", report)


if __name__ == "__main__":
    unittest.main()
