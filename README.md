# Defensive Security Lab

[Español](README.es.md)

A compact collection of defensive security utilities and intentionally vulnerable local labs. The repository documents practical work in log analysis, host inspection, network scripting, and secure coding.

> Use these materials only on systems you own or are explicitly authorized to test.

## Projects

### SOC and defensive analysis

- `soc/logs/` — generates simulated authentication logs, analyzes events, identifies repeated failures, and produces a report.
- `soc/check_failed_logins/` — read-only failed-login summary with candidate addresses.

### System and network utilities

- `pentesting/binarios-SUID/` — inventories SUID binaries and helps compare them with known escalation references.
- `pentesting/dev-tcp-scanner/` — Bash TCP-connectivity scanner with validated ports and a localhost default.
- `pentesting/escaner_red/` — Python network-scanning exercise intended for controlled environments.

### Controlled vulnerability labs

- `pentesting/dockerlabs/injection/` — Docker example contrasting vulnerable and safer PHP handling, published on loopback.
- `pentesting/sql-injection-time/` — documentation for a DVWA time-based SQL-injection lab.
- `pentesting/xor_signing_exploit/` — educational demonstration of why repeating-key XOR is unsuitable for message authentication.

## Requirements

Requirements vary by project and may include Python 3, Bash, Docker, and Docker Compose. Read the source before running scripts with elevated privileges.

### Reproduce the log-analysis example

```bash
cd soc/logs
./simulated_logs.sh /tmp/simulated_logs.log
python3 analisis_logs.py /tmp/simulated_logs.log --output-dir /tmp/log-analysis-report
```

The generated log, blocked-IP list, and Markdown report are intentionally kept out of version control.

### Review failed logins and local ports

```bash
bash soc/check_failed_logins/check_failed_logins.sh --log /path/to/auth.log
bash pentesting/dev-tcp-scanner/port_escan.sh --start-port 1 --end-port 10
```

The failed-login utility requires Python 3 for address validation. It reads the supplied log and prints counts and candidates. It does not write a report or alter firewall rules. The scanner defaults to `127.0.0.1`, ports 1–10, and a one-second connection timeout; `--host` explicitly accepts `localhost` or an IPv4 address. Use it only on systems you own or are expressly authorized to test. The intentionally vulnerable injection lab's Compose port and the documented DVWA example bind to `127.0.0.1`.

## Security considerations

- Example logs and addresses are simulated or private-range data.
- Do not point scanners at third-party infrastructure without written authorization.
- The vulnerable examples are for isolated local laboratories only.
- Never store real credentials, tokens, or production logs in this repository.

## Current limitations

Automated regression tests cover the simulated log analyzer, failed-login summary, TCP scanner, and the injection lab's published port. GitHub Actions runs both Python suites and checks Bash syntax. From the repository root, run `python3 -m unittest discover -s soc/logs -p 'test_*.py' -v` and `python3 -m unittest discover -s tests -p 'test_*.py' -v`. The remaining directories are independent learning exercises without automated validation; there is no unified CLI.

Before these changes, the separate failed-login script could modify the firewall, the scanner lacked working input validation, and the injection lab published its port on all interfaces. Those paths now have read-only reporting, validated scanner arguments, and a loopback binding. This does not establish safety for the other legacy exercises.

## License

No repository-wide license has been selected. Third-party references retain their original ownership and terms.
