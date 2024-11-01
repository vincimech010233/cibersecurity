#!/bin/bash

# Script en Bash para generar eventos de inicio de sesión fallidos y exitosos
for i in {1..20}; do
    if (( RANDOM % 2 )); then
        echo "$(date) - LOGIN_SUCCESS - User=user$i - IP=192.168.1.$((RANDOM % 255))" >> simulated_logs.log
    else
        echo "$(date) - LOGIN_FAILED - User=user$i - IP=192.168.1.$((RANDOM % 255))" >> simulated_logs.log
    fi
done
