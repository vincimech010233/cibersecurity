#!/usr/bin/env bash

set -euo pipefail

output_file=${1:-"$(dirname "$0")/simulated_logs.log"}
mkdir -p "$(dirname "$output_file")"
: > "$output_file"

# Generate simulated login events for local defensive-analysis exercises.
for i in {1..20}; do
    if (( RANDOM % 2 )); then
        printf '%s - LOGIN_SUCCESS - User=user%s - IP=192.168.1.%s\n' "$(date)" "$i" "$((RANDOM % 255))" >> "$output_file"
    else
        printf '%s - LOGIN_FAILED - User=user%s - IP=192.168.1.%s\n' "$(date)" "$i" "$((RANDOM % 255))" >> "$output_file"
    fi
done

printf 'Generated %s\n' "$output_file"
