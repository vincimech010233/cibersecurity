import os
import re
import socket
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG_SCRIPT = ROOT / "soc/check_failed_logins/check_failed_logins.sh"
SCAN_SCRIPT = ROOT / "pentesting/dev-tcp-scanner/port_escan.sh"


class SafeDefaultsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)

    def run_script(self, script, *args, env=None):
        return subprocess.run(
            ["bash", str(script), *map(str, args)],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            timeout=15,
        )

    def test_log_parser_reports_candidates_without_writes(self):
        log = self.work / "auth log.txt"
        log.write_text(
            "".join("Failed password for user from 192.0.2.4 port 22\n" for _ in range(6))
            + "Failed password for user from 127.0.0.1 port 22\n"
            + "Failed password for user from 2001:db8::4 port 22\n"
            + "Failed password for user from ::: port 22\n"
            + "Failed password for user from invalid;command port 22\n"
            + "Accepted password for user from 198.51.100.2 port 22\n"
        )
        result = self.run_script(LOG_SCRIPT, "--log", log)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.splitlines(),
            ["ATTEMPTS ADDRESS CANDIDATE", "6 192.0.2.4 yes", "1 127.0.0.1 no", "1 2001:db8::4 no"],
        )
        self.assertEqual(sorted(path.name for path in self.work.iterdir()), [log.name])
        self.assertNotRegex(LOG_SCRIPT.read_text(), r"\b(?:sudo|iptables|nft|ufw)\b")

    def test_log_parser_rejects_invalid_args_and_missing_file(self):
        self.assertEqual(self.run_script(LOG_SCRIPT, "--wrong", "file").returncode, 2)
        self.assertEqual(self.run_script(LOG_SCRIPT, "--log").returncode, 2)
        self.assertEqual(self.run_script(LOG_SCRIPT, "--log", self.work / "missing").returncode, 1)

    def test_scanner_default_is_loopback_and_ten_ports_without_network(self):
        capture = self.work / "calls.txt"
        timeout_stub = self.work / "timeout"
        timeout_stub.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$SCAN_CAPTURE"\nexit 1\n')
        timeout_stub.chmod(0o755)
        env = dict(os.environ, PATH=f"{self.work}:{os.environ['PATH']}", SCAN_CAPTURE=str(capture))
        result = self.run_script(SCAN_SCRIPT, env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(result.stdout.splitlines()), 10)
        calls = capture.read_text().splitlines()
        self.assertEqual(len(calls), 10)
        self.assertTrue(all(" _ 127.0.0.1 " in call for call in calls))

    def test_scanner_rejects_bad_host_ports_and_ranges(self):
        bad_args = [
            ("--host", "evil;command"),
            ("--host", "999.1.1.1"),
            ("--host", "010.0.0.1"),
            ("--host", "a b"),
            ("--start-port", "0"),
            ("--start-port", "01"),
            ("--start-port", "-1"),
            ("--start-port", "65536"),
            ("--end-port", "65536"),
            ("--end-port", "x"),
            ("--start-port", "10", "--end-port", "1"),
            ("--start-port", "1", "--end-port", "1025"),
            ("--timeout", "0"),
            ("--timeout", "11"),
            ("--timeout", "18446744073709551616"),
            ("--host",),
        ]
        for args in bad_args:
            with self.subTest(args=args):
                self.assertEqual(self.run_script(SCAN_SCRIPT, *args).returncode, 2)

    def test_scanner_detects_local_open_port_and_boundary(self):
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen(1)
            port = listener.getsockname()[1]
            result = self.run_script(
                SCAN_SCRIPT, "--host", "127.0.0.1", "--start-port", port, "--end-port", port
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), f"Port {port} open")
        self.assertEqual(self.run_script(SCAN_SCRIPT, "--start-port", "65535", "--end-port", "65535").returncode, 0)

    def test_shell_syntax_and_compose_bindings(self):
        for script in ROOT.rglob("*.sh"):
            self.assertEqual(subprocess.run(["bash", "-n", str(script)]).returncode, 0, str(script))
        compose_files = list((ROOT / "pentesting/dockerlabs").rglob("docker-compose.y*ml"))
        self.assertTrue(compose_files)
        for compose in compose_files:
            content = compose.read_text()
            for published in re.findall(r'^\s+-\s+["\']?([^"\'\s]+:[0-9]+)["\']?\s*$', content, re.M):
                self.assertTrue(published.startswith("127.0.0.1:"), (compose, published))
        self.assertIn('"127.0.0.1:8080:80"', (ROOT / "pentesting/dockerlabs/injection/docker-compose.yml").read_text())


if __name__ == "__main__":
    unittest.main()
