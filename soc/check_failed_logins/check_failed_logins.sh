#!/usr/bin/env bash
set -euo pipefail

usage() {
    printf 'Usage: %s [--log FILE]\n' "${0##*/}"
}

log_file=/var/log/auth.log
case $# in
    0) ;;
    2)
        if [[ $1 != --log || -z $2 ]]; then
            usage >&2
            exit 2
        fi
        log_file=$2
        ;;
    1)
        if [[ $1 == --help ]]; then
            usage
            exit 0
        fi
        usage >&2
        exit 2
        ;;
    *)
        usage >&2
        exit 2
        ;;
esac

if [[ ! -f $log_file || ! -r $log_file ]]; then
    printf 'Cannot read log file: %s\n' "$log_file" >&2
    exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then
    printf 'Python 3 is required to validate addresses\n' >&2
    exit 1
fi

printf 'ATTEMPTS ADDRESS CANDIDATE\n'
awk '/Failed password/ {
    for (i = 1; i < NF; i++) {
        if ($i == "from") {
            print $(i + 1)
            break
        }
    }
}' "$log_file" | LC_ALL=C sort | uniq -c | LC_ALL=C sort -k1,1nr -k2,2 |
while read -r attempts address; do
    if ! python3 -c 'import ipaddress, sys; ipaddress.ip_address(sys.argv[1])' "$address" >/dev/null 2>&1; then
        continue
    fi

    candidate=no
    if (( attempts > 5 )) && [[ $address != ::1 && $address != 127.0.0.1 ]]; then
        candidate=yes
    fi
    printf '%s %s %s\n' "$attempts" "$address" "$candidate"
done
