# Defensive Security Lab

[Español](README.es.md)

A compact collection of defensive security utilities and intentionally vulnerable local labs. The repository documents practical work in log analysis, host inspection, network scripting, and secure coding.

> Use these materials only on systems you own or are explicitly authorized to test.

## Projects

### SOC and defensive analysis

- `soc/logs/` — generates simulated authentication logs, analyzes events, identifies repeated failures, and produces a report.
- `soc/check_failed_logins/` — shell utility for reviewing failed login activity.

### System and network utilities

- `pentesting/binarios-SUID/` — inventories SUID binaries and helps compare them with known escalation references.
- `pentesting/dev-tcp-scanner/` — minimal Bash TCP-connectivity scanner.
- `pentesting/escaner_red/` — Python network-scanning exercise intended for controlled environments.

### Controlled vulnerability labs

- `pentesting/dockerlabs/injection/` — local Docker example contrasting vulnerable and safer PHP handling.
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

## Security considerations

- Example logs and addresses are simulated or private-range data.
- Do not point scanners at third-party infrastructure without written authorization.
- The vulnerable examples are for isolated local laboratories only.
- Never store real credentials, tokens, or production logs in this repository.

## Current limitations

The simulated log analyzer has automated regression tests and GitHub Actions CI (Python 3.11 and Bash syntax checks). Run `python3 -m unittest discover -s soc/logs -p 'test_*.py' -v` from the repository root. Other directories remain independent learning exercises without automated validation; there is no unified CLI.

The analyzer writes a candidate IP list; it does not change firewall rules. The separate `soc/check_failed_logins/` script does modify the host firewall and is not part of this tested workflow. The older Docker labs bind to all interfaces by default; review and restrict their port bindings before running them in an isolated environment.

## License

No repository-wide license has been selected. Third-party references retain their original ownership and terms.
