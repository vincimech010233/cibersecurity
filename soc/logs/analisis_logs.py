import re
from collections import Counter

ip_counter = Counter()
with open("simulated_logs.log", "r") as log_file:
    for line in log_file:
        if "LOGIN_FAILED" in line:
            match = re.search(r"IP=(\d+\.\d+\.\d+\.\d+)", line)
            if match:
                ip_counter[match.group(1)] += 1

print("Intentos de acceso fallidos por IP:")
for ip, count in ip_counter.items():
    if count > 3:
        print(f"IP sospechosa detectada: {ip} - Intentos: {count}")


blocked_ips = set()
threshold = 3  # Número de intentos antes de bloquear

for ip, count in ip_counter.items():
    if count > threshold:
        blocked_ips.add(ip)

# Guardar lista de IPs bloqueadas en un archivo
with open("blocked_ips.txt", "w") as block_file:
    for ip in blocked_ips:
        block_file.write(f"{ip}\n")
print("IPs bloqueadas guardadas en blocked_ips.txt")


def enviar_alerta(ip):
    print(f"Alerta: IP sospechosa detectada {ip}")

for ip, count in ip_counter.items():
    if count > threshold:
        enviar_alerta(ip)

with open("report.md", "w") as report:
    report.write("# Resumen de Incidentes\n")
    report.write(f"Total de IPs bloqueadas: {len(blocked_ips)}\n\n")
    report.write("## Detalles de IPs bloqueadas:\n")
    for ip in blocked_ips:
        report.write(f"- {ip}\n")
print("Reporte generado en report.md")
