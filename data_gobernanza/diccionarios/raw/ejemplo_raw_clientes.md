# Diccionario ejemplo - raw_clientes_csv

| Campo | Tipo | Descripcion | Sensibilidad | Owner |
| --- | --- | --- | --- | --- |
| customer_id | string | Identificador entregado por la fuente | Interno | Equipo docente |
| first_name | string | Nombre del cliente | Confidencial | Equipo docente |
| last_name | string | Apellido del cliente | Confidencial | Equipo docente |
| email | string | Correo de contacto | Confidencial | Equipo docente |
| phone | string | Telefono de contacto | Confidencial | Equipo docente |
| created_at | datetime | Fecha de alta en el sistema origen | Interno | Equipo docente |
| ingested_at | datetime | Timestamp de ingesta en raw | Interno | Ingenieria |

Notas: datos llegan en CSV UTF-8; campos obligatorios `customer_id`, `email`. Duplicados se marcan y se loguean en `tmp/historico/clientes.log`.
