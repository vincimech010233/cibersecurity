# Laboratorio de seguridad defensiva

[English](README.md)

Colección compacta de utilidades defensivas y laboratorios locales deliberadamente vulnerables. Documenta trabajos prácticos de análisis de registros, inspección de sistemas, scripting de red y programación segura.

> Utiliza estos materiales únicamente en sistemas propios o para los que tengas autorización expresa.

## Proyectos

### SOC y análisis defensivo

- `soc/logs/` — genera registros simulados de autenticación, analiza eventos, identifica fallos repetidos y produce un informe.
- `soc/check_failed_logins/` — resumen de accesos fallidos de solo lectura con direcciones candidatas.

### Utilidades de sistemas y redes

- `pentesting/binarios-SUID/` — inventaría binarios SUID y ayuda a compararlos con referencias conocidas.
- `pentesting/dev-tcp-scanner/` — escáner TCP en Bash con puertos validados y localhost por defecto.
- `pentesting/escaner_red/` — ejercicio de escaneo de red en Python para entornos controlados.

### Laboratorios controlados

- `pentesting/dockerlabs/injection/` — ejemplo Docker que contrasta tratamiento PHP vulnerable y más seguro, publicado en loopback.
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

### Revisar accesos fallidos y puertos locales

```bash
bash soc/check_failed_logins/check_failed_logins.sh --log /ruta/al/auth.log
bash pentesting/dev-tcp-scanner/port_escan.sh --start-port 1 --end-port 10
```

La utilidad de accesos fallidos necesita Python 3 para validar direcciones. Lee el registro indicado y muestra recuentos y candidatos. No escribe informes ni modifica reglas del cortafuegos. El escáner utiliza por defecto `127.0.0.1`, puertos 1–10 y timeout de un segundo; `--host` acepta explícitamente `localhost` o una dirección IPv4. Úsalo solo en sistemas propios o con autorización expresa. El puerto Compose del laboratorio vulnerable de inyección y el ejemplo documentado de DVWA se enlazan a `127.0.0.1`.

## Consideraciones de seguridad

Los registros y direcciones de ejemplo son simulados o privados. No dirijas escáneres contra infraestructura ajena sin autorización escrita. Los ejemplos vulnerables son exclusivamente para laboratorios locales aislados.

## Limitaciones

Las pruebas de regresión cubren el analizador de logs simulados, el resumen de accesos fallidos, el escáner TCP y el puerto publicado del laboratorio de inyección. GitHub Actions ejecuta ambas suites Python y comprueba la sintaxis Bash. Desde la raíz, ejecuta `python3 -m unittest discover -s soc/logs -p 'test_*.py' -v` y `python3 -m unittest discover -s tests -p 'test_*.py' -v`. Los demás directorios siguen siendo ejercicios independientes sin validación automática; no existe una CLI unificada.

Antes de estos cambios, el script separado de accesos fallidos podía modificar el cortafuegos, el escáner carecía de validación funcional y el laboratorio de inyección publicaba su puerto en todas las interfaces. Esas rutas ahora tienen informes de solo lectura, argumentos de escaneo validados y enlace a loopback. Esto no establece la seguridad de los demás ejercicios legacy.

## Licencia

Aún no se ha elegido una licencia global. Las referencias de terceros conservan sus términos y propiedad.
