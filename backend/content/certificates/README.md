# Certificados

Cada archivo se adjunta a su certificación por nombre: `<categoría>/<slug>.<pdf|png|jpg|webp>`.
Después de agregar o cambiar archivos:

```bash
python manage.py attach_certificates
python manage.py export_fallback
```

Los certificados de MinTIC y Dev Senior tienen el número de documento tapado. Las versiones
sin tapar están en `_originales/`, que no se sube al repositorio.

| Archivo esperado | Certificación |
| --- | --- |
| `development/enterprise-full-stack-spring-angular` | Enterprise Full Stack — Spring Boot 4 y Angular 21 |
| `development/mision-tic-2022-ruta-completa` | Misión TIC 2022 — Ruta completa |
| `development/mision-tic-java` | Misión TIC — Desarrollo de Software con Java |
| `development/mintic-android` | Desarrollo de Aplicaciones Móviles Android |
| `development/mintic-python` | Desarrollo de Software con Python |
| `development/cisco-pcap-python` | PCAP — Fundamentos de Programación en Python |
| `security/lfd121-developing-secure-software` | Developing Secure Software (LFD121) |
| `security/cisco-gestion-amenazas-ciberneticas` | Gestión de Amenazas Cibernéticas |
| `agile/ibm-enterprise-design-thinking` | Enterprise Design Thinking Practitioner |
| `agile/scrum-fundamentals-certified` | Scrum Fundamentals Certified (SFC™) |
| `infra/cisco-ccna-switching-routing-wireless` | CCNAv7: Switching, Routing y Wireless Essentials |
| `infra/cisco-ccna-introduction-to-networks` | CCNAv7: Introduction to Networks |
| `infra/cisco-ndg-linux-unhatched` | NDG Linux Unhatched |
