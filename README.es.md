# Laboratorio de seguridad defensiva

[English](README.md)

Colección compacta de utilidades defensivas y laboratorios locales deliberadamente vulnerables. Documenta trabajos prácticos de análisis de registros, inspección de sistemas, scripting de red y programación segura.

> Utiliza estos materiales únicamente en sistemas propios o para los que tengas autorización expresa.

## Proyectos

### SOC y análisis defensivo

- `soc/logs/` — genera registros simulados de autenticación, analiza eventos, identifica fallos repetidos y produce un informe.
- `soc/check_failed_logins/` — utilidad shell para revisar intentos de acceso fallidos.

### Utilidades de sistemas y redes

- `pentesting/binarios-SUID/` — inventaría binarios SUID y ayuda a compararlos con referencias conocidas.
- `pentesting/dev-tcp-scanner/` — escáner mínimo de conectividad TCP en Bash.
- `pentesting/escaner_red/` — ejercicio de escaneo de red en Python para entornos controlados.

### Laboratorios controlados

- `pentesting/dockerlabs/injection/` — ejemplo local con Docker que contrasta tratamiento PHP vulnerable y más seguro.
- `pentesting/sql-injection-time/` — documentación de un laboratorio DVWA de inyección SQL temporal.
- `pentesting/xor_signing_exploit/` — demostración educativa de por qué XOR con clave repetida no sirve para autenticar mensajes.

## Requisitos

Cada proyecto puede requerir Python 3, Bash, Docker o Docker Compose. Revisa el código antes de ejecutar scripts con privilegios elevados.

### Reproducir el ejemplo de análisis de logs

```bash
cd soc/logs
./simulated_logs.sh /tmp/simulated_logs.log
python3 analisis_logs.py /tmp/simulated_logs.log --output-dir /tmp/log-analysis-report
```

El log generado, la lista de IP bloqueadas y el informe Markdown se mantienen fuera del control de versiones.

## Consideraciones de seguridad

Los registros y direcciones de ejemplo son simulados o privados. No dirijas escáneres contra infraestructura ajena sin autorización escrita. Los ejemplos vulnerables son exclusivamente para laboratorios locales aislados.

## Limitaciones

El analizador de logs simulados tiene pruebas de regresión y CI con GitHub Actions (Python 3.11 y comprobación de sintaxis Bash). Ejecuta `python3 -m unittest discover -s soc/logs -p 'test_*.py' -v` desde la raíz del repositorio. Los demás directorios siguen siendo ejercicios independientes sin validación automática; no existe una CLI unificada.

El analizador escribe una lista de IP candidatas; no modifica el cortafuegos. El script separado `soc/check_failed_logins/` sí modifica el cortafuegos del equipo y no forma parte de este flujo probado. Los laboratorios Docker antiguos publican puertos en todas las interfaces por defecto; revisa y restringe sus enlaces de puertos antes de ejecutarlos en un entorno aislado.

## Licencia

Aún no se ha elegido una licencia global. Las referencias de terceros conservan sus términos y propiedad.
