#!/bin/bash

# Archivo de log
LOG_FILE="/var/log/auth.log"

# Archivo de salida para registrar los intentos fallidos detectados
OUTPUT_FILE="/var/log/failed_access_attempts.log"

grep "Failed password" "$LOG_FILE" | awk '{for (i=1; i<=NF; i++) if ($i ~ /from/) print $(i+1)}' | sort | uniq -c | sort -nr > "$OUTPUT_FILE"

while read -r line; do
    ATTEMPTS=$(echo $line | awk '{print $1}')
    IP=$(echo $line | awk '{print $2}')

    if [[ "$IP" != "::1" && "$ATTEMPTS" -gt 5 ]]; then
        sudo iptables -A INPUT -s "$IP" -j DROP
        echo "IP bloqueada: $IP debido a $ATTEMPTS intentos fallidos" >> "$OUTPUT_FILE"
    fi
done < "$OUTPUT_FILE"
