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

## Consideraciones de seguridad

Los registros y direcciones de ejemplo son simulados o privados. No dirijas escáneres contra infraestructura ajena sin autorización escrita. Los ejemplos vulnerables son exclusivamente para laboratorios locales aislados.

## Limitaciones

Todavía no existe una CLI unificada, una suite automática de pruebas ni integración continua.

## Licencia

Aún no se ha elegido una licencia global. Las referencias de terceros conservan sus términos y propiedad.
