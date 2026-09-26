import subprocess
import sys
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
            "NOT_LOGIN_FAILED - IP=192.168.1.10",
            "LOGIN_FAILED - IP=999.999.999.999",
            "LOGIN_FAILED - IP=192.168.1.10.99",
        ]

        self.assertEqual(count_failed_logins(lines), {"192.168.1.10": 2})

    def test_outputs_are_sorted_and_threshold_is_exclusive(self) -> None:
        counts = {"192.168.1.30": 5, "192.168.1.20": 4, "192.168.1.10": 3}
        with tempfile.TemporaryDirectory() as temporary_dir:
            blocked = write_outputs(counts, Path(temporary_dir), threshold=3)

            self.assertEqual(blocked, {"192.168.1.20", "192.168.1.30"})
            self.assertEqual(
                (Path(temporary_dir) / "blocked_ips.txt").read_text(),
                "192.168.1.20\n192.168.1.30\n",
            )
            report = (Path(temporary_dir) / "report.md").read_text()
            self.assertIn("Total blocked IPs: 2", report)
            self.assertIn("192.168.1.20: 4 failed attempts", report)

    def test_cli_from_another_directory(self) -> None:
        script = Path(__file__).with_name("analisis_logs.py").resolve()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            log = root / "input folder" / "fixture.log"
            log.parent.mkdir()
            log.write_text("LOGIN_FAILED - IP=192.0.2.1\n" * 4)
            for extra, output in [([], log.parent), (["--output-dir", str(root / "reports")], root / "reports")]:
                result = subprocess.run([sys.executable, str(script), str(log), *extra], cwd=root, capture_output=True, text=True, check=True)
                self.assertIn("Blocked IPs: 1", result.stdout)
                self.assertEqual((output / "blocked_ips.txt").read_text(), "192.0.2.1\n")

    def test_empty_input_clears_previous_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            write_outputs({"192.0.2.1": 4}, output, 3)
            self.assertEqual(write_outputs(count_failed_logins([]), output, 3), set())
            self.assertEqual((output / "blocked_ips.txt").read_text(), "")
            self.assertIn("Total blocked IPs: 0", (output / "report.md").read_text())


if __name__ == "__main__":
    unittest.main()
