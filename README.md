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

## Security considerations

- Example logs and addresses are simulated or private-range data.
- Do not point scanners at third-party infrastructure without written authorization.
- The vulnerable examples are for isolated local laboratories only.
- Never store real credentials, tokens, or production logs in this repository.

## Current limitations

The collection does not yet have a unified CLI, automated test suite, or CI pipeline. Each directory is an independent learning project.

## License

No repository-wide license has been selected. Third-party references retain their original ownership and terms.
